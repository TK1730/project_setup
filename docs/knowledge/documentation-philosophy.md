---
type: guideline
title: 'ドキュメントの考え方'
description: '文書を書くときの判断の土台になる考え方（少なく新しく正確に、完璧より改善、飾らずソースで読める、文書はテストのように扱う）。'
tags: [knowledge, documentation, philosophy, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# ドキュメントの考え方

文書を書くときの判断の土台になる考え方をまとめる。
個々のルールで迷ったときは、ここに立ち返る。
内容は Google の docguide の考え方をもとにしている。

## 少なく、新しく、正確に

- 古く不正確な文書の山より、新しく正確な少数の文書のほうが良い（Minimum Viable Documentation）。
  古い文書は、誤った情報を流し、読む人の作業を遅らせる。
- 短く実用的な文書は、長く網羅的な文書より良い。
  読者の大半は、書き手の知識のごく一部を、素早く何度も必要とするだけである。
- 文書は盆栽のように、生かしつつ頻繁に刈り込む。
  不要になった記述は、気づいたときにすぐ消す。

## 完璧より改善

- 長い議論より、少しずつの改善を選ぶ（Better is better than best）。
  完璧な文書は存在しない。
- 1 行の更新でも、文書が良くなるなら取り込む。
  1 回の変更の基準を下げると、改善の回数が増え、長い目で見て文書が良くなる。

## 飾らず、ソースで読める

- 余計な機能より、飾らず消化しやすい内容を選ぶ（Radical simplicity）。
- プレーンテキストのままで要点が読めるようにする。
  表示用のソフト（レンダラー）を外しても読めるべきである。
- 内容と見た目を混ぜない。
  標準の Markdown で足りないときは、その表現が本当に必要かを考え直す。
- 静的な内容は、特定のサーバーの機能に依存しないので動的な内容より良い。
  ただし、新しい内容は古い内容より良い。

## 文書はテストのように扱う

- 文書の更新は面倒な作業だが、テストと同じく、続けると見返りがある。
- 文書は、コードを変えるのと同じ変更で直す。
  同じ変更で直すと、文書が古くならず、レビューする人に変更の意図も伝えられる。

## 決定理由（Rationale）

- 考え方を個々のルールと分けて置くのは、ルールに書かれていない場面でも判断できるようにするためである。
  ルールは場面ごとの答えだが、考え方は答えを導く理由になる。
- Google の docguide を土台にしたのは、コードと同じリポジトリで Markdown の文書を保守するための指針として公開されており、出典を確かめられるためである。

## See also

- [書く場所の選び方](/knowledge/where-to-document.md)
- [文書の保守](/knowledge/documentation-maintenance.md)
- [Google docguide: Philosophy 要約](/references/google-styleguide/docguide-philosophy.md)
- [Google docguide: Documentation Best Practices 要約](/references/google-styleguide/docguide-best-practices.md)
- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
