---
type: reference
title: 'autonomous-coding のコーディング用プロンプト'
description: 'claude-quickstarts の autonomous-coding で、2 回目以降の毎セッションに送るプロンプト coding_prompt.md の要約で、記憶のない状態から状況をつかみ、1 機能を実装してブラウザで確かめ、きれいな状態で終えるまでの 10 段階の手順と、その書き方の工夫を説明する。'
tags: [claude, agent, harness, long-running, prompt, testing, quickstart]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-29T00:00:00Z }
stale_after: 2027-10-29T00:00:00Z
---

# autonomous-coding のコーディング用プロンプト

claude-quickstarts の autonomous-coding にあるプロンプト [coding_prompt.md][prompt] の要約。
ハーネスは、2 回目以降のセッションの始めに、このプロンプトだけをユーザーメッセージとして送る。
システムプロンプトは「You are an expert full-stack developer building a production-quality web application.」の 1 文しかないので、エージェントの毎セッションの動き方は、ほぼこのプロンプトで決まる。

- 対象: 2026-10-29 時点の main ブランチ（コミット `1a18c34`）。197 行の Markdown
- ハーネス全体の仕組みは [autonomous-coding の要約](autonomous-coding.md) にまとめている

[prompt]: https://github.com/anthropics/claude-quickstarts/blob/main/autonomous-coding/prompts/coding_prompt.md

## 全体の構成

プロンプトは 4 つの部分からなる。

| 部分                    | 中身                                                         |
| ----------------------- | ------------------------------------------------------------ |
| YOUR ROLE - CODING AGENT | 役割と、10 段階の手順（STEP 1〜10）                         |
| TESTING REQUIREMENTS    | 確認に使うブラウザ操作のツールと、使い方の決まり             |
| IMPORTANT REMINDERS     | 全体の目標、このセッションの目標、優先順位、品質の基準       |
| 最後の 1 行             | 「Begin by running Step 1 (Get Your Bearings).」             |

冒頭で、エージェントに次の前提を伝えている。

> 引用: "This is a FRESH context window - you have no memory of previous sessions."

記憶がないことを最初に言い切ることで、前のセッションの内容を思い込みで補わず、ファイルを読んで状況をつかむように促している。

## 10 段階の手順

### STEP 1: 状況をつかむ（必須）

次の 7 つのコマンドを、そのまま書いて実行させる。

```bash
pwd
ls -la
cat app_spec.txt
cat feature_list.json | head -50
cat claude-progress.txt
git log --oneline -20
cat feature_list.json | grep '"passes": false' | wc -l
```

作業場所、ファイル構成、仕様、機能一覧の先頭、前回までの進捗メモ、最近のコミット、残りのテスト数の順に読む。
中でも `app_spec.txt` を読むことが欠かせないと念を押している。

使うコマンドは、どれもハーネスの Bash の許可リストに入っているものである。

### STEP 2: サーバーを起動する

`init.sh` があれば `chmod +x init.sh` のあとに `./init.sh` を実行する。
なければ手でサーバーを起動し、その手順を記録する。

### STEP 3: 前回の作業を確かめる（必須）

新しい作業の前に、`passes` が `true` の機能のうち、アプリの中心となるものを 1〜2 件テストし直す。
チャットアプリなら、ログインしてメッセージを送り、返事を受け取るテストを例に挙げている。

問題を見つけたら、次のように扱う。

- その機能の `passes` をすぐに `false` に戻す。
- 問題を一覧にし、新しい機能より先にすべて直す。

見落としやすい見た目の不具合として、次の例を並べている。
白地に白い文字などのコントラスト不足、意味のない文字の表示、間違った時刻、レイアウトの崩れやはみ出し、近すぎるボタン、ホバー時の表示がないこと、コンソールのエラー。

### STEP 4: 実装する機能を 1 つ選ぶ

`feature_list.json` の中で、`passes` が `false` のうち最も優先度の高いものを選ぶ。

> 引用: "It's ok if you only complete one feature in this session, as there will be more sessions later that continue to make progress."

1 セッションで 1 機能だけでよいと明記して、一度に多くをやろうとする失敗を防いでいる。

### STEP 5: 実装する

コードを書き、ブラウザで確かめ、見つけた問題を直し、最初から最後まで動くことを確かめる。

### STEP 6: ブラウザ操作で確かめる

機能は必ず実際の UI を通して確かめる。

| する                                   | しない                                       |
| -------------------------------------- | -------------------------------------------- |
| クリックとキーボード入力で UI を操作する | `curl` だけで確かめる                        |
| スクリーンショットで見た目を確かめる   | JavaScript の実行で UI を飛ばす              |
| ブラウザのコンソールのエラーを見る     | 見た目の確認を省く                           |
| 利用者の一連の操作を通しで確かめる     | 十分に確かめずに `passes` にする             |

