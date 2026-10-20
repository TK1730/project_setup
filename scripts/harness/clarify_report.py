#!/usr/bin/env python3
"""逆質問の記録（gate-events.jsonl）を集計し、依頼に欠けやすい指標を表示する。

使い方:
    python3 scripts/harness/clarify_report.py

指標名は 目的・Done / 制約 / 文脈 / 検証 の 4 つに揃えて数える。
記録そのものは書き換えず、表記ゆれは読み込むときに揃える。
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

INDICATORS = ("目的・Done", "制約", "文脈", "検証")


def gate_dir() -> Path:
    """AGENTS.md の規定どおり ~/.antigravity-gate を優先する。"""
    antigravity = Path.home() / ".antigravity-gate"
    return antigravity if antigravity.is_dir() else Path.home() / ".claude-gate"


def normalize(label: str) -> str | None:
    """表記ゆれ（例: 目的 / 目的・Done定義）を 4 つの指標名に揃える。揃えられなければ None。"""
    for indicator in INDICATORS:
        if label.startswith(indicator.split("・")[0]):
            return indicator
    return None


def main() -> int:
    path = gate_dir() / "gate-events.jsonl"
    if not path.exists():
        print(f"記録がありません: {path}")
        return 1

    totals: Counter[str] = Counter()
    weekly: defaultdict[str, Counter[str]] = defaultdict(Counter)
    unknown: Counter[str] = Counter()
    events = 0

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            week = datetime.fromisoformat(event["ts"]).strftime("%G-W%V")
        except (json.JSONDecodeError, KeyError, ValueError) as err:
            print(f"{lineno} 行目を読み飛ばしました: {err}", file=sys.stderr)
            continue
        if event.get("type") != "clarify":
            continue
        events += 1
        for label in event.get("missing", []):
            indicator = normalize(label)
            if indicator is None:
                unknown[label] += 1
                continue
            totals[indicator] += 1
            weekly[week][indicator] += 1

    print(f"逆質問の件数: {events}\n")
    print("指標ごとの件数（逆質問 1 件に複数の指標が入ることがある）")
    for indicator in INDICATORS:
        share = totals[indicator] / events * 100 if events else 0
        print(f"  {indicator}: {totals[indicator]} 件（{share:.0f}%）")

    print("\n週ごとの件数")
    print("  週        " + " ".join(f"{i:>6}" for i in INDICATORS))
    for week in sorted(weekly):
        print(f"  {week}  " + " ".join(f"{weekly[week][i]:>6}" for i in INDICATORS))

    if unknown:
        print("\n揃えられなかった指標名（normalize に追加を検討）")
        for label, count in unknown.most_common():
            print(f"  {label}: {count} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
