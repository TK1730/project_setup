---
type: guideline
title: 'モダンなフロントエンドテスト手法（Playwright・Storybook・Vitest）'
description: 'React / Next.js 開発で主流となっている Playwright、Storybook Interaction Test、Vitest（および Browser Mode）の特徴・強み・使い分けを解説するガイドライン。'
tags: [testing, playwright, storybook, vitest, frontend, nextjs]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# モダンなフロントエンドテスト手法（Playwright・Storybook・Vitest）

現在の React / Next.js 開発では、テストの対象と粒度の違いに応じて **Playwright（E2E テスト）**、**Storybook Interaction Test（UI カタログ兼インタラクションテスト）**、および **Vitest（単体テスト・Browser Mode によるコンポーネントテスト）** の3つを組み合わせて品質を担保するのが主流である。かつてのフロントエンドテストは「E2E は不安定で遅い（Flaky）」「擬似 DOM（jsdom）では実際のレイアウトやブラウザ API が動かない」という課題を抱えていたが、これら3つのモダンツールはその弱点を解消するよう設計されている。それぞれの強みと守備範囲を理解し、検証したいリスクに最も適したツールを選択する。

## 1. Playwright による E2E テスト

Playwright は、実際のブラウザエンジン（Chromium / WebKit / Firefox）とアプリケーションサーバー（バックエンド実機または API モック）を起動し、ページ遷移や認証を含むユーザーシナリオ全体を通しで検証する E2E テストフレームワークである。

### 主な特徴と強み

1.  **Auto-waiting（自動待機）による高い安定性**: ボタンのクリックやテキストの検証を行う際、対象の要素が DOM に現れ、アニメーションが終わり、クリック可能な状態になるまで Playwright が自動的に待機する。従来の E2E テストで頻発していた「固定時間の `sleep` を入れないとタイミング次第でテストが落ちる（Flaky Test）」という問題を根本から解消している。
1.  **Role ベースの Locator（Testing Library と同じ思想）**: `page.getByRole('button', { name: '開始' })` や `page.getByLabel('ユーザー名')` のように、アクセシビリティロールと表示名に基づいた要素取得が標準のベストプラクティスとして組み込まれている。これにより、単体・結合テストと E2E テストで同じ設計思想（実装詳細に依存しないテスト）を一貫して適用できる。
1.  **Trace Viewer による圧倒的なデバッグ体験**: テスト失敗時のスクリーンショットや動画だけでなく、各操作ステップの前後における実際の DOM スナップショット、コンソールログ、ネットワーク通信（リクエスト・レスポンスの中身）を時系列で巻き戻して確認できる **Trace Viewer** を備えている。CI 上で失敗したテストの原因特定が劇的に速くなる。

```ts
import { test, expect } from '@playwright/test';

test('問題を選択して演習を開始できる', async ({ page }) => {
  await page.goto('/problems');

  // Auto-waiting により要素が表示・操作可能になるまで自動で待ってからクリックされる
  await page.getByRole('link', { name: '配列の合計値' }).click();
  await page.getByRole('button', { name: '開始' }).click();

  await expect(page).toHaveURL(/\/problems\/.+\/solve/);
  await expect(page.getByRole('heading', { name: '配列の合計値' })).toBeVisible();
});
```

## 2. Storybook Interaction Test（`play` 関数）

Storybook はコンポーネントの見た目を一覧・確認する UI カタログとして広く使われているが、各ストーリー（`*.stories.tsx`）に **`play` 関数** を定義することで、カタログ上でそのままクリックや文字入力、アサーションを自動実行するインタラクションテストとして活用できる。

### 主な特徴と強み

1.  **カタログ作成とテストの二重管理をなくせる**: コンポーネントの初期状態を表現するために作った Story をそのままテストフィクスチャとして再利用し、`play` 関数内で `@storybook/test`（内部は Testing Library と Vitest の `expect`）を使って操作と検証を記述できる。
1.  **実際のブラウザ画面でステップ実行を見ながらデバッグできる**: Storybook の画面下部にある「Interactions」パネル上で、どのボタンをクリックし、どのアサーションが成功・失敗したかを1ステップずつ巻き戻しながら視覚的に確認できる。
1.  **Visual Regression Test（VRT：画像差分テスト）との高い親和性**: `play` 関数で「モーダルを開いた状態」「バリデーションエラーを表示させた状態」まで操作を進め、その最終状態のスクリーンショットを Chromatic や Playwright 等で撮影して画像差分を比較することで、CSS 崩れと動作保証を同時に自動化できる。

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { expect, fn, userEvent, within } from '@storybook/test';
import { AnswerForm } from './AnswerForm';

