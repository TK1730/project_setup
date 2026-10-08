---
type: guideline
title: 'ドキュメントの考え方'
description: 'docs を書くときの判断の土台になる考え方。'
tags: [documentation, philosophy, google-docguide]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# ドキュメントの考え方

docs を書くときの判断の土台になる考え方。個々のルールで迷ったときは、ここに立ち返る。

## 少なく、新しく、正確に

- 古く不正確な文書の山より、新しく正確な少数の文書のほうが良い（Minimum Viable Documentation）。
- 簡潔で実用的な文書は、長く網羅的な文書より良い。読者の大半は、書き手の知識のごく一部を素早く何度も必要とするだけである。
- 文書は盆栽のように、生かしつつ頻繁に刈り込む。

## 完璧より改善

- 長い議論より段階的な改善を選ぶ（Better is better than best）。完璧な文書は存在しない。
- 1 行の更新でも価値があればマージする。

## 飾らず、ソースで読める

- 余計な機能より、飾らず消化しやすい内容を選ぶ（Radical simplicity）。
- プレーンテキストで要点が読めるようにする。レンダラーを外しても読めるべきである。
- 内容と見た目を混ぜない。標準の Markdown で足りない場合は、本当に必要かを考え直す。
- 静的な内容は動的な内容より良い。ただし、新鮮さは古さより良い。

## 文書はテストのように扱う

文書の更新は面倒な作業だが、テストと同じく、続けると見返りがある。

## See also

- [文書の種類と置き場所](/guides/document-types.md)
- [文書の保守](/guides/maintenance.md)
- [Google docguide: philosophy.md](https://github.com/google/styleguide/blob/gh-pages/docguide/philosophy.md)
