---
type: reference
title: 'Harness² の要約'
description: 'Google Research が公開した、エージェントのハーネスを再帰的に改良するフレームワーク Harness²（google-research/harness2）の要約。'
tags: [ai, agents, harness, harness-engineering, google-research]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-19T00:00:00Z }
stale_after: 2027-10-19T00:00:00Z
---

# Harness² の要約

Google Research の GitHub リポジトリ [google-research/harness2][repo] の要約。Harness²（ハーネス・スクエア）は、AI エージェントを動かす周りの仕組み（ハーネス）を、モデルの重みを変えずに自動で改良していくフレームワークである。論文「Harness²: Recursive Agent Harnessing for an Open World」（[arXiv:2610.14224][paper]）の実装として公開されている。

- 作者: Ruiyao Xu、Yanfei Chen、Tomas Pfister ほか（Google）
- バージョン: 0.1.0（2026-10-13 時点の main ブランチ）
- ライセンス: Apache 2.0。Google の公式サポート製品ではない。
- 本文書は README、`docs/` 配下の文書、`harness2/core/` のソースコードをもとにした要約である。論文本文は読んでいない。

## 用語: ハーネスとハーネシング

README は 2 つの言葉を次のように定義している。

| 用語                       | 意味                                                                                                           |
| :------------------------- | :------------------------------------------------------------------------------------------------------------- |
| ハーネス（harness）        | モデルをエージェントとして動かすための周りの仕組み。プロンプト、ツール、記憶、スキル、オーケストレーションなど |
| ハーネシング（harnessing） | そのハーネスを最適化する作業                                                                                   |

> 引用: "A **harness** is the system around a model that enables it to act as an agent"

人がプロンプトや `AGENTS.md` を手で直していく作業を、エージェント自身に繰り返させるのが Harness² の狙いである。

## 何を解決しようとしているか

ハーネスは通常、設計時に想定したタスクに合わせて作られる。しかし実際のエージェントは、設計時に見たことがないタスクにも出会う。README はこれを「オープンワールド」と呼ぶ。Harness² は、新しいタスクに出会うたびにそのタスク用にハーネスを改良し、そこで得た教訓を次のタスクに引き継ぐ。

改良には正解データ（ground truth）を使わない。採点結果を見ずに、同じタスクを異なるハーネスで実行した結果の違いを手がかりにする。

## 2 段階の再帰

Harness² の中心は、2 つの階層の再帰（同じ手順の繰り返し）である。

### タスクレベルの再帰: Propose–Probe–Compose

1 つのタスクの中で、実行用のハーネスを改良する。1 ステップは次の 3 段階からなる。

1. Propose（提案）: ハーネスエディタが、ハーネスへの編集案を出す。編集案には、どの分野にも通じる一般的な編集（invariant）と、そのタスクの分野に特化した編集（domain）の 2 種類がある。
1. Probe（試行）: 編集案を当てたハーネスで、同じタスクを実際に実行する。
1. Compose（合成）: 元のハーネスと各候補の実行結果の振る舞いの違い（behavioral contrast）を比べ、良い編集を組み合わせて改良版のハーネスを作る。

提案が不正な形だった場合は 1 回だけ再試行し、それでも駄目なら元のハーネスを引き継ぐ。

### ハーネシングレベルの再帰: 改善用ハーネスの更新

タスクを終えるたびに、採用したハーネスと、実行結果で裏付けられた教訓を保存する。保存先は分野（ドメイン）ごとの経験ライブラリであり、README はこれを改善用ハーネス（improvement harness）と呼ぶ。同じ分野の次のタスクでは、このライブラリを参考にしてハーネスを改良する。

ソースコード上のライブラリの構成は次のとおりである。要約ではなく、採用したハーネスの全体をそのまま保存する。

```text
<root>/<run-tag>/<mode>/<domain>/INDEX.md
<root>/<run-tag>/<mode>/<domain>/harnesses/<task>/harness/...      採用したハーネス全体
<root>/<run-tag>/<mode>/<domain>/harnesses/<task>/EXPERIENCE.md    採用理由と教訓
```

同じ分野のタスクは順番に実行し、それより前のエントリだけを読む。異なる分野は並行して実行できる。

## 編集できる 8 つの構成要素

Harness² が編集の対象にするハーネスの構成要素は 8 つある。ソースコードでは c1〜c8 と呼ばれる。

| 構成要素      | 実行時の役割                         |
| :------------ | :----------------------------------- |
| system prompt | コンテキストを組み立てる             |
| guardrails    | コンテキストを組み立てる             |
| memory        | コンテキストを組み立てる             |
| skills        | コンテキストを組み立てる             |
| tool guidance | ツールの使い方を決める               |
| scripts       | ツールの使い方を決める               |
| subagents     | 作業の委任を指揮する                 |
| plugins       | ツールループの中の振る舞いを制御する |

