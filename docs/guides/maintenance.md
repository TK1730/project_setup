---
type: guideline
title: '文書の保守'
description: '文書の作成から削除までの流れと、レビューの進め方。'
tags: [documentation, maintenance, lifecycle, okf, review, google-docguide]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# 文書の保守

文書の作成から削除までの流れと、レビューの進め方。文書はコードと同じリポジトリで、コードと同じ変更で保守する（Docs-as-Code）。

## ライフサイクル

1. 作成: Frontmatter を付け、`status: stable`、`verified` に確かめた人または AI と当日の日時、`stale_after` に 1 年後の日時を書く。そのディレクトリの `index.md` に項目を追加する。
1. 更新: 仕様を変えたら、関連コードと同じ PR で文書も更新する。docstring、ヘッダー、`README.md` も対象である。内容を確かめたら `verified` に記録を追加し、`stale_after` を更新する。
1. 鮮度の確認: `stale_after` を過ぎた文書は、現行のコードと突き合わせて確かめ直す。
1. 廃止・削除: 不要になった文書はすぐに削除し、`index.md` からも外す。移行期間が必要なら `status: deprecated` にする。

Frontmatter の各項目の意味は [Open Knowledge Format 運用ガイド](/guides/open-knowledge-format.md) で定める。

## 死んだ文書を削除する

死んだ文書は誤情報を流し、作業を遅らせ、「散らかしたままで良い」という前例になる。文書の状態が悪いときは、次の順で進める。

1. 確実に誤っているものから消す。不明なものは後回しにする。
1. 全員で、各文書を残すか消すかを素早く決める。
1. 迷ったら削除する。git から取り戻せる。
1. 繰り返す。

## レビュー

完璧を求めすぎない。

- レビュアーは、妥当なら直ちに承認し、曖昧な指摘より代案を示す。
- 大きな変更は、別の変更として自分で出す。
- 文書を悪化させる場合に限り、差し戻す。
- 作者は、些細な議論に時間を使わず、早めに折れて先へ進む。

## See also

- [Open Knowledge Format 運用ガイド](/guides/open-knowledge-format.md)
- [ドキュメントの考え方](/guides/philosophy.md)
- [Google docguide: best_practices.md](https://github.com/google/styleguide/blob/gh-pages/docguide/best_practices.md)
