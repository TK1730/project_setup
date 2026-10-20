---
type: reference
title: 'migrate-to-e2e スキルの要約'
description: 'TesterArmy の e2e リポジトリが配布するエージェントスキル migrate-to-e2e の中身、インストール先、前提条件、エージェントに指示する操作の要約。'
tags: [ai, agent, skills, e2e, testing, playwright, migration, security]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-18T00:00:00Z }
stale_after: 2027-10-18T00:00:00Z
---

# migrate-to-e2e スキルの要約

`migrate-to-e2e` は、既存の E2E テスト（Playwright、Cypress、Selenium、Detox、Maestro）を、TesterArmy が作る OSS のテストフレームワーク `e2e` へ少しずつ移すための、コーディングエージェント向けスキルである。移行元のテストスイートがあることが前提で、テストが無いプロジェクトに新しく E2E テストを作るスキルではない。

この要約は、GitHub の [tester-army/e2e](https://github.com/tester-army/e2e) をコミット `ef977f4856da009cac26d78d2e9bb14e5991ee41`（2026-10-17）の時点で読んで書いた。インストールの挙動は、npm パッケージ `skills` 1.7.2 のリポジトリ [vercel-labs/skills](https://github.com/vercel-labs/skills) をコミット `13e4063a1cf913f5606d57d42ab83a86f5001e04` の時点で読んで書いた。どちらも実行はしていない。

## migrate-to-e2e が行うこと

1 回のセッションで 1 つの区切り（slice、1〜5 件程度のテスト）だけを移し、古いスイートと新しいスイートの両方が通る状態で終える。古いテストは、ユーザーが確認するまで消さない。進み具合は `MIGRATION.md` に記録し、次のセッションはそこから再開する。

スキルの手順は次の 9 段階である（`skills/migrate-to-e2e/SKILL.md` の見出しに対応する）。

1. 再開か新規か: `MIGRATION.md` を探し、あれば中身をリポジトリと突き合わせてから続きをする。
1. 棚卸し（初回）: 移行元のランナー、テストの数とアサーションの数、共有コード、CI での動かし方、e2e の置き場所を調べ、`MIGRATION.md` を作る。
1. ハーネスの用意（1 回だけ）: `npx e2e init --yes` で設定ファイルを作り、アプリの起動方法を移し、最も単純なテストを 1 件移して通す。
1. 区切りの選択: どのテストを移すかをユーザーに聞く。
1. 移植: 共有ヘルパーを先に移し、テストを 1 件ずつ移行ガイドの対応表どおりに書き換える。
1. 検証: `npx e2e run <file> --repeat-each 3` で 3 回中 3 回通ることを確かめ、アサーションの数が元より減っていないことを確かめる。任意で、アプリにわざとバグを入れて両方のスイートが落ちるかを見る（Defect check）。
1. 両スイートの並走: 古いテストはユーザーの確認後にだけ消す。CI への追加も、ユーザーの同意を得てから行う。
1. 進捗ファイルの更新: `MIGRATION.md` をその都度更新する。
1. 引き継ぎ: 移したテスト、結果、作成・変更したファイルをユーザーに報告する。

移行元の見分け方は、スキルの表で決まっている。

| 移行元     | 見分け方                                                     | 移行先のエンジン |
| :--------- | :----------------------------------------------------------- | :--------------- |
| Playwright | `playwright.config.*`、`@playwright/test`                    | web              |
| Cypress    | `cypress.config.*`、`cypress/` ディレクトリ                  | web              |
| Selenium   | `selenium-webdriver`、`pom.xml` などに書かれた Selenium      | web              |
| Detox      | `.detoxrc*`、`package.json` の `detox`                       | mobile           |
| Maestro    | `appId:` と `---` で始まる YAML、`.maestro/`、`maestro test` | mobile           |

WebdriverIO と Appium には移行ガイドが無く、Selenium、Detox、Maestro のガイドで部分的に読み替える、とスキルに書かれている。

## migrate-to-e2e を構成するファイル

スキル本体は `skills/migrate-to-e2e/SKILL.md`（324 行）の 1 ファイルだけで、スクリプトや `references/` は持たない。

- `skills/migrate-to-e2e/SKILL.md`: Frontmatter の `name` と `description` と、上の手順。
- `plugins/e2e/skills/migrate-to-e2e/`: Claude Code と Codex のプラグイン用の写し。`SKILL.md` は同じ内容で、Codex の画面表示用の `agents/openai.yaml` が 1 つ増える。`openai.yaml` は `allow_implicit_invocation: true`（明示的に呼ばなくても使われうる）を指定している。

スキルは、手順の大半を次の 2 つの資料に任せ、エージェントに読ませる。

- `e2e` スキル: `skills/e2e/SKILL.md` と `skills/e2e/references/`。テストの書き方、設定、実行、デバッグを説明する。`npx e2e guide <topic>` でも読める。
- 移行ガイド: `docs/migrate/playwright.mdx` など移行元ごとの文書。`e2e` パッケージを入れると `node_modules/e2e/docs/` にも入る。Web 上では `https://e2e.tester.army/docs/migrate/<移行元>.md` にある。

`--skill migrate-to-e2e` を付けて入れると、この 2 つの資料は入らない。`e2e` スキルは、別に `npx skills add tester-army/e2e`（スキルを指定しない）で入れるか、`npx e2e init` で入る。

## migrate-to-e2e のインストールと呼び出し

公式文書（`docs/coding-agents.mdx` の「Migrate an existing suite」）のインストールコマンドは次のとおりである。

```bash
npx skills add tester-army/e2e --skill migrate-to-e2e
```

pnpm なら `pnpm dlx skills add tester-army/e2e --skill migrate-to-e2e` と書く。

`skills` CLI がファイルを置く場所は、README とソースコード（`src/installer.ts`、`src/agents.ts`、`src/local-lock.ts`）から次のように読み取れる。

- 既定はプロジェクト単位で、`-g` を付けるとユーザーのホームディレクトリに入る。
- 実体（canonical copy）は `.agents/skills/migrate-to-e2e/` に置く。Codex、Cursor、Gemini CLI、GitHub Copilot、Antigravity などはこの場所をそのまま読む。
- Claude Code のように専用の場所を使うエージェントには、`.claude/skills/migrate-to-e2e/` に実体へのシンボリックリンクを作る。`--copy` を付けるとリンクではなくコピーになる。
- 対象のエージェントは、`-a` で指定しなければ、インストール済みのエージェントを検出して対話で選ばせる。
- プロジェクト直下の `skills-lock.json` に、入れたスキルの出所とハッシュを追記する。
- リポジトリには `skills/migrate-to-e2e/` と `plugins/e2e/skills/migrate-to-e2e/` の 2 つがあるが、CLI は `skills/` を先に探し、同じ名前の 2 つ目を飛ばす（`src/skills.ts`）。このため `openai.yaml` は入らないと読める。実行しての確認はしていない。

入れたあとは、エージェントに `/migrate-to-e2e` と頼むか、「テストを e2e に移して」のように頼む。スキルの `description` には、`e2e` の設定と古いスイートが両方あるプロジェクトで使う、とも書かれている。

## migrate-to-e2e を使う前提条件

- Node.js と npm（`npx`）。`e2e` 本体は npm パッケージ `e2e`（Apache-2.0、調査時点で 0.21.2）で、Web のテストには `@e2e-dev/web` を使う。
- 移行元のテストスイート。古いスイートをその環境で動かせると、移植したテストと結果を比べられる。
- AI モデルは必須ではない。そのまま書き換えた（literal port）テストはモデル無しで動く、とスキルに書かれている。`agent.act` などのエージェントの手順を使うときだけ、モデルの設定が要る。
- モデルは利用者が自分で用意する。ChatGPT、GitHub Copilot、OpenCode Console、SuperGrok のサブスクリプション、各社の API キー（`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`AI_GATEWAY_API_KEY` など）、ローカルモデルのいずれかである（`docs/models.mdx`、`docs/subscriptions.mdx`）。
- TesterArmy の有料プラットフォームのアカウントは、文書を読んだ範囲では求められていない。README は、TesterArmy が別に有料の「agentic testing platform」を運営していると書くだけである。料金体系は確認していない。

## migrate-to-e2e がエージェントに指示する操作

ここからは、スキルの安全性を確かめるための整理である。スキルの文章は英語なので、該当箇所を原文のまま引用する。

### エージェントが実行するコマンド

| コマンド                                       | 目的                                              |
| :--------------------------------------------- | :------------------------------------------------ |
| `npx e2e init --yes`                           | 設定ファイルと例のテストを作る                    |
| `npx playwright test --list`、`npx e2e list`   | 両ランナーのテストの数え上げ                      |
| `npx e2e run <file> --repeat-each 3`           | 移植したテストを 3 回実行する                     |
| `npx e2e mcp`                                  | 動いているアプリを MCP 経由で見てロケーターを探す |
| 移行元の CI と同じ起動コマンド                 | DB やモックサーバーなどの依存を起動する           |
| `git checkout -- <file>`、`git diff -- <file>` | Defect check で入れたバグを戻し、戻ったか確かめる |
| `npx e2e feedback ... --dry-run`               | e2e チームへの報告の下書き                        |

`npx e2e init` は `package.json` に `test:e2e` スクリプトを足す。Playwright の移行ガイドの手順には「Install dependencies.」とあり、依存パッケージのインストールも行う。

### エージェントが書くファイル

- `MIGRATION.md`（e2e の設定ファイルの隣か、リポジトリの最上位）
- `e2e.config.ts`
- `tests/**/*.e2e.ts`（移植したテスト）と `tests/support/` などのヘルパー（`.ts`）
- `package.json` のスクリプト
- ユーザーが同意した場合だけ: CI のワークフロー、古いテストやヘルパーの削除、Defect check のためのアプリのコード（同じセッションで戻す）

アプリのコードは変えない、という規則がある。

> 引用: "Do not change app code."

アプリに無いテスト ID が要るテストは、`agent.act` か別のロケーターで書き、アプリの変更はユーザーに提案するにとどめる。ただし Defect check は例外で、手順 6 で入れたバグは同じセッションで戻す。バグを入れる条件は次のとおりである。

> 引用: "With the user's agreement, plant a small bug in an end state the source asserts (a checkout showing the wrong total), in a file with no uncommitted changes."

戻すときは、そのファイルだけを `git checkout -- <file>` で戻してビルドし直し、`git diff -- <file>` が空になったことを確かめる、とスキルに書かれている。

`git checkout -- <file>` は、そのファイルの未コミットの変更を消す。スキルは「未コミットの変更が無いファイルに入れる」と条件を付けているが、エージェントが条件を見落とすと作業中の変更が消える。

### 外部へ送るデータ

- モデルの提供元: エージェントの手順（`agent.act` など）を使うと、設定したモデルの API を呼ぶ。画面の情報を渡すと考えられるが、送る内容の詳細は確認していない。
- e2e の利用統計: `e2e` CLI は、既定で匿名の利用統計を PostHog（`https://eu.i.posthog.com`、`packages/e2e/src/telemetry/posthog.ts`）へ送る。文書は、テストやアプリの中身、認証情報は送らないと説明している。`E2E_TELEMETRY_DISABLED=1`、`DO_NOT_TRACK=1`、`npx e2e telemetry disable` で止められる（`docs/telemetry.mdx`）。
- e2e チームへの報告: e2e の機能が足りないとき、スキルは `npx e2e feedback` での報告を勧める。送り先は同じ PostHog である（`packages/e2e/src/cli/feedback.ts`）。

  > 引用: "offer to send `npx e2e feedback --type feature -m "<the gap>"` once: preview it with `--dry-run` and send it only when the user agrees"

- `skills` CLI の利用統計: インストール時に `https://www.skills.sh/tele/t` へ利用統計を、公開リポジトリなら `https://www.skills.sh/tele/audit` へ安全性の監査の問い合わせを送る。`DISABLE_TELEMETRY=1` か `DO_NOT_TRACK=1` で止められる（`skills` の README の「Telemetry」）。

### 求める認証情報

- エージェントの手順に使うモデルを聞き、サブスクリプションなら `npx e2e login` をユーザーに実行してもらう。
- テストに要るパスワードやトークンは、設定ファイルの `credentials` か `secrets` で名前を指定する。値そのものは書かない。

  > 引用: "Never put a secret in a test, the config, or the progress file."

  認証情報は名前で指定する、とも書かれている（詳しくは `e2e` スキルのトピック `setup`）。

### スキルが自分に課している歯止め

- 古いテスト、ヘルパー、古いランナーの設定は、ユーザーの確認なしに消したり変えたりしない。
- 1 セッションで 1 つの区切りだけを扱う。
- アサーションを弱める、理由なくタイムアウトを延ばす、手順を抜く、で通すことをしない。
- コミットはしない（「Do not commit on the user's behalf.」）。

## migrate-to-e2e で確かめられなかったこと

- `npx skills add` を実際に実行したときの対話画面と、書かれるファイルの一覧。上の内容はソースコードを読んで推測したものである。
- エージェントの手順でモデルに送る画面情報の中身（スクリーンショットか、アクセシビリティツリーか）。
- TesterArmy の有料サービスの料金と、e2e の OSS 部分との境界。

## See also

- [e2e のドキュメント](https://e2e.tester.army/docs)
- [tester-army/e2e の migrate-to-e2e/SKILL.md][skill-md]
- [e2e: Coding agents（スキルのインストール方法）](https://e2e.tester.army/docs/coding-agents)
- [e2e: From Playwright（Playwright の移行ガイド）](https://e2e.tester.army/docs/migrate/playwright)
- [e2e: Telemetry](https://e2e.tester.army/docs/telemetry)
- [vercel-labs/skills の README][skills-readme]

[skill-md]: https://github.com/tester-army/e2e/blob/ef977f4856da009cac26d78d2e9bb14e5991ee41/skills/migrate-to-e2e/SKILL.md
[skills-readme]: https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/README.md
