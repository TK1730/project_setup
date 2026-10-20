---
type: reference
title: 'Google docguide: Documentation Best Practices 要約'
description: 'Google docguide の Documentation Best Practices の要約（最小限の文書、コードと同時の更新、死んだ文書の削除、書く場所の選び方、重複の禁止）。'
tags: [documentation, best-practices, comments, google-styleguide, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Google docguide: Documentation Best Practices 要約

Google の docguide のうち、Documentation Best Practices の要約である。
外部ガイドの要約であり、最終的な根拠は原典を参照すること。
要点は「文書は少なく新しく保つ」「コードと同じ変更で直す」「伝えたいことはコードに近い手段から順に書く」「同じことを書き直さずリンクする」の 4 つである。

## 最小限の文書とコードと同時の更新

出典: Minimum Viable Documentation / Update Docs with Code / Prefer the Good Over the Perfect

- 散らかった大量の文書より、新しく正確な少数の文書のほうが良い。
  古い、誤っている、重複している情報は削る。
- 文書は盆栽のように、生かしつつ頻繁に刈り込むとうまくいく。
- 文書は、コードを変えるのと同じ変更（CL）で直す。
  レビュアーは、docstring、ヘッダー、`README.md` などの更新を求めてよい。
- 完璧な文書は存在しない。あるのは実績のある方法と慎重な指針だけである。

## 死んだ文書の削除

出典: Delete Dead Documentation

死んだ文書は、誤った情報を流し、作業を遅らせ、散らかしたままで良いという前例になる。
文書の状態が悪いときは、次のように進める。

- 少しずつ進める。文書の健全さは徐々に積み上がる。
- 確実に誤っているものから消し、不明なものは放っておく。
- チーム全員で、各文書を残すか消すかを素早く決める。
- 迷ったら削除する（移行するなら置いていく）。必要なものは後から取り戻せる。
- 繰り返す。

## 書く場所の選び方

出典: Documentation is the Story of Your Code

人とコンピューターの両方が分かるように書くことが目標であり、文書はその一部である。
伝える手段は、短いコメントから長い文章まで次のように並ぶ。

1. 意味のある名前: ローカル変数からクラス、ファイル、ディレクトリまで、名前で伝えられることはコメントや文書に回さない。
1. インラインコメント: コードだけでは表せないこと、たとえば「なぜそのコードがあるか」を書く。
1. メソッドのコメント: メソッドが何をし、どう使うかという「振る舞いの約束」を書く。
   引数、戻り値、注意点や制約、投げる例外や返すエラーを書く。
   ここに書いた振る舞いには、それを確かめるテストがあるのが妥当なことが多いとされる。
   「なぜ」は、使い方の理解に必要な場合を除き、インラインコメントに任せる。
   実用的に書く（原文の例: 「これはハンマーだ。釘を打つのに使う。」）。
1. クラス・ファイルのコメント: 概要と、短い使用例を書く。
   使い方が複数あるときは、最も単純な使い方を先に置く。
1. `README.md`: 初めての人にディレクトリを案内する。
   何を置く場所か、最初に見るべきファイルはどれか、誰が保守していてどこで詳しく知れるかを書く。
1. docs ディレクトリ: 使い始め方、テストの実行、出力のデバッグ、リリースの方法を書く。
1. 設計文書・PRD: 設計への意見を集めるために書く。
   実装後は決定の記録として扱い、半分だけ正しい文書として使わない。
1. 外部の文書（Google Sites、Drive、wiki など）: 使うなら、プロジェクトの `README.md` などから分かりやすくリンクする。

## 重複の禁止

出典: Duplication is Evil

- 共通の技術や手順の手引きを、自分で書き直さない。リンクする。
- 手引きが無い、またはひどく古い場合は、元の場所を更新するか、パッケージ単位の `README.md` を作る。

## See also

- [Google docguide: Philosophy 要約](/references/google-styleguide/docguide-philosophy.md)
- [Google docguide: Markdown style guide 要約](/references/google-styleguide/docguide-style.md)
- [Google docguide: best_practices.md](https://github.com/google/styleguide/blob/gh-pages/docguide/best_practices.md)
