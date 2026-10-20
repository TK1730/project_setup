---
type: decision
title: 'migrate-to-e2e スキルの導入判断'
description: 'E2E テストの移行スキル migrate-to-e2e がこのプロジェクトで使えるかと、AGENTS.md の規定に照らした安全性の評価。'
tags: [development, ai, agent, skills, e2e, testing, security]
status: draft
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-18T00:00:00Z }
stale_after: 2027-10-18T00:00:00Z
---

# migrate-to-e2e スキルの導入判断

`npx skills add tester-army/e2e --skill migrate-to-e2e` で入るスキル（中身は [migrate-to-e2e スキルの要約](/references/tester-army/migrate-to-e2e.md)）を、このプロジェクトで使うべきかの評価。結論は「いまは入れない」で、移行元になる E2E テストがこのリポジトリに無く、スキルが働く前提を満たさないためである。

この文書は AI が調べて書いた評価で、導入するかどうかはまだ人が決めていない。そのため `status` を `draft` にしている。

## このプロジェクトのテストの現状

2026-10-18 時点のリポジトリを調べた結果は次のとおりである。

| 種類                       | 道具                                                     | 場所                                                 |
| :------------------------- | :------------------------------------------------------- | :--------------------------------------------------- |
| フロントエンドの単体テスト | Vitest（`unit` プロジェクト、`*.test.ts`）               | `frontend/lib/`、`frontend/features/` の `*.test.ts` |
| コンポーネントのテスト     | Storybook の Vitest アドオン（`storybook` プロジェクト） | `*.stories.tsx`                                      |
| バックエンドのテスト       | `go test`                                                | `backend/`                                           |
| E2E テスト                 | なし                                                     | なし                                                 |

- `frontend/package.json` には `playwright` と `@vitest/browser-playwright` があるが、どちらも Storybook のテストをブラウザで動かすための部品である（`frontend/vitest.config.ts` の `storybook` プロジェクト）。Playwright のテストスイートではない。
- スキルが移行元を見分ける印（`playwright.config.*`、`@playwright/test`、`cypress.config.*`、`.detoxrc*`、`.maestro/` など）は、リポジトリのどこにも無い。
- CI のワークフロー（`.github/` など）も無い。

## このプロジェクトで使えるかの判断

使えない。理由は次の 3 つである。

1. 移行元が無い: スキルは既存の E2E スイートを e2e に移すためのもので、棚卸しの最初の質問が「移行元のランナーは何か」である。このリポジトリには移す対象が無いので、手順の 1 段目で止まる。
1. 誤って動くおそれがある: `frontend/package.json` の `playwright` を手がかりに、エージェントが Storybook の部品を Playwright のスイートと取り違えるかもしれない。Vitest の単体テストと Storybook のテストは、どちらも E2E テストではなく、e2e に移す対象ではない。
1. 新しく E2E テストを始める道具ではない: E2E テストを新しく作りたいなら、移行用の `migrate-to-e2e` ではなく、e2e 本体（`npx e2e init`）と `e2e` スキルを検討する対象になる。e2e は Next.js の例（`examples/with-next`）を持つので、技術的にはフロントエンドに当てはめられる。ただしその検討は、この文書の範囲の外である。

仮に将来 Playwright などの E2E スイートを作ったあとで使うなら、スキルは次の変更をリポジトリに入れる。

- `frontend/` の直下に `e2e.config.ts`、`tests/**/*.e2e.ts`、`tests/support/*.ts`、`MIGRATION.md` を作る（pnpm のモノレポでは、移行元の設定ファイルの隣に置く、とスキルにある）。
- `frontend/package.json` に `test:e2e` スクリプトと `e2e`、`@e2e-dev/web` などの依存を足す。
- アプリの起動（`pnpm dev`）と、バックエンドと PostgreSQL の起動を、e2e の設定ファイルへ移す。e2e には Docker Compose のようなサービスの定義が無いので、テストの前に `compose.yaml` の起動コマンドを別に流す形になる。

## AGENTS.md の規定に照らした安全性

スキルの指示は、このリポジトリの `AGENTS.md`（習熟度ゲート利用規定）と次の点でぶつかる。ランクを記録した `proficiency.json` が無い間は、`AGENTS.md` の定めで全軸ランク 1 として扱う。

### コードの代筆との衝突

スキルの作業の中心は、エージェントが TypeScript のテスト、ヘルパー、設定ファイルを書くことである。

> 引用: "Port the slice's shared helpers first, once, as plain `.ts` files (not `.e2e.ts`, so the runner does not collect them), for example under `tests/support/`."

TS 軸がランク 1 の間は、`AGENTS.md` の「その言語のコードを代筆しない」に反する。`.ts` の編集は hook でも止められる。スキルを使うとしても、エージェントの役割は移行の方針と対応表の説明までになり、テストは本人が書くことになる。

Defect check（任意）では、エージェントがアプリのコード（`.tsx` など）にわざとバグを入れる。これも代筆にあたる。

### 生成量との衝突

AI 軸がランク 0〜1 の間は、1 ファイル・50 行を目安に区切り、単位ごとに本人の了解を得る決まりである。スキルの 1 回の区切りは 1〜5 件のテストと共有ヘルパーで、初回はさらに設定ファイル、スモークテスト、`MIGRATION.md` を一度に作る。区切りを本人の了解ごとに細かく分け直す必要がある。

### 外部への送信との衝突

`AGENTS.md` の安全規定は外部への送信を制限している。スキルと e2e には、次の送信がある。

- `npx e2e feedback` による e2e チームへの報告。スキルは `--dry-run` で見せてから、ユーザーの同意を得て送ると定めている。それでもこのリポジトリでは送らない扱いにするのが規定に合う。
- `e2e` CLI と `skills` CLI の匿名の利用統計。どちらも既定で送る。使う場合は `E2E_TELEMETRY_DISABLED=1`、`DISABLE_TELEMETRY=1` などで止める。
- エージェントの手順（`agent.act` など）を使うときの、モデルの提供元への送信。そのまま書き換えたテストならモデルは要らない。

### 破壊的な操作

Defect check で入れたバグを戻すために、スキルは `git checkout -- <file>` を使う。

> 引用: "Revert only that file (`git checkout -- <file>`), rebuild, and confirm `git diff -- <file>` is empty."

これは、そのファイルの未コミットの変更を消す操作である。使うなら Defect check を `off` にするのが安全である。

### 規定と衝突しない点

- コミットしない、古いテストを確認なしに消さない、秘密の値を書かない、というスキルの規則は、このリポジトリの方針と合う。
- `npx skills add` がファイルを置く `.agents/skills/` と `skills-lock.json` は、このリポジトリで既に他のスキル（Go や React のスキル）に使っている場所である。入れても置き場所の決まりは崩れない。

## 決定理由（Rationale）

いま入れても、移す対象が無いので何も起きないか、Storybook の部品を取り違えて誤った作業を始めるおそれがある。加えて、作業の中心が TS の代筆で、ランク 1 の間は規定上エージェントが担えない。E2E テストを入れる必要が出たら、まず e2e 本体を使うか Playwright を使うかを別に決める。そのあとに既存スイートの移行が必要になった時点で、改めてこのスキルを評価する。

## See also

- [migrate-to-e2e スキルの要約](/references/tester-army/migrate-to-e2e.md)
- [AGENTS.md（習熟度ゲート利用規定）](../../AGENTS.md)
- [frontend/vitest.config.ts](../../frontend/vitest.config.ts)
- [frontend/package.json](../../frontend/package.json)
- [skills-lock.json](../../skills-lock.json)
