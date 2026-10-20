---
type: reference
title: 'Google docguide: Markdown style guide 要約'
description: 'Google docguide の Markdown style guide の要約（文書の骨子、見出し、リスト、コード、リンク、表、画像）。'
tags: [documentation, markdown, style, google-styleguide, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Google docguide: Markdown style guide 要約

Google の docguide のうち、Markdown style guide の要約である。外部ガイドの要約であり、最終的な根拠は原典を参照すること。目指すのは「ソースのまま読めて持ち運べる」「長くチームをまたいで保守できる」「記法が単純で覚えやすい」の 3 つである。

## 文書の扱い方

出典: Minimum viable documentation / Better is better than best / Capitalization

- 散らかった大量の文書より、新しく正確な少数の文書のほうが良い。本当に必要な文書を見極め、不要なものは小さく頻繁に消す。
- 文書のレビューの基準は、コードのレビューより低くする。レビュアーは、妥当ならすぐ承認し、曖昧な指摘より代案を示し、大きな変更は自分で別の変更として出す。文書を悪くする場合に限って差し戻す。作者は、些細な議論に時間を使わず早めに折れる。
- 製品名・ツール名は、元の大文字小文字のまま書く。

## 文書の骨子

出典: Document layout / Table of contents

- 骨子は「H1 のタイトル → 1〜3 文の短い紹介 → `[TOC]` → H2 の本文 → `## See also`」とする。
- タイトルはファイル名と同じか近い名前にする。H1 は 1 つだけにし、本文は H2 から始める。
- 短い紹介は、その話題を何も知らない人を想定し、「これは何か」「なぜ必要か」に答える。
- `[TOC]` は Gitiles など対応する環境で使い、紹介の後、最初の H2 の前に置く。スクリーンリーダーは置いた位置で目次を読むためである。

## 行と見出し

出典: Character line limit / Trailing whitespace / Headings

- 1 行は 80 文字までにする。コードと同じ道具で扱いやすくするためである。リンク、表、見出し、コードブロックは例外とする。
- 行末に空白を置かない。改行は行末のバックスラッシュで控えめに行い、できれば段落（空行）で済ませる。
- 見出しは `#` の形式（ATX）で書き、`=` や `-` の下線の形式は使わない。`#` の後に空白、前後に空行を置く。
- 見出しは、アンカーが分かりやすくなるよう、文書の中で重複しない完全な名前にする（「Summary」ではなく「Foo summary」）。

## リスト

出典: Lists

- 長く変わりうる番号付きリストは、番号をすべて `1.` と書く（lazy numbering）。短く変わらないリストは、ソースで読みやすいので番号を振る。
- 入れ子のリストは、番号付きも箇条書きも 4 スペースで字下げする。短く入れ子がない 1 行のリストなら、記号の後は 1 スペースでよい。

## コード

出典: Code

- 短いコード、項目名、一般的なファイルの種類（`README.md` など）はインラインコードで書く。自動でリンクにされたくない例の URL もインラインコードで囲む。
- 複数行のコードはフェンスで囲み、言語を明示する。インデントによるコードブロックは、言語を指定できず、始まりと終わりが曖昧なので使わない。
- 端末に貼り付けるコマンドは、改行をバックスラッシュでエスケープする。

## リンク

出典: Links

- リンクはできるだけ短くする。Markdown の文書へは完全な URL ではなく、`/` から始まるパスで書く。
- 相対パスは同じディレクトリの中だけで使い、`../` は避ける。
- リンクテキストに「here」「link」や URL そのものを使わない。文を自然に書いてから、最もふさわしい語句をリンクにする。読者は文書を読むより流し読みするためである。
- 参照リンク（`[text][id]`）は、長いリンクが本文を読みにくくするときと、表のセルを短く保つときに使う。短いリンクには使わない。定義は、最初に使った節の末尾（次の見出しの前）に置く。複数の節で使う定義は文書の末尾に置く。

## 画像と表

出典: Images / Tables

- 画像は控えめに使い、説明するより見せるほうが簡単な場合（画面操作など）に限る。目の見えない読者のために代替テキストを付ける。
- 表は、素早く見比べたい表形式のデータにだけ使う。空のセルが多い、行に対して列が多すぎる、セルに長い文章が入る場合は、リストと小見出しにする。

## HTML より Markdown

出典: Strongly prefer Markdown to HTML

- 標準の Markdown で書き、HTML による工夫は避ける。HTML は文書の読みやすさと持ち運びやすさを下げる。
- やりたいことが Markdown でできないときは、本当に必要かを考え直す。

## See also

- [Google docguide: Philosophy 要約](/references/google-styleguide/docguide-philosophy.md)
- [Google docguide: style.md](https://github.com/google/styleguide/blob/gh-pages/docguide/style.md)
