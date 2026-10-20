---
type: reference
title: 'Documenting Architecture Decisions 要約'
description: 'Michael Nygard の記事「Documenting Architecture Decisions」の要約（ADR を書く理由、対象にする決定、形式、番号と置き換えの扱い）。'
tags: [documentation, adr, architecture, decision]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Documenting Architecture Decisions 要約

Michael Nygard が 2011 年に Cognitect のブログで公開した記事「Documenting Architecture Decisions」の要約である。
外部資料の要約であり、最終的な根拠は原典を参照すること。
ADR（Architecture Decision Record）という書き方を提案した記事である。
要点は「重要な決定を 1 つずつ短いファイルに残し、未来の開発者が理由を知って判断できるようにする」の 1 つである。
記事そのものも ADR の形式（Context、Decision、Status、Consequences）で書かれている。

## ADR を書く理由

出典: Context

- アジャイルなプロジェクトでは、決定は一度にまとめては行われず、プロジェクトの途中で少しずつ行われる。
- 大きな文書は更新されず、読まれもしない。
  小さく分かれた文書なら、更新される見込みがあり、誰にとっても読みやすい。
- プロジェクトで最も追いにくいものの 1 つは、決定の動機である。
  理由や結果を知らない新しいメンバーには、2 つの選択肢しかない。
  1. 盲目的に受け入れる。
     状況が変わって見直すべき決定まで残り、変えるのが怖くなってプロジェクトが重みで崩れる。
  1. 盲目的に変える。
     まだテストされていない非機能要件を支えていた決定などを、気づかずに壊すおそれがある。
- どちらも避けるために、決定の理由と結果を残す。

## ADR の対象と置き方

出典: Decision

- 対象は「アーキテクチャ上重要な」決定である。
  構造、非機能の特性、依存関係、インターフェース、作り方の技法に影響する決定を指す。
- ADR は短いテキストファイルで、1 つの決定と、その決定が応えた力（状況や制約）を書く。
  中心は決定なので、同じ力が複数の ADR に出てきてもよい。
- プロジェクトのリポジトリの `doc/arch/adr-NNN.md` に、Markdown のような軽い書式で置く。
- 番号は連番で振り、再利用しない。
- 決定が覆っても、古い ADR は消さずに「置き換えられた（superseded）」と記す。
  「かつての決定だったが、今の決定ではない」ことにも意味があるためである。

## ADR の形式

出典: Decision

| 節 | 書くこと |
| :-- | :-- |
| Title | 短い名詞句（例: 「ADR 9: LDAP for Multitenant Integration」） |
| Context | 働いている力（技術、政治、社会、プロジェクト固有の事情）。互いに引っ張り合う力は、そうと書く。価値判断を入れず事実だけを書く |
| Decision | 力への対応。完全な文で、能動態で書く（「We will …」） |
| Status | 合意前は proposed、合意後は accepted。後の ADR で変わったら deprecated か superseded とし、置き換えた ADR を示す |
| Consequences | 決定を適用した後の状況。良い結果だけでなく、悪い結果も中立の結果もすべて書く |

- 全体で 1〜2 ページに収める。
- 未来の開発者との会話のつもりで、段落にまとめた完全な文で書く。
  箇条書きは見た目のためだけに使い、文の断片を並べる言い訳にしない。

## ADR を使った結果

出典: Consequences / Experience Report

- 1 つの ADR の結果は、後の ADR の背景になりやすい。
  大きな決定が、小さな決定の入る余地を作る。
- メンバーが入れ替わっても、過去の決定の動機が見える。
  「何を考えてこうしたのか」と頭を抱える人がいなくなり、状況が変われば見直す時期も分かる。
- 記事の時点で、6〜10 人の開発者が ADR を使うプロジェクトを経験し、全員が得られる背景の多さを評価した。
- 将来の大きな作り直しの意図を書き残すと、その変更をうっかり難しくすることを防げた。
- 開発者以外の人には、バージョン管理の中の文書は見にくいという反論がありうる。
  実際には GitHub が Markdown を表示するので、wiki と同じように読めた。

## See also

- [Documenting Architecture Decisions (Cognitect)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
