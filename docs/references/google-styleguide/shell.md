---
type: reference
title: 'Google Shell Style Guide 要約'
description: 'Google Shell Style Guide の要約（シェルを使う場面、クオート、エラー処理）。'
tags: [shell, bash, google-styleguide, scripting]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# Google Shell Style Guide 要約

Google の Shell Style Guide を、小さなスクリプトや Taskfile のコマンドを書く開発者向けに要約した参考資料である。外部ガイドの要約であり、最終的な根拠は原典を参照すること。要点は「シェルは小さな用途に限る」「bash を使い、変数は必ず引用符で囲む」「コマンドの戻り値を確認し、エラーは STDERR に出す」の 3 つである。

## シェルを使う場面

出典: Background > When to use Shell / Which Shell to Use

- シェルは小さなユーティリティや単純なラッパースクリプトにだけ使う。他のコマンドを呼ぶのが中心で、データ加工が少ない用途なら許容される。
- 性能が重要なら、シェル以外を使う。
- 100 行を超える、または制御フローが単純でないスクリプトは、構造化された言語で書き直す。スクリプトは育つので、早めの書き直しが推奨されている。
- 実行ファイルに使えるシェルは bash のみで、先頭は `#!/bin/bash` とする。オプションは最小限にし、`set` でシェルオプションを設定する。こうすると `bash script_name` で呼んでも動作が変わらない。

## 書き方の基本

出典: Features and Bugs / Naming Conventions / Formatting

- 変数は引用符で囲み、波括弧を付ける（`"${var}"`）。引数をそのまま渡すときは `"$@"` を使う。`$*` はほぼ常に不適切とされている（Formatting > Quoting）。

  ```bash
  echo "${name}"
  other_command "$@"
  ```

- 条件式は `[ ... ]` や `test` ではなく `[[ ... ]]` を使う。パス名展開と単語分割が起きないため、誤りが減る（Tests）。
- 空文字の判定は `-z` / `-n` を使う（Testing Strings）。数値の比較と計算は `(( ... ))` を使い、`[[ ... ]]` の `>` は辞書順比較になるので避ける（Arithmetic）。
- コマンド置換はバッククォートではなく `$(command)` を使う。入れ子でもエスケープが要らない（Command Substitution）。
- ShellCheck で一般的な不具合を検出することが推奨されている（ShellCheck）。
- 関数名と変数名は小文字のスネークケース、定数と環境変数は大文字のスネークケースで、ファイル先頭に宣言する（Naming Conventions）。

  ```bash
  readonly BACKUP_DIR='/var/backup'
  my_func() { local name="$1"; }
  ```

- 関数内の変数は `local` で宣言する。コマンド置換の結果を代入するときは、宣言と代入を別の文に分ける。`local x="$(cmd)"` では `$?` が `local` の終了コードになり、`cmd` の失敗を見逃す（Use Local Variables）。
- 関数が 1 つ以上ある長さのスクリプトでは `main` 関数を置き、最後の行を `main "$@"` にする。短い直線的なスクリプトでは不要（main）。
- `eval` は避ける（Eval）。`.sh` 拡張子は、実行ファイルでは付けても付けなくてもよく、ライブラリには付ける（File Extensions）。

## エラー処理

出典: Environment > STDOUT vs STDERR / Calling Commands > Checking Return Values

- エラーメッセージはすべて STDERR に出す。通常の出力と問題を分離できる。`err` のような出力用関数を用意することも推奨されている。

  ```bash
  err() { echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2; }
  ```

- コマンドの戻り値は必ず確認し、意味のある終了コードを返す。`if ! cmd; then` で直接確認する形が簡潔である。

  ```bash
  if ! mv "${src}" "${dest_dir}/"; then err "mv failed"; exit 1; fi
  ```

- パイプの各段の結果は `PIPESTATUS` で確認できる。次のコマンドで上書きされるので、必要なら直後に別の変数へ退避する。
- `set -euo pipefail` は広く使われている慣習だが、このガイドは推奨も要求もしていない。ガイドが強調するのは戻り値の明示的な確認である。ガイドが `set -e` に触れるのは Arithmetic の節で、`set -e` 有効時に `(( i++ ))` がシェルを終了させる例を挙げている。使う場合は、この挙動を理解したうえで判断する。

## See also

- [Google Shell Style Guide（原典）](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://www.shellcheck.net/)
- [Markdown の書き方](/knowledge/markdown-style.md)
- [docs ハブ](/index.md)
