---
type: reference
title: 'Google docguide: Philosophy 要約'
description: 'Google docguide の Philosophy の要約（飾らない単純さ、ソースで読める文書、最小限の文書、完璧より改善）。'
tags: [documentation, philosophy, google-styleguide, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Google docguide: Philosophy 要約

Google の docguide（Markdown で書く文書のスタイルガイド）のうち、Philosophy の章の要約である。外部ガイドの要約であり、最終的な根拠は原典を参照すること。要点は「飾らず単純に」「ソースのままで読めるように」「少なく実用的に」「議論より少しずつ改善する」の 4 つである。

## 飾らない単純さ（Radical simplicity）

出典: Radical simplicity

- 規模を広げられることと、他と組み合わせられることは、なくてもよい機能をたくさん持つことより大事である。規模は単純さ・速さ・手軽さから生まれ、組み合わせやすさは飾らず消化しやすい内容から生まれる。
- 気が散るものが少ないほど、書きやすく、読みやすい。
- 新しい機能は、最も単純な使い方を邪魔してはならない。必要としない人には見えないままにする。
- Markdown は、早くコードに戻りたい普通のエンジニアのためのものである。大きく複雑な文書も書けるが、それが主な目的ではない。
- 作業の切り替えが少ないほど、人は快適に働ける。エンジニアは、コードを読み書きするのと同じ道具で文書を扱えるべきである。

## ソースのままで読める文書（Readable source text）

出典: Readable source text

- プレーンテキストで足りるだけでなく、それが最も優れている。Markdown が最も広く使える手段であり、HTML は勧めない。
- 内容と見た目を混ぜない。レンダラーを外しても、ソースから要点を読めるようにする。
- ソースを人が読みやすい形に保つと、持ち運びやすく、将来の使い道にも対応しやすい。
- 静的な内容は、特定のサーバーの機能に依存しないので動的な内容より良い。ただし、新しい内容は古い内容より良い。この 2 つの釣り合いをとる。

## 最小限の文書（Minimum viable documentation）

出典: Minimum viable documentation

- 文書はテストのように扱うと育つ。面倒な作業だが、続けると見返りがある。
- 短く実用的な文書は、長く網羅的な文書より良い。読者の大半は、書き手の知識のごく一部を、素早く何度も必要とするだけである。

## 完璧より改善（Better is better than best）

出典: Better is better than best

- 長い議論より、少しずつの改善のほうが良い。不完全さを我慢すると、プロジェクトは自然に育つ。
- 手を付けられない仕事を抱え込まない（原文の比喩は「クッキーをなめて自分のものにせず、皿を回す」）。アイデアは安い。本当にやれるものだけを選び、やれないものは手放す。

## See also

- [Google docguide: philosophy.md](https://github.com/google/styleguide/blob/gh-pages/docguide/philosophy.md)
