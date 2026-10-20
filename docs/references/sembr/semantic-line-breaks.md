---
type: reference
title: 'Semantic Line Breaks (SemBr) 要約'
description: 'Semantic Line Breaks の仕様の要約（意味の区切りで改行する規則、使う理由、既存の文書の移し方、Git での差分の見方、由来）。'
tags: [documentation, markdown, line-breaks, sembr]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Semantic Line Breaks (SemBr) 要約

Mattt が公開している Semantic Line Breaks（SemBr）の仕様の要約である。
外部仕様の要約であり、最終的な根拠は原典を参照すること。
要点は「ソースでは、意味のまとまりごとに改行する」の 1 つである。
英語の文章を前提にした仕様である。

## SemBr の考え方

出典: Summary / Introduction

- Markdown、reStructuredText、AsciiDoc などは、続く 2 つの行を空白 1 つでつないで表示する。
  そのため、ソースの改行を意味の区切りとして使っても、表示は変わらない。
- 1 文ごとに改行すると、ソースで文章の形と構造が分かりやすくなる。
  さらに節（clause）の区切りでも改行すると、文の組み立てが見えやすくなる。

```markdown
All human beings are born free and equal in dignity and rights.
They are endowed with reason and conscience
and should act towards one another in a spirit of brotherhood.
```

## SemBr の規則

出典: Semantic Line Breaks Specification (SemBr)

規則の強さは RFC 2119 の言葉（MUST、SHOULD、MAY など）で表す。

1. 文章は SemBr を使ってよい（MAY）。
1. 改行は、表示される結果を変えてはならない（MUST NOT）。
1. 改行は、文の意味を変えるべきではない（SHOULD NOT）。
1. ピリオド、感嘆符、疑問符で終わる文の後では、改行しなければならない（MUST）。
1. カンマ、セミコロン、コロン、エムダッシュで区切られた独立節の後では、改行するべきである（SHOULD）。
1. 文の構造を分かりやすくするためや、行の長さを守るために、従属節の後で改行してよい（MAY）。
1. 番号付きや箇条書きのリストの前では、改行することを勧める（RECOMMENDED）。
1. 関係する項目をまとめるためや、行の長さを守るために、リストの項目の後で改行してよい（MAY）。
1. ハイフンでつないだ語の途中で改行してはならない（MUST NOT）。
1. リンクの前後で改行してよい（MAY）。
1. インラインの装飾の前で改行してよい（MAY）。
1. 1 行の長さは 80 文字までを勧める（RECOMMENDED）。
1. リンクやコードなどのために必要なら、1 行が 80 文字を超えてよい（MAY）。

## SemBr を使う理由

出典: Why Use Semantic Line Breaks?

- 書く人にとって: 文章の見た目の構造が、考えの構造と一致する。
- 直す人にとって: 文法の誤りや、意図を変えずに簡潔にできる箇所を見つけやすい。
- 一緒に作業する人にとって: 1 つの文や節の変更が 1 行の変更として現れる。
  段落全体が詰め直されたような差分にならず、履歴が追いやすい。
- 読む人にとって: 表示には何の影響もなく、改行は見えない。

## SemBr の使い方

出典: FAQ

- どこで改行するか迷ったら、声に出して読む。
  強調のために間を置くところや、息継ぎをするところが改行の候補である。
- 既存の文書を一度に書き直す必要はない。
  新しく書く文と直した文から SemBr を使う。
  見た目が違うので、まだ直していない箇所がすぐ分かり、見直しの機会にもなる。
- Git の通常の差分は行単位なので、SemBr の文章では変更が見えにくいことがある。
  `git diff --word-diff` を使うと単語単位で比べられる。
- 自動で改行を入れたり確かめたりする道具や、コーディングエージェント向けのスキルもある。
- 表示でも改行したいときは、Markdown なら行末にバックスラッシュを置く。
  行末の 2 つの空白でも改行できるが、行末の空白を自動で消す道具とは相性が悪い。

## SemBr の由来

出典: About / Brandon Rhodes「Semantic Linefeeds」（2012）

1. 1974 年に Brian W. Kernighan が、Bell 研究所の技術メモ「UNIX for Beginners」の「文書を書くときのヒント」の節で、次のように勧めた。
   各文を新しい行から始め、行を短くし、カンマやセミコロンの後など自然な場所で改行する。
   文書は何度も書き直され、人は句を書き換えたり文を足し引きしたり並べ替えたりして直すので、後の編集が楽になる、という理由である。
1. 2012 年に Brandon Rhodes が、ブログ記事「Semantic Linefeeds」で、自分が長く使ってきたこの書き方に名前を付け、出典が上の Kernighan のメモであることを突き止めた。
1. Mattt が、いくつかの会社のテクニカルライティングのチームで見てきたやり方を、SemVer の仕様の構成にならって SemBr の仕様にまとめた。
   Rhodes の記事は、由来を調べた資料として紹介されている。

## See also

- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
- [Semantic Line Breaks](https://sembr.org/)
- [One sentence per line (Brandon Rhodes)](http://rhodesmill.org/brandon/2012/one-sentence-per-line/)
