---
type: guideline
title: '文書の保守'
description: '文書をコードと同じ変更で直し、死んだ文書を消し、レビューで完璧を求めすぎないための考え方。'
tags: [knowledge, documentation, maintenance, review, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# 文書の保守

文書を書いたあと、どう保ち続けるかをまとめる。
要点は「コードと同じ変更で直す」「死んだ文書はすぐ消す」「レビューで完璧を求めすぎない」の 3 つである。
内容は Google の docguide の Documentation Best Practices と Markdown style guide をもとにしている。

## コードと同じ変更で直す

- 文書は、コードを変えるのと同じ変更（コミットやプルリクエスト）で直す。
  文書が古くならず、レビューする人に変更の意図も伝えられる。
- レビューする人は、doc comment、ヘッダー、`README.md` などの文書も一緒に直すよう求めてよい。

## 死んだ文書を消す

死んだ文書は、誤った情報を流し、作業を遅らせ、散らかしたままで良いという前例になる。
文書の状態が悪いときは、次の順で進める。

1. 少しずつ進める。文書の健全さは徐々に積み上がる。
1. 確実に誤っているものから消し、不明なものは後回しにする。
1. チーム全員で、各文書を残すか消すかを素早く決める。
1. 迷ったら消す。必要なものは後から取り戻せる。
1. 繰り返す。

## レビューで完璧を求めすぎない

文書のレビューの基準は、コードのレビューより低くする。
1 回の変更の基準を下げると、改善の回数が増え、長い目で見て文書が良くなる。

| 立場 | すること |
| :-- | :-- |
| レビューする人 | 妥当ならすぐ承認する。曖昧な指摘より代案を示す。大きな変更は、自分で別の変更として出す（「ついでにこれも」と求めない）。文書を悪くする場合に限って差し戻す |
| 書いた人 | 些細な議論に時間を使わず、早めに折れて先へ進む |

## See also

- [ドキュメントの考え方](/knowledge/documentation-philosophy.md)
- [Google docguide: Documentation Best Practices 要約](/references/google-styleguide/docguide-best-practices.md)
- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
