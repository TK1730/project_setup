---
type: guideline
title: 'docs の機械チェック（docs_check.py）'
description: 'docs の決まりのうち機械的に判定できるものを確かめるスクリプト docs_check.py の使い方。'
tags: [development, harness, docs, scripts]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-19T00:00:00Z }
stale_after: 2027-10-19T00:00:00Z
---

# docs の機械チェック（docs_check.py）

docs の決まりのうち、機械的に判定できるものを確かめるスクリプトの使い方。docs を書いたあとや作業の区切りに実行し、決まりから外れた箇所を見つける。結果は、作業の質を良くする仕組みの材料にもなる。

## 使い方

リポジトリのルートで実行する。外部ライブラリは使わない。

```bash
python3 scripts/harness/docs_check.py
```

引数を付けないと、`docs/` 全体を確かめる。`docs/unreviewed/` は除く。`unreviewed/` の文書は、移動先の場所を前提に書かれていて、目次の構成も移動先とは違うためである。

ディレクトリを指定すると、その下だけを確かめる。`unreviewed/` の文書は、こうして個別に確かめる。`unreviewed/` の下では、目次を `unreviewed/index.md` の 1 か所にまとめる運用なので、`index.md` の無いディレクトリの文書は `unreviewed/index.md` から辿れるかを確かめる。

```bash
python3 scripts/harness/docs_check.py docs/unreviewed/development/harness-improvement
```

問題が 1 件でもあれば、終了コード 1 を返す。

## 確かめること

決まりの正は [Open Knowledge Format (OKF) の使い方](/conventions/open-knowledge-format.md) と [文書の構成の決まり](/conventions/document-structure.md) である。スクリプトは、そのうち次のものだけを確かめる。

| 確かめること                                                                 | 結果 |
| :--------------------------------------------------------------------------- | :--- |
| Frontmatter があり、7 つのキーが決まりの順にある                             | 問題 |
| `type` が決まりの 6 種のどれかである                                         | 問題 |
| `status` が `draft` / `stable` / `deprecated` のどれかである                 | 問題 |
| H1 が `title` と同じである                                                   | 問題 |
| docs 内へのリンクが `/` で始まる                                             | 問題 |
| 各ディレクトリに `index.md` がある                                           | 問題 |
| 各文書が、そのディレクトリの `index.md` から辿れる                           | 問題 |
| `index.md` の説明文が、リンク先の `description` と同じである                 | 問題 |
| `knowledge/` と `references/` から、プロジェクト固有の文書へリンクしていない | 問題 |
| `stale_after` を過ぎていない                                                 | 警告 |

`index.md` と `log.md` は予約名なので、Frontmatter とリンクの確認から除く。`index.md` の中のリンクは、決まりどおり相対パスで書いてよい。

## 確かめないこと

次のことは機械では判定しにくいので、確かめない。[作業の質の振り返り（work-retro）](/development/harness-improvement/work-retro.md) で扱う。

- 文章の書き方（[文章の書き方の決まり](/conventions/documentation-writing.md)）
- 1 つの文書に 1 つの関心ごとだけを書いているか
- `knowledge/` と `references/` の文章に、プロジェクト固有の内容が書かれていないか。リンクは確かめるが、「このプロジェクトでは〜」のような文章は機械では判定しにくい

`../` で始まるリンクは、docs の外（ソースコードなど）へのリンクとみなして確かめない。docs の中を `../` で指すリンクは見逃す。

## 決定理由（Rationale）

- Python で書いた。Frontmatter の読み取り、リンクの抽出、ディレクトリの走査といった、データの加工が中心のためである。
- 外部ライブラリの YAML パーサーを使わず、トップレベルの `key: value` だけを読む。確かめたいのはキーの有無と値だけであり、依存を増やさずに動かせるようにするためである。
- 期限切れを問題ではなく警告にした。期限切れは文書の誤りではなく、確かめ直す時期が来たという知らせだからである。

## See also

- [docs の機械チェックのスクリプト](../../../scripts/harness/docs_check.py)
- [ハーネス改善の仕組み](/development/harness-improvement/index.md)
