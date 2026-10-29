# 未確認の文書

AI が書き、まだ人が内容を確かめていない文書の置き場所である。ここにある文書は正しい情報として扱わない。

確かめ終わった文書は、パスから `unreviewed/` を外した場所へ移し、移動先の `index.md` に項目を足す。文書内のリンクは移動先の場所を前提に書いてあるので、ここに置いている間は切れているものがある。

目次は、ほかのプロジェクトへ持ち出せる文書（プロジェクト非依存）と、このプロジェクトだけの文書（プロジェクト固有）に分けている。

## プロジェクト非依存

### references

- [migrate-to-e2e スキルの要約](references/tester-army/migrate-to-e2e.md) - TesterArmy の e2e リポジトリが配布するエージェントスキル migrate-to-e2e の中身、インストール先、前提条件、エージェントに指示する操作の要約。
- [モデルと働く人間のための「もっと野心的になる」方法](references/felixrieseberg/how-to-be-more-ambitious.md) - Felix Rieseberg の記事「How to be more ambitious: A tutorial for humans with models」の要約で、AI モデルへの頼み方を Altitude・Depth・Range の 3 方向に広げる方法を説明する。
- [Claude Code チームのコードレビューの進め方](references/claude/blog/claude-code-team-code-review.md) - claude.dev ブログの記事「How the Claude Code team does code review」の要約で、エージェントがコードの大半を書く状況において、人の時間を節約しつつ差し戻しを増やさないレビューの仕組みを説明する。
- [効果的なエージェント自動化の作り方](references/claude/blog/building-effective-agent-automations.md) - Claude ブログの記事「Building effective agent automations」の要約で、定期実行で情報源を読み、前回からの変化をまとめて投稿するエージェントを Claude Managed Agents で作るときの失敗パターンと対策をまとめる。
- [Claude Opus 5.5 を最小コストで最大品質に使う設定ガイド](references/zodchiii/claude-opus-5-5-setup-guide.md) - darkzodchi（@zodchiii）の X 記事「The Claude Opus 5.5 Setup Guide」の要約で、Opus 5 からの移行で費用を増やさないための effort・キャッシュ・API 変更点・プロンプトの設定をまとめる。
- [長時間動くエージェントのための効果的なハーネス](references/claude/engineering/effective-harnesses-for-long-running-agents.md) - Anthropic のエンジニアリングブログの記事「Effective harnesses for long-running agents」の要約で、記憶を持たないセッションをまたいでエージェントに開発を続けさせるための、初期化エージェントとコーディングエージェントの 2 段構成と、状態を引き継ぐファイルを説明する。
- [Harness² の要約](references/google-research/harness2.md) - Google Research が公開した、エージェントのハーネスを再帰的に改良するフレームワーク Harness²（google-research/harness2）の要約。
- [good-css のモダン CSS テクニック要約](references/good-css/modern-css-techniques.md) - good-css.com の要約で、専門家から集めたモダン CSS のテクニック 47 件を、8 つの分類ごとに使う場面と要点でまとめる。
- [エージェントの各ステップを見張らずに済ませるループとグラフ](references/hanakoxbt/loops-and-graphs.md) - Hanako（@hanakoxbt）の X 記事「Loops and Graphs」の要約で、作業単位を正しくするループと作業の形を決めるグラフを分け、人間の承認を最後の 1 ステップだけにする設計を説明する。
- [Pro Git: Commit Guidelines 要約](references/pro-git/commit-guidelines.md) - Git の公式の本 Pro Git の「Commit Guidelines」の要約（空白の誤りの確認、論理的に分けたコミット、コミットメッセージの形）。

## プロジェクト固有

### decisions

- [ADR 2: フロントエンドは車輪の再発明をせずライブラリを使う](decisions/adr-002-use-libraries-instead-of-reinventing.md) - フロントエンドで、学習のために UI 部品やデータ取得を自作する方針をやめ、実績のあるモダンなライブラリや OSS を使うことにした決定。

### development

- [ハーネス改善の仕組み](development/harness-improvement/) - AI と開発するときのやり方を、記録をもとに目的ごとに良くしていく仕組みの使い方。
- [migrate-to-e2e スキルの導入判断](development/migrate-to-e2e-adoption.md) - E2E テストの移行スキル migrate-to-e2e がこのプロジェクトで使えるかと、AGENTS.md の規定に照らした安全性の評価。

### frontend

- [フロントエンドの設計方針](frontend/design-policy.md) - フロントエンドで、実績のあるライブラリや OSS を使って作るための設計方針（サーバーとクライアントの境界、スタイル、UI 部品、データ取得、状態管理、バックエンドとの連携、feature の構成）。

## 戻すときに足す目次の項目

`references/index.md` に足す項目は次のとおりである。

```markdown
- [darkzodchi](zodchiii/) - darkzodchi（@zodchiii）が X に投稿した AI モデル活用に関する記事の要約。
- [Felix Rieseberg](felixrieseberg/) - Felix Rieseberg（Anthropic）のブログ記事の要約。
- [Google Research](google-research/) - Google Research が GitHub で公開しているリポジトリの要約。
- [good-css](good-css/) - good-css.com のモダン CSS テクニック集の要約。
- [Hanako](hanakoxbt/) - Hanako（@hanakoxbt）が X に投稿した AI エージェントの設計に関する記事の要約。
- [Pro Git](pro-git/) - Git の公式の本 Pro Git の要約。
- [TesterArmy e2e](tester-army/) - TesterArmy の E2E テストフレームワーク e2e が配布するエージェントスキルの要約。
```

`references/claude/blog/` は `index.md` ごと戻し、`references/claude/index.md` に `- [Claude 公式ブログ](blog/) - claude.dev ブログに掲載された記事の要約。` を足す。
`references/claude/engineering/` も `index.md` ごと戻し、`references/claude/index.md` に `- [Anthropic エンジニアリングブログ](engineering/) - Anthropic のエンジニアリングブログに掲載された記事の要約。` を足す。
`development/index.md` には、`harness-improvement/` の項目と、`commits.md` と `task-commands.md` の間に導入判断の項目を足す。