const meta = {
  component: AnswerForm,
  args: { onSubmit: fn() },
} satisfies Meta<typeof AnswerForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const EmptyError: Story = {
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);

    // 未入力のまま送信ボタンをクリック
    await userEvent.click(canvas.getByRole('button', { name: '提出する' }));

    // エラーメッセージが表示され、onSubmit が呼ばれていないことを検証
    await expect(canvas.getByText('回答を入力してください')).toBeInTheDocument();
    await expect(args.onSubmit).not.toHaveBeenCalled();
  },
};
```

## 3. Vitest（単体テスト ＋ Browser Mode）

Vitest は Vite ベースの高速なテストランナーであり、Jest 互換の直感的な API を持ちながら、TypeScript や ESM（ES Modules）を複雑な設定なしでそのまま高速に実行できる。

### 1. 純粋関数・カスタムフックの高速実行（Node / jsdom 環境）

1.  日付計算、データ変換、バリデーション関数などの純粋な TypeScript ロジックや、DOM のレイアウトに依存しないカスタムフックの単体テストは、Vitest の Node 環境または軽量な `jsdom` / `happy-dom` 環境でミリ秒単位で高速に回す。
1.  ウォッチモード（ファイル保存時の差分再実行）が非常に速いため、TDD（テスト駆動開発）のサイクルを回すのに適している。

### 2. 近年のトレンド：Vitest Browser Mode

1.  **従来の `jsdom`（擬似 DOM）の限界**: 長年使われてきた `jsdom` は Node.js 上で DOM の一部を模倣しているだけなので、CSS の実際のレイアウト計算（`getBoundingClientRect`）、要素の可視判定、ネイティブの `<dialog>` 要素、`IntersectionObserver`、`ResizeObserver`、クリップボード API などが正しく動作せず、モックだらけになる課題があった。
1.  **Vitest Browser Mode の解決策**: E2E テストのようにアプリケーション全体やページ遷移を立ち上げるのではなく、**テスト対象の1コンポーネントだけを本物のヘッドレスブラウザ（Playwright プロバイダ等）にマウントしてテストを実行する** 手法である。
1.  **メリット**: `jsdom` のような偽の環境に起因するモックの苦労をなくし、本物の CSS・本物のブラウザネイティブ API が動く環境で、E2E よりもはるかに軽量・高速にコンポーネント結合テストを実行できる。

## 4. 3手法の使い分けまとめ表

どのテスト手法をいつ使うべきかの判断基準を以下の表にまとめる。

| 観点                                | Vitest（Node / jsdom）                                         | Vitest Browser Mode / Storybook Interaction Test                                                                              | Playwright（E2E）                                                                          |
| :---------------------------------- | :------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| **主なテスト対象**                  | 純粋関数、ユーティリティ、複雑なカスタムフック、軽量なロジック | 単一〜複数コンポーネントの UI 操作、フォーム検証、モーダル・ポップオーバー等の開閉                                            | 複数ページをまたぐ導線、認証・認可、ルーティング、バックエンド API との結合                |
| **実行環境**                        | Node.js（および擬似 DOM の `jsdom`）                           | 本物のブラウザ（コンポーネント単位でマウント）                                                                                | 本物のブラウザ ＋ アプリケーションサーバー全体                                             |
| **実行速度**                        | 最速（ミリ秒単位）                                             | 高速〜中速（ページ遷移を伴わないため軽量）                                                                                    | 低速（サーバー起動と画面遷移を伴う）                                                       |
| **CSS・実ブラウザ API の検証**      | 不可（レイアウト計算やネイティブ API はモックが必要）          | **可能**（本物のレンダリングエンジン上で動作）                                                                                | **可能**（本番と同一のブラウザ環境で動作）                                                 |
| **Testing Trophy における位置づけ** | Unit                                                           | Unit 〜 **Integration（主戦場）**                                                                                             | E2E（クリティカルパスに限定）                                                              |
| **使い分けの目安**                  | ロジックの分岐や境界値・異常値を網羅したいとき                 | UI カタログ（Storybook）を作りながらフォームやインタラクションを固めたいとき、または実ブラウザ API を使う部品を検証したいとき | 「ログインして問題を解き、結果画面へ遷移する」といったアプリの根幹シナリオを保証したいとき |

## See also

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Storybook Interaction Testing](https://storybook.js.org/docs/writing-tests/interaction-testing)
- [Vitest Documentation](https://vitest.dev/guide/)
- [Vitest Browser Mode Guide](https://vitest.dev/guide/browser/)
- [フロントエンドのテスト戦略（Testing Trophy と Testing Library の原則）](/learning/testing/frontend-testing-strategy.md)
- [UI コンポーネント（見た目と名前）の定番カタログ](/learning/ui-and-design/ui-component-catalog.md)