OpenCode 用の実装では、`systemprompt.md`、`guardrails.md`、`LongTermMEMORY.md`、`tool_descriptions/tool_guidance.md` の 4 ファイルを常に読み込む。この 4 ファイルの合計は 24,000 文字までに制限されている。ソースコードのコメントは、ここに書く量がエージェント自身の出力に使える量を圧迫するためと説明している。スキルは `skills/` に置き、使う場面を system prompt か guardrails に書いて呼び出させる。

編集案は変更する部分だけを出し、出さなかった部分は元のまま引き継ぐ（omitted-is-inherited）。

## 再帰の広げ方: 並列と逐次

予算 `k` を増やすと、タスクレベルの再帰を 2 通りに広げられる。

| モード             | 動き                                                                                      | 性質         |
| :----------------- | :---------------------------------------------------------------------------------------- | :----------- |
| 並列（parallel）   | 一般的な候補と分野特化の候補を `k` 個ずつ試し、共有した実行結果から `k` 個の合成を作る    | 広く探索する |
| 逐次（sequential） | 改良したハーネスと蓄積した実行結果を次に持ち越し、Propose–Probe–Compose を `k` 回繰り返す | 深く磨き込む |

どちらのモードも、1 タスクあたり実行（rollout）を 4k 回、改良の段階を 3k 回使う。

## 成果

README によれば、3 つの業務系ベンチマークと 4 つのモデル・ハーネスの組み合わせで評価した。Harness² を 1 ステップ当てるだけで、GLM-5 と Gemini 3.5 Flash の成績が元のハーネスより上がった。

| ベンチマーク    | 内容                      | 最大の改善幅                         |
| :-------------- | :------------------------ | :----------------------------------- |
| WorkBuddy-Bench | オフィス作業、Web、コード | 11.5 ポイント                        |
| JobBench        | 専門職の業務              | 4.5 ポイント                         |
| LAB             | 法務の業務                | 部分合格率で 11.8 パーセントポイント |

再帰の予算 `k` を増やすと、さらに成績が上がったとしている。

## 実装の構成

Python 3.12 以上で書かれている。設計は「手法」「実行基盤」「ベンチマーク」の 3 つを互いに独立させている。

| 軸                        | 役割                                                               | 主なディレクトリ       |
| :------------------------ | :----------------------------------------------------------------- | :--------------------- |
| 手法（method）            | 再帰、プロンプト、選択、経験ライブラリ                             | `harness2/core/`       |
| 実行基盤（substrate）     | エージェントを実際に動かすフレームワーク。OpenCode（既定）と Codex | `harness2/substrate/`  |
| ベンチマーク（benchmark） | タスクの定義と読み込み                                             | `harness2/benchmarks/` |

ソースコードには、手法が採点に頼らないための仕組みがいくつかある。

- 手法側が受け取る実行結果の型 `RunView` は、点数を持たない。
- 採点を行う `judge.py` は、手法側のどこからも import されない。採点は、選択が終わったあとに別コマンドで行う。
- ベンチマーク固有の説明文に benchmark、rubric、score などの語が入っていると、エラーで止まる。説明文には測り方ではなく作業の内容を書かせる。

## 使い方の概要

Linux、Python 3.12、uv を使う。モデルの認証が要らないデモから試せる。

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[render]'
harness2-demo --output runs/demo --k 2
```

モデルを使うベンチマークの実行には、Node.js 20 以上、Google Cloud CLI（Vertex AI 経由でモデルを呼ぶ）、ベンチマークごとの依存が必要である。実行、採点、集計は別々のコマンドに分かれている。

| コマンド          | 役割                     |
| :---------------- | :----------------------- |
| `harness2-setup`  | ベンチマークを導入する   |
| `harness2-check`  | 導入状態を確かめる       |
| `harness2`        | ハーネスの改良を実行する |
| `harness2-judge`  | 選ばれた出力を採点する   |
| `harness2-report` | 結果を集計する           |

モデルを使う実行には API の費用がかかる。README は、小さなタスク選択から始めるよう勧めている。

## 注意点

- エージェントのネットワークアクセスは制限されておらず、Codex はサンドボックスを無効にして動く。
- ベンチマークは公開されており、採点基準もネット上にある。検証中に、Codex が指示されていないのに JobBench の採点基準をダウンロードした例が報告されている。評価の前に、ファイアウォールや DNS で Hugging Face や GitHub への通信を止めるよう求めている。

## See also

- [google-research/harness2（GitHub）][repo]
- [Harness²: Recursive Agent Harnessing for an Open World（arXiv）][paper]
- [harness2.github.io](https://harness2.github.io)

[repo]: https://github.com/google-research/harness2
[paper]: https://arxiv.org/abs/2610.14224
