---
type: reference
title: 'autonomous-coding の要約'
description: 'Anthropic の claude-quickstarts リポジトリにある autonomous-coding の要約で、初期化エージェントとコーディングエージェントの 2 段構成で、何セッションもかけてアプリを作らせる最小のハーネスの仕組みと、Bash コマンドを許可リストで絞る安全対策を説明する。'
tags: [claude, agent, harness, long-running, agent-sdk, security, quickstart]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-29T00:00:00Z }
stale_after: 2027-10-29T00:00:00Z
---

# autonomous-coding の要約

Anthropic の GitHub リポジトリ [anthropics/claude-quickstarts][repo] にある [autonomous-coding][dir] の要約。
Claude Agent SDK を使い、記憶を持たないセッションを何度もつないで 1 つのアプリを作らせる、最小のハーネスのデモである。
エンジニアリングブログの記事「Effective harnesses for long-running agents」で説明された 2 段構成を、そのまま動くコードにしたものにあたる。

- 対象: 2026-10-29 時点の main ブランチ（コミット `1a18c34`）
- 言語: Python。依存は `claude-code-sdk>=0.0.25` だけで、Claude Code の CLI も必要
- ライセンス: README には「Internal Anthropic use.」と書かれている
- 本文書は README、Python のソースコード、`prompts/` のプロンプトをもとにした要約である

[repo]: https://github.com/anthropics/claude-quickstarts
[dir]: https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding

## 全体の流れ

`autonomous_agent_demo.py` を実行すると、次のループが回る。

1. プロジェクトのディレクトリに `feature_list.json` がなければ初回とみなし、アプリの仕様 `prompts/app_spec.txt` をディレクトリへ写す。
1. セッションごとに新しいクライアントを作る。コンテキストは毎回空から始まる。
1. 初回だけ初期化用のプロンプトを、2 回目からはコーディング用のプロンプトを送る。
1. セッションが終わったら `feature_list.json` を数えて進捗を表示し、3 秒待って次のセッションへ進む。
   エラーで終わったときも、新しいセッションでやり直す。

ループは `--max-iterations` に達するか、Ctrl+C で止めるまで続く。
同じコマンドをもう一度実行すれば、`feature_list.json` があるので続きから再開する。

| オプション         | 意味                     | 既定値                       |
| ------------------ | ------------------------ | ---------------------------- |
| `--project-dir`    | 作るアプリのディレクトリ | `./autonomous_demo_project`  |
| `--max-iterations` | セッションの最大回数     | 無制限                       |
| `--model`          | 使うモデル               | `claude-sonnet-4-5-20250929` |

相対パスを渡すと、`generations/` の下に置かれる。

## 2 種類のエージェント

2 つのエージェントは、システムプロンプト、ツール、設定が同じで、最初に送るプロンプトだけが違う。

| エージェント             | 動く回数                  | プロンプト                      |
| ------------------------ | ------------------------- | ------------------------------- |
| 初期化エージェント       | 最初のセッションで 1 回   | `prompts/initializer_prompt.md` |
| コーディングエージェント | 2 回目以降の毎セッション  | `prompts/coding_prompt.md`      |

### 初期化エージェントの仕事

1. `app_spec.txt` を読む。
1. `feature_list.json` に、200 件以上の E2E テストケースを書く。
   各テストは分類（`functional` か `style`）、説明、手順、`passes` を持ち、`passes` はすべて `false` で始める。
   10 手順以上のテストを 25 件以上入れ、重要な機能から順に並べる。
1. 依存の導入とサーバーの起動を行う `init.sh` を書く。
1. git リポジトリを作り、最初のコミットをする。
1. 仕様に沿ってディレクトリ構成を作る。時間が残れば実装を始めてもよい。
1. 終わる前に、やったことを `claude-progress.txt` に書く。

プロンプトは、以後のセッションで機能を消したり書き換えたりすることを「CATASTROPHIC」と強く禁じている。
変えてよいのは `passes` を `true` にすることだけである。

### コーディングエージェントの仕事

`coding_prompt.md` は、毎セッションの手順を 10 段階で決めている。
詳しくは [autonomous-coding のコーディング用プロンプト](autonomous-coding-coding-prompt.md) にまとめている。

1. 状況をつかむ。`pwd`、`ls`、`app_spec.txt`、`feature_list.json`、`claude-progress.txt`、`git log` を読み、未完了のテストを数える。
1. `init.sh` でサーバーを起動する。
1. 新しい作業の前に、完了済みの中から中心となる機能を 1〜2 件確かめる。
   壊れていれば `passes` を `false` に戻し、新しい機能より先に直す。