### STEP 7: `feature_list.json` を更新する

書き換えてよいのは `passes` の 1 項目だけで、スクリーンショットで確かめたあとに限る。
テストの削除、説明や手順の書き換え、テストの統合、並べ替えは禁じている。

### STEP 8: コミットする

コミットメッセージのひな形を示している。
件名に機能名と「verified end-to-end」を書き、本文に変更内容、ブラウザで確かめたこと、`passes` にしたテストの番号を書く。

### STEP 9: 進捗メモを更新する

`claude-progress.txt` に次のことを書く。
このセッションでやったこと、終えたテスト、見つけた問題と直した問題、次にやるべきこと、全体の完了状況（例: 「45/200 tests passing」）。

### STEP 10: きれいな状態で終える

コンテキストが埋まる前に、次のことを済ませる。

1. 動くコードをすべてコミットする。
1. `claude-progress.txt` を更新する。
1. 確かめたテストがあれば `feature_list.json` を更新する。
1. コミットされていない変更を残さない。
1. アプリを動く状態のままにする（壊れた機能を残さない）。

## 確認に使うツール

TESTING REQUIREMENTS では、Puppeteer の MCP サーバーのツールを挙げている。

| ツール                | 用途                                       |
| --------------------- | ------------------------------------------ |
| `puppeteer_navigate`  | ブラウザを起動して URL を開く              |
| `puppeteer_screenshot` | スクリーンショットを撮る                  |
| `puppeteer_click`     | 要素をクリックする                         |
| `puppeteer_fill`      | フォームに入力する                         |
| `puppeteer_evaluate`  | JavaScript を実行する。デバッグのときだけ使う |

人と同じようにマウスとキーボードで操作し、JavaScript の実行で近道をしないよう重ねて求めている。

## 最後の念押し

IMPORTANT REMINDERS は、目標を 2 つの大きさで分けて書いている。

| 項目               | 内容                                                       |
| ------------------ | ---------------------------------------------------------- |
| 全体の目標         | 200 件以上のテストがすべて通る、本番品質のアプリ           |
| このセッションの目標 | 少なくとも 1 機能を完璧に仕上げる                        |
| 優先順位           | 新しい機能より、壊れたテストを直すのが先                   |
| 品質の基準         | コンソールのエラーがない、仕様どおりの UI、UI を通して動く、速い |

最後に、時間は無制限にあるので正しく仕上げること、そしてセッションを終える前にコードをきれいな状態にすること（STEP 10）が最も大事だと書いて締めている。

## 書き方の工夫

ここからは、プロンプトを読んで本文書の筆者が読み取ったことである。プロンプト自身が説明しているわけではない。

- 手順に番号を振り、STEP 1 から始めるよう最後の 1 行で指示している。毎回同じ順で動かすためである。
- STEP 1 はやり方を言葉で説明せず、実行するコマンドをそのまま書いている。
- 重要な指示には「MANDATORY」「CRITICAL」「NEVER」などの強い言葉と太字を使っている。
- `passes` 以外を書き換えない決まりを、STEP 7 で 2 回、初期化用のプロンプトでも 1 回書いている。
- 「時間は無制限にある」「1 機能だけでもよい」と書いて、急いで多くをやろうとする動機を取り除いている。

各段階は、エンジニアリングブログの記事が挙げた失敗に対応している。

| 記事が挙げた失敗                       | 対応する段階            |
| -------------------------------------- | ----------------------- |
| 一度に多くをやり、作りかけのまま尽きる | STEP 4、STEP 10         |
| 早すぎる段階で「完成」と宣言する       | STEP 1 の残りテストの数え上げ、STEP 7 |
| 前のセッションの不具合が残る           | STEP 3                  |
| テストせずに機能を完了にする           | STEP 6、STEP 7          |
| アプリの起動方法を調べるのに時間がかかる | STEP 2                |

## 読んでいて気づいた点

- STEP 8 のひな形には「Screenshots in verification/ directory」とあるが、`verification/` に保存するよう指示している段階はない。
- 「Don't use the puppeteer "active tab" tool.」とあるが、ハーネスが許可しているツールの中にそれらしいものはない。
  ハーネスは `puppeteer_select` と `puppeteer_hover` も許可しているが、プロンプトのツール一覧には載っていない。
- 残りのテストを数えるコマンドは、`"passes": false` という書き方（コロンのあとに空白 1 つ）にだけ一致する。
  `feature_list.json` の整形が違うと、正しく数えられない。

## See also

- [coding_prompt.md（GitHub）][prompt]
- [autonomous-coding の要約](autonomous-coding.md)
- [長時間動くエージェントのための効果的なハーネス](/references/claude/engineering/effective-harnesses-for-long-running-agents.md)
