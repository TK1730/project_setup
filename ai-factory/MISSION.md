# Mission: AIファクトリー（AIエージェントによるソフトウェア開発工場）

## Why
普段使っている Claude Code を「対話で使う道具」から「仕様を渡せば実装・テスト・記録まで半自動で回る工場」に育て、個人開発の生産量を上げたい。

## Success looks like
- 自分のリポジトリで、仕様（feature list など）から `claude -p` を無人で回し、1機能ずつ実装 → 検証 → コミットまで進む小さなファクトリーが動いている
- エージェントの「完了」を、自分が全行レビューしなくても信用できる検証の仕組み（テスト・E2E・シナリオ）を持っている
- コスト・失敗・コード劣化を監視して、ファクトリーを継続運用できている

## Constraints
- 個人開発。予算は個人のサブスクリプション / API 費用の範囲（StrongDM の「1人1日$1,000」級ではない）
- Claude Code を日常的に使用（skills・hooks・CLAUDE.md・サブエージェントは既知）
- 既に `scripts/harness/` にハーネス用スクリプトがある（worktree + `claude -p` の比較実行など）

## Out of scope
- NVIDIA 型の GPU データセンター（「AI Factory」の別の意味）
- MLOps / モデルの学習パイプライン
