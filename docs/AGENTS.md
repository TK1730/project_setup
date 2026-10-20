---
type: guideline
title: 'docs ディレクトリ運用規約（エージェント向け指示）'
description: 'AI エージェントが docs を探索・作成・更新するときの行動指針。'
tags: [docs, agents, okf]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# docs ディレクトリ運用規約（エージェント向け指示）

このファイルは、AI エージェントが `docs/` 配下のドキュメントを参照・作成・更新する際に遵守すべきルールです。

## 1. 知識の探索ルール（Progressive Disclosure）

エージェントは知識を探索する際、無差別に全ファイルを走査せず、以下の手順を踏むこと。

1. 目次の確認: まず `docs/index.md` を参照し、関心のある領域（frontend, backend, database, knowledge 等）のディレクトリの `index.md` を開く。
1. 目的ドキュメントの特定: `index.md` の説明文とリンクを辿り、最小限の対象ドキュメントのみを読み込む。
1. 鮮度確認: YAML Frontmatter の `status` が `stable` であること、および現在時刻が `stale_after` より前であることを確認する。`verified` の `by` に `human:` があれば人が確かめた文書、なければ AI だけが確かめた文書として扱う。

## 2. ドキュメント作成・更新のルール

エージェントがドキュメントを作成または更新する場合は、書く前に `docs/conventions/` の文書を読み、そのルールに従うこと。`conventions/` にはこのプロジェクトで決めた書き方のルールを置き、1 ファイルに 1 つの関心ごとを書いている。ルールの土台となる一般論は `docs/knowledge/` にあり、各ルールの文書からリンクしている。

| 知りたいこと                       | 読む文書                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| Frontmatter と索引の構造           | [Open Knowledge Format (OKF) の使い方](/conventions/open-knowledge-format.md) |
| ディレクトリの役割と依存の向き     | [Open Knowledge Format (OKF) の使い方](/conventions/open-knowledge-format.md) |
| 作成・更新・削除の流れ、レビュー   | [文書の保守の決まり](/conventions/documentation-maintenance.md)               |
| 1 つの文書の組み立て方、ファイル名 | [文書の構成の決まり](/conventions/document-structure.md)                      |
| 文章の書き方                       | [文章の書き方の決まり](/conventions/documentation-writing.md)                 |
| Markdown の記法                    | [Markdown の書き方の決まり](/conventions/markdown-style.md)                   |
| 何をどこに書くか                   | [書く場所の決まり](/conventions/where-to-document.md)                         |
| 機能・ライブラリの説明文書の型     | [コードを説明する文書の決まり](/conventions/code-docs.md)                     |
| README の書き方                    | [README の決まり](/conventions/readme-writing.md)                             |
| 判断に迷ったときの考え方           | [ドキュメントの考え方](/knowledge/documentation-philosophy.md)                |

AI が書き、まだ人が確かめていない文書は `docs/unreviewed/` に置く。手順は [文書の保守の決まり](/conventions/documentation-maintenance.md) に従う。

機能を説明する文書は、1 つの機能に 1 つの文書にする。機能の区切りは、コードの機能パッケージに合わせる（例: `internal/pomodoro/record/` と `internal/pomodoro/settings/` は別の文書）。機能の文書は `docs/<領域>/features/<機能名>.md` に置き、機能が大きく操作ごとに分けるときは `docs/<領域>/features/<機能名>/` に置く。領域全体に共通する構成と決まりだけを `docs/<領域>/architecture.md` に書く。1 つの文書に複数の機能が混ざっていると、読む人がどの話がどの機能のものか分からなくなるためである。

## 3. 禁止事項

- 1つのドキュメントに無関係な関心事を混在させること（関心の分離違反）。機能の文書の分け方は §2 に従う。
- `knowledge/`、`references/`、`learning/` にプロジェクト固有の内容を書くこと、およびそこからプロジェクト固有の文書やソースコードへリンクすること（依存の向きの違反）。
- 目次（各ディレクトリの `index.md`）から辿れない孤立ファイル（孤島ドキュメント）を作ること。
- 使われなくなった古い記述を放置すること（不要になった情報は削除または `status: deprecated` にする）。

## See also

- [docs の目次](/index.md)
- [Open Knowledge Format (OKF) の使い方](/conventions/open-knowledge-format.md)
- [このプロジェクトの決まりごと](/conventions/)
