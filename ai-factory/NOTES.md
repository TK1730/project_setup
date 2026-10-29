# Notes

- 日本語で教える。
- ユーザーは Claude Code を日常的に使っている。基礎（CLAUDE.md、skills、hooks）は教え直さない。
- 既存の `scripts/harness/probe.sh` は git worktree と `claude -p` を使って、変更前後のハーネスを比べる。レッスンの例として使える。
- 環境は WSL2。レッスンは Windows のブラウザで開く（`explorer.exe` + `wslpath -w`）。
- 教材一式は `ai-factory/` ディレクトリに置く（ユーザーの指定）。
- 手元の環境に `jq` がない。スクリプトの JSON 処理は `python3` の標準ライブラリで書く。
- Claude Code は v2.1.312（2026-10-29 時点）。`--permission-prompts none` と `--max-budget-usd` が使える。
- スターターキット（`starter/`）はこのリポジトリの中では動かさず、`~/workspace/factory-sandbox` などにコピーして試してもらう。
