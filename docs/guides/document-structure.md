---
type: guideline
title: '文書の構成'
description: '1 つの文書の組み立て方（標準骨子）とファイル名のルール。'
tags: [documentation, structure, naming, google-docguide]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# 文書の構成

1 つの文書をどの順番で組み立てるかと、ファイル名の付け方のルール。

## ファイル名

- 内容を表す英語小文字の kebab-case にする（例: `naming-conventions.md`）。
- 1 つのファイルには 1 つの関心ごとだけを書く。
- `index.md` と `log.md` は OKF の予約名なので、文書の名前に使わない。

## 標準骨子

```markdown
---
（Frontmatter）
---

# 文書タイトル

1〜3 文の概要。

## トピック

本文。

## 決定理由（Rationale）

なぜこの設計・選択にしたのか。

## See also

- [関連文書](/knowledge/related.md)
```

1. Frontmatter: [Open Knowledge Format 運用ガイド](/guides/open-knowledge-format.md) のキーを付ける。
1. タイトル: H1 を 1 つだけ置き、Frontmatter の `title` と同じにする。ファイル名と同じか近い名前にする。
1. 概要: Frontmatter の `description` を広げる形で、1〜3 文で「これは何か」「なぜ必要か」を書く（BLUF: 結論を先に書く）。その話題を何も知らない人が読んでも分かるようにする。
1. 本文: H2 から始める。表や Mermaid 図を適宜使う。
1. 決定理由（Rationale）: 設計や選択の背景、検討した代替案。根拠がある場合だけ書く。
1. See also: 関連するコードや文書へのリンクを末尾にまとめる。

## ページ内目次

GitHub は `[TOC]` を描画しないため、ページ内目次は書かない。長くなって目次が欲しくなったら、文書の分割を検討する。

## See also

- [Markdown の書き方](/guides/markdown-style.md)
- [文章の書き方](/guides/writing.md)
- [Google docguide: style.md](https://github.com/google/styleguide/blob/gh-pages/docguide/style.md)
