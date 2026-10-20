---
type: reference
title: 'Pro Git: Commit Guidelines 要約'
description: 'Git の公式の本 Pro Git の「Commit Guidelines」の要約（空白の誤りの確認、論理的に分けたコミット、コミットメッセージの形）。'
tags: [git, commit, pro-git]
status: draft
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Pro Git: Commit Guidelines 要約

Git の公式サイトで公開されている本『Pro Git』第 2 版の、5.2 節「Contributing to a Project」にある「Commit Guidelines」の要約である。
外部資料の要約であり、最終的な根拠は原典を参照すること。
要点は「空白の誤りを入れない」「1 つのコミットを論理的に 1 つのまとまりにする」「メッセージは短い要約、空行、詳しい説明の順に書く」の 3 つである。
原典は、Git プロジェクト自身の手引き（Git のソースの `Documentation/SubmittingPatches`）にも良い助言がある、と紹介している。

## 空白の誤りを入れない

出典: Commit Guidelines

- コミットに、空白の誤り（行末の余計な空白など）を入れない。
- コミットの前に `git diff --check` を実行すると、空白の誤りの候補を一覧にしてくれる。
  ほかの開発者を困らせる空白の誤りを、コミットする前に見つけられる。

## 論理的に分けたコミット

出典: Commit Guidelines

- 1 つのコミットを、論理的に 1 つのまとまりの変更にする。
- 変更を消化しやすい大きさに分ける。
  週末に 5 つの課題を続けて書き、月曜日に 1 つの巨大なコミットで出すことはしない。
  週末にコミットしなかったとしても、月曜日にステージングエリアを使い、少なくとも課題ごとに 1 つのコミットに分け、それぞれに役立つメッセージを付ける。
- 同じファイルに別々の変更が入っているときは、`git add --patch` でファイルの一部だけをステージする。
- 1 つにまとめても 5 つに分けても、最後にブランチの先端が指す状態は同じである。
  それなら、レビューする開発者が楽になるように分ける。
- 分けておくと、後で 1 つの変更だけを取り出したり、取り消したり（revert）しやすい。
- ほかの人に送る前に、履歴を書き換える道具を使って、整理された分かりやすい履歴にする。

## コミットメッセージの形

出典: Commit Guidelines

- 1 行目に、変更を簡潔に表す 50 文字程度までの要約を書く。
- 次に空行を 1 行置き、その後に詳しい説明を書く。
- Git プロジェクトは、詳しい説明に「変更の動機」と「前の振る舞いとの違い」を書くよう求めている。
  これは良い指針である。
- メッセージは命令形で書く（「Fix bug」と書き、「Fixed bug」や「Fixes bug」とは書かない）。
  `git merge` や `git revert` が作るメッセージと書き方がそろう。

原典が示す型（Tim Pope の型を少し変えたもの）の要点は次のとおりである。

- 要約は先頭を大文字にし、50 文字以内にする。
- 本文は 72 文字程度で折り返す。
- 要約と本文の間の空行は欠かせない（本文を省く場合を除く）。
  1 行目はメールの件名として扱われることがあり、rebase などの道具は空行が無いと混乱する。
- 段落の間には空行を入れる。
  箇条書きも使ってよい。

## See also

- [Pro Git: Contributing to a Project](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)
- [A Note About Git Commit Messages (Tim Pope)](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
