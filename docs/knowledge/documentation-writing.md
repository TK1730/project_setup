---
type: guideline
title: '文章の書き方'
description: '文書の中の文章を、流し読みする読者に向けて書くための考え方（短く書く、意味の区切りで改行する、初めての人を想定する、名前を正しく書く、内容が分かるリンクにする）。'
tags: [knowledge, documentation, writing, google-docguide, sembr]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# 文章の書き方

文書の中の文章をどう書くかをまとめる。
要点は、短く書くことである。
読者は文書を読むより流し読みするので、要点がすぐ拾える文章にする。
内容は Google の docguide と Semantic Line Breaks の考え方をもとにしている。

## 短く書く

- 短く実用的な文章は、長く網羅的な文章より良い。
  読者の大半は、書き手の知識のごく一部を、素早く何度も必要とするだけである。
- 古い、誤っている、重複している情報は削る。

## 意味の区切りで改行する

- ソースでは、1 文ごとに改行する。
  長い文は、節の区切りでも改行する。
  ソースを開いたとき、文章の形と構造がぱっと見で分かる。
- 切る位置は、句読点の有無ではなく意味のまとまりで決める。
  読点が無くても、「〜ので」「〜けれど」のような節の後で切ってよい。
- 改行の位置に迷ったら、声に出して読む。
  間を置くところや、息継ぎをするところが改行の候補である。
- 1 つの文の変更が 1 行の変更として差分に出るので、レビューもしやすくなる。

```markdown
All human beings are born free and equal in dignity and rights.
They are endowed with reason and conscience
and should act towards one another in a spirit of brotherhood.
```

```markdown
きょうは天気が良かったので
外に出た。
```

## 初めての人を想定して書く

- 文書の冒頭には、1〜3 文の短い紹介を置き、「これは何か」「なぜ必要か」に答える。
- 紹介は、その話題を何も知らない人が読むことを想定して書く。
  書き手が当たり前だと思っている基本の情報こそ、初めての人には足りない。

## 名前を正しく書く

- 製品名、ツール名、プログラム名は、元の大文字と小文字のまま書く（`Markdown`、`GitHub` など）。

## 内容が分かるリンクにする

- リンクの文字列に「ここ」「link」や URL そのものを使わない。
  流し読みする読者の目はリンクに留まるが、「ここ」では何も伝わらない。
- 先に文を自然に書き、そのあとで最もふさわしい語句をリンクにする。

```markdown
詳しくは [Markdown の書き方](markdown.md) を参照する。
```

## See also

- [ドキュメントの考え方](/knowledge/documentation-philosophy.md)
- [文書の構成](/knowledge/document-structure.md)
- [Markdown の書き方](/knowledge/markdown-style.md)
- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
- [Google docguide: Documentation Best Practices 要約](/references/google-styleguide/docguide-best-practices.md)
- [Semantic Line Breaks (SemBr) 要約](/references/sembr/semantic-line-breaks.md)
