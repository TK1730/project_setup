#!/usr/bin/env python3
"""docs の決まりのうち、機械的に判定できるものを確かめる。

使い方:
    python3 scripts/harness/docs_check.py              # docs/ 全体（unreviewed/ を除く）
    python3 scripts/harness/docs_check.py <ディレクトリ>  # 指定したディレクトリの下だけ

決まりの正は docs/conventions/open-knowledge-format.md と docs/conventions/document-structure.md である。
問題があれば終了コード 1 を返す。期限切れ（stale_after）は警告だけで、終了コードには含めない。
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

KEYS = ["type", "title", "description", "tags", "status", "verified", "stale_after"]
TYPES = {"spec", "guideline", "architecture", "database-schema", "decision", "reference"}
STATUSES = {"draft", "stable", "deprecated"}
RESERVED = {"index.md", "log.md"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
INDEX_ITEM = re.compile(r"^[-*] \[[^\]]*\]\(([^)\s]+)\) - (.+)$")


def bundle_parts(path: Path) -> tuple[str, ...]:
    """docs/ からの相対パスの各部分。unreviewed/ の下なら、移動先の場所として返す。"""
    parts = path.resolve().parts
    if "docs" not in parts:
        return ()
    rest = parts[len(parts) - parts[::-1].index("docs") :]
    return rest[1:] if rest[:1] == ("unreviewed",) else rest


def unreviewed_root(directory: Path) -> Path | None:
    """directory が docs/unreviewed/ の下にあれば、その unreviewed/ を返す。"""
    for candidate in [directory, *directory.parents]:
        if candidate.name == "unreviewed" and candidate.parent.name == "docs":
            return candidate
    return None


def frontmatter(text: str) -> dict[str, str] | None:
    """先頭の --- で囲まれた部分を、トップレベルの key: value として読む。無ければ None。"""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip().strip("'\"")
    return fields


def check_doc(path: Path, text: str, errors: list[str], warnings: list[str]) -> None:
    fields = frontmatter(text)
    if fields is None:
        errors.append(f"{path}: Frontmatter がない")
        return
    present = [k for k in fields if k in KEYS]
    missing = [k for k in KEYS if k not in fields]
    if missing:
        errors.append(f"{path}: Frontmatter に {', '.join(missing)} がない")
    elif present != KEYS:
        errors.append(f"{path}: Frontmatter のキーの順番が決まりと違う")
    if fields.get("type") and fields["type"] not in TYPES:
        errors.append(f"{path}: type '{fields['type']}' は決まりの 6 種に無い")
    if fields.get("status") and fields["status"] not in STATUSES:
        errors.append(f"{path}: status '{fields['status']}' は draft / stable / deprecated に無い")

    h1 = re.search(r"^# (.+)$", text, re.M)
    if h1 and fields.get("title") and h1.group(1).strip() != fields["title"]:
        errors.append(f"{path}: H1 と title が違う")

    try:
        if datetime.fromisoformat(fields.get("stale_after", "")) < datetime.now(timezone.utc):
            warnings.append(f"{path}: stale_after を過ぎている。内容を確かめ直す")
    except ValueError:
        errors.append(f"{path}: stale_after が日時として読めない")

    body = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in LINK.findall(body):
        if target.startswith(("/", "http", "#", "mailto:", "../")):
            continue
        if target.split("#")[0].endswith(".md"):
            errors.append(f"{path}: docs 内へのリンク '{target}' は / 始まりで書く")

    # knowledge/ と references/ は、プロジェクト固有の文書に依存しない。
    if bundle_parts(path)[:1] in (("knowledge",), ("references",)):
        for target in LINK.findall(body):
            if target.startswith("/") and not target.startswith(("/knowledge/", "/references/")):
                errors.append(f"{path}: プロジェクト固有の文書 '{target}' へリンクしている")


def check_index(index: Path, errors: list[str]) -> None:
    """目次の各項目の説明文が、リンク先の description と同じかを確かめる。"""
    for line in index.read_text(encoding="utf-8").splitlines():
        item = INDEX_ITEM.match(line)
        if not item or not item.group(1).endswith(".md"):
            continue
        target = index.parent / item.group(1)
        fields = frontmatter(target.read_text(encoding="utf-8")) if target.exists() else None
        if fields and fields.get("description") and item.group(2).strip() != fields["description"]:
            errors.append(f"{index}: '{item.group(1)}' の説明文が description と違う")


def check_tree(root: Path, errors: list[str], warnings: list[str]) -> None:
    skip = root / "unreviewed" if root.name == "docs" else None
    for directory in [root, *sorted(p for p in root.rglob("*") if p.is_dir())]:
        if skip and (directory == skip or skip in directory.parents):
            continue
        docs = sorted(p for p in directory.glob("*.md") if p.name not in RESERVED)
        index = directory / "index.md"
        if not index.exists():
            unreviewed = unreviewed_root(directory)
            if unreviewed is None:
                if docs or any(p.is_dir() for p in directory.iterdir()):
                    errors.append(f"{directory}: index.md がない")
                continue
            # unreviewed/ の下は、目次を unreviewed/index.md の 1 か所にまとめる運用である。
            index = unreviewed / "index.md"
        else:
            check_index(index, errors)
        listed = {
            (index.parent / target).resolve()
            for target in LINK.findall(index.read_text(encoding="utf-8"))
        }
        for doc in docs:
            check_doc(doc, doc.read_text(encoding="utf-8"), errors, warnings)
            if doc.resolve() not in listed:
                errors.append(f"{doc}: {index} から辿れない")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    errors: list[str] = []
    warnings: list[str] = []
    check_tree(root, errors, warnings)
    for message in warnings:
        print(f"警告: {message}")
    for message in errors:
        print(f"問題: {message}")
    print(f"\n問題 {len(errors)} 件、警告 {len(warnings)} 件")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
