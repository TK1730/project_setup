# AIファクトリー Resources

## Knowledge

- [Anthropic Engineering: "Effective harnesses for long-running agents" (Justin Young, 2025-11-26)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  初期化エージェントとコーディングエージェントの組み合わせ、feature list（JSON）、progress file、init.sh、git で状態を引き継ぐ方法。Use for: 無人の作業ラインと、状態の記録の設計。**最初に読む一次資料。**
  - 日本語の解説：[Qiita @nogataka「長時間稼働AIエージェントはなぜ破綻するのか？ Anthropic流の解決アプローチ」(2026-01-06)](https://qiita.com/nogataka/items/72a51b50f73bd96bd941)。翻訳ではなく要点をまとめた解説。フィールド名などの細部は原文で確かめる（原文では `passes`）。
- [GitHub: anthropics/claude-quickstarts の autonomous-coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
  上の記事の実装（Python の Agent SDK）。`agent.py` のループ、`prompts/initializer_prompt.md`、`prompts/coding_prompt.md`、`security.py`（Bash の許可リスト）。Use for: ループとプロンプトの実物を見る。注意：ループの停止条件は `--max-iterations` だけ。
- [OpenAI: "Harness engineering: leveraging Codex in an agent-first world" (Ryan Lopopolo, 2026-02-11)](https://openai.com/index/harness-engineering)
  手書きコードなしで約1,500 PR を出したチームの実践。docs をエージェントの single source of truth にする、linter と構造テストでアーキテクチャを機械的に強制する。Use for: リポジトリ設計、運用中の劣化対策。（WebFetch では 403 だったので、要約は [InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex) 経由）
- [Simon Willison: "How StrongDM's AI team build serious software without even looking at the code" (2026-02-07)](https://simonwillison.net/2026/Feb/7/software-factory/)
  ダークファクトリーの実例：シナリオ（ホールドアウト）、satisfaction、Digital Twin Universe、トークンコスト。批判的な視点も含む。Use for: 検証の設計、コストの議論。
- [Dan Shapiro: "The Five Levels: from Spicy Autocomplete to the Software Factory" (2026-01-23)](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/)
  AI 開発の段階をレベル0〜5に分ける。Use for: 自分が今どこにいて、次はどこを目指すかの位置づけ。
- [Claude Code Docs: Run Claude Code programmatically](https://code.claude.com/docs/en/headless)
  `claude -p`、`--bare`、`--output-format json`、`--permission-mode`、`--permission-prompts none`、`--max-budget-usd`。Use for: 作業ラインを実際に組む（公式の一次情報）。
- [Stanford CodeX: "Built by Agents, Tested by Agents, Trusted by Whom?" (2026-02-08)](https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/)
  ダークファクトリーへの批判的な分析。Use for: 人間のレビューをどこまで省いてよいかを考えるとき。

## Wisdom (Communities)

- （未調査。次のセッションで、Claude Code / エージェント開発の実践者コミュニティを探す）

## Gaps

- 個人の予算で運用しているファクトリーの、実際のコスト事例
- 日本語の一次資料
