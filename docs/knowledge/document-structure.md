---
type: guideline
title: '文書の構成'
description: '1 つの文書を組み立てる順番の指針（タイトル、短い紹介、目次、本文、See also）と、決定の理由を ADR に分けて残す考え方。'
tags: [knowledge, documentation, structure, google-docguide, adr]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# 文書の構成

1 つの文書をどの順番で組み立てるかをまとめる。
骨子は「タイトル → 短い紹介 → 目次 → 本文 → See also」である。
内容は Google の docguide の Markdown style guide と、ADR を提案した Michael Nygard の記事をもとにしている。

## 文書の骨子

```markdown
# 文書のタイトル

短い紹介。

[TOC]

## トピック

本文。

## See also

- [関連する文書](/path/to/related.md)
```

1. タイトル: H1 を 1 つだけ置く。
   ファイル名と同じか、近い名前にする。
1. 短い紹介: 1〜3 文で、話題の全体像を書く。
   その話題を何も知らない人が読むことを想定し、「これは何か」「なぜ必要か」に答える。
1. 目次: 文書を表示する環境が `[TOC]` に対応していれば、紹介の後に置く。
1. 本文: 見出しは H2 から始める。
1. See also: もっと知りたい人や、探していたものが見つからなかった人のために、関連するリンクを末尾にまとめる。

## 目次の置き方

- docguide は、ノートパソコンの 1 画面に内容が収まらないなら、`[TOC]` で目次を出すことを勧めている。
- `[TOC]` は、紹介の後、最初の H2 の前に置く。
  画面で見る人にはどこに置いても同じに見えるが、スクリーンリーダーは置いた位置で目次を読み上げるためである。
- `[TOC]` は Gitiles などの対応する環境で使う書き方であり、どこでも表示されるわけではない。

## 決定の理由を ADR に分ける

- アーキテクチャ上重要な決定（構造、非機能の特性、依存関係、インターフェース、作り方に影響する決定）は、その理由を ADR に 1 つずつ残す。
- 大きな文書は更新されず、読まれもしない。
  決定の理由を ADR に分けると、文書も ADR も小さく保てる。
- 書き方は [ADR の書き方](/knowledge/architecture-decision-records.md) を参照する。

## See also

- [ADR の書き方](/knowledge/architecture-decision-records.md)
- [文章の書き方](/knowledge/documentation-writing.md)
- [Markdown の書き方](/knowledge/markdown-style.md)
- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
- [Documenting Architecture Decisions 要約](/references/cognitect/documenting-architecture-decisions.md)
