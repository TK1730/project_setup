# 出発点：Claude Code の日常ユーザーで、個人用のエージェント開発工場を作りたい

ユーザーは Claude Code を日常的に使っている（skills・hooks・CLAUDE.md・サブエージェント）。さらに、worktree と `claude -p` で変更前後のハーネスを比べる `scripts/harness/probe.sh` を自分で書いている。
Shapiro のレベルでは 2〜3 の実践者と推定する。目標はレベル4（仕様を渡して数時間走らせ、結果を検証する）。

**Implications**: Claude Code の基本操作は教え直さない。最初は全体像（ファクトリーの部品）から入り、そのあと無人実行・状態の引き継ぎ・検証・運用の順に深める。