1. `passes` が `false` の中で最も優先度の高い機能を 1 つ選ぶ。
1. 実装する。
1. ブラウザ操作で確かめる。
1. 確かめたあとで、`passes` だけを書き換える。
1. git にコミットする。
1. `claude-progress.txt` を更新する。
1. コミットされていない変更がなく、アプリが動く状態でセッションを終える。

確認はすべて Puppeteer の MCP サーバーを通したブラウザ操作で行う。
人と同じようにクリックや入力で操作し、スクリーンショットで見た目も確かめる。
`curl` だけの確認や、JavaScript の実行で UI を飛ばすことは禁じている。

1 セッションで 1 機能だけでもよいと明記し、一度に多くをやってコンテキストを使い切る失敗を防いでいる。

## セッションをまたいで残るもの

アプリのディレクトリには、次のファイルが残る。

| ファイル                | 役割                                                 |
| ----------------------- | ---------------------------------------------------- |
| `feature_list.json`     | テストケースの一覧。何が終わったかの唯一の基準       |
| `app_spec.txt`          | アプリの仕様                                         |
| `init.sh`               | 環境を用意してサーバーを起動するスクリプト           |
| `claude-progress.txt`   | セッションごとの進捗メモ                             |
| `.claude_settings.json` | ハーネスが書き出す安全設定                           |
| git の履歴              | 各セッションの変更。次のセッションが最初に読む       |

ハーネス側の Python は、進捗を数えるとき以外にこれらのファイルを読まない。
次に何をするかは、エージェントがファイルを読んで自分で決める。

## 安全対策

`client.py` と `security.py` で、3 段の防御（多層防御）をかけている。

| 段階                   | 仕組み                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| OS のサンドボックス    | 設定の `sandbox.enabled` を有効にし、Bash コマンドを隔離した環境で動かす                   |
| ファイル操作の制限     | 作業ディレクトリをアプリのディレクトリにし、`Read(./**)` などでその中だけを許可する         |
| Bash コマンドの許可リスト | `PreToolUse` フックで、許可リストにないコマンドを止める                                 |

許可リスト `ALLOWED_COMMANDS` に入っているのは次のコマンドである。

- ファイルを見る: `ls`、`cat`、`head`、`tail`、`wc`、`grep`
- ファイル操作: `cp`、`mkdir`、`chmod`
- その他: `pwd`、`npm`、`node`、`git`、`ps`、`lsof`、`sleep`、`pkill`、`init.sh`

このうち 3 つは、許可リストに入っていても引数をさらに調べる。

| コマンド  | 追加の条件                                                    |
| --------- | ------------------------------------------------------------- |
| `pkill`   | 止めてよいのは `node`、`npm`、`npx`、`vite`、`next` だけ       |
| `chmod`   | `+x`、`u+x` のような実行権の付与だけ。フラグは使えない         |
| `init.sh` | `./init.sh` か、`/init.sh` で終わるパスだけ                   |

フックは、`&&`、`||`、`;`、`|` でつないだコマンドを分け、それぞれのコマンド名を調べる。
引用符が閉じていないなどで解析できないときは、止める側に倒す（fail-safe）。
フックの動きを確かめるテストが `test_security.py` にある。

## 付属のアプリ仕様

`prompts/app_spec.txt` は、claude.ai のクローンを作る仕様である。
React と Vite、Tailwind CSS のフロントエンドに、Node.js と Express、SQLite のバックエンドを組み合わせる。
チャット、Artifact の表示、会話の管理、プロジェクトなどの機能と、データベースの表、API の一覧が XML 風のタグで書かれている。
別のアプリを作らせたいときは、このファイルを書き換える。

## 時間の目安

- 初回のセッションは、200 件のテストケースを書くので数分以上かかる。止まって見えても動いている。
- 2 回目以降は、1 セッションに 5〜15 分ほどかかる。
- 200 件をすべて終えるには、合わせて何時間もかかる。

短く試したいときは、`initializer_prompt.md` の「200」を 20〜50 などに減らすよう README は勧めている。

## 読んでいて気づいた点

- 依存の名前は `claude-code-sdk` で、`ClaudeCodeOptions` を使っている。
  これは Claude Agent SDK に改名される前の名前であり、今の SDK で動かすときは読み替えが要る可能性がある。
- 既定のモデルは `claude-sonnet-4-5-20250929` で、新しいモデルを使うには `--model` で指定する。
- エージェントの出力の表示では、ツールの結果に「blocked」という文字があるかどうかで、フックに止められたかを判断している。
  これは表示のためだけで、止める判断はフックが行う。

## See also

- [autonomous-coding（GitHub）][dir]
- [autonomous-coding のコーディング用プロンプト](autonomous-coding-coding-prompt.md)
- [長時間動くエージェントのための効果的なハーネス](/references/claude/engineering/effective-harnesses-for-long-running-agents.md)
