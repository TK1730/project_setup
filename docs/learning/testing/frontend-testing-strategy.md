---
type: guideline
title: 'フロントエンドのテスト戦略（Testing Trophy と Testing Library の原則）'
description: 'Kent C. Dodds の Testing Trophy と Testing Library の設計思想に基づき、フロントエンドで何をどの粒度・どのクエリでテストすべきかを定めたガイドライン。'
tags: [testing, frontend, react, testing-library]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# フロントエンドのテスト戦略（Testing Trophy と Testing Library の原則）

フロントエンドのテストは、Kent C. Dodds が提唱した **Testing Trophy（テスティング・トロフィー）** のモデルに従い、複数コンポーネントが連携する **Integration テスト（結合テスト）** を最も厚く書くことを基本方針とする。また、テストコードを書く際は **Testing Library** の原則に従い、コンポーネントの内部状態やクラス名といった「実装詳細」ではなく、実際のユーザーが画面を見て操作するのと同じ「アクセシビリティロールや表示テキスト」を通じて振る舞いを検証する。この方針により、リファクタリングで壊れにくく、かつ実際のユーザー体験の破綻を確実に検知できる費用対効果の高いテストスイートを維持できる。

## 1. Testing Trophy の4層

従来のテストピラミッドよりもフロントエンド開発の実態に即したモデルとして、下から順に **Static → Unit → Integration → E2E** の4層で品質を担保する。トロフィーの胴体部分にあたる **Integration（結合テスト）** の面積を最も大きく取るのが最大の特徴である。

```text
        /---------\
       /   E2E     \        ← 主要なクリティカルパスのみ（少数・高コスト）
      /-------------\
     /               \
    /   Integration   \     ← ★ここを一番厚くする（画面・機能単位の連携テスト）
   /                   \
  /---------------------\
   |       Unit        |    ← 純粋関数・複雑なカスタムフック単体
   |-------------------|
  =======================
  |       Static        |   ← TypeScript の型検査・ESLint（土台）
  =======================
```

1.  **Static（静的解析）**: TypeScript の型チェックや ESLint によって、コードを実行する前にタイポ、型の不一致、未定義プロパティの参照などを機械的に防ぐ土台の層である。
1.  **Unit（単体テスト）**: 金額計算、日付フォーマット、バリデーションロジックなどの純粋関数や、複雑な状態遷移を持つ独立したカスタムフックを単体で検証する層である。実行速度が非常に速く、エッジケース（境界値や異常値）を網羅するのに適している。
1.  **Integration（結合テスト）**: 複数のコンポーネント、フォーム、状態管理、およびモック化した API 通信（MSW など）を組み合わせて、1つの機能や画面セクション単位でユーザー操作から画面更新までの一連の流れを検証する層である。単体テストでは見落とされがちな「コンポーネント間の受け渡しミス」を検知でき、かつ E2E テストよりも高速・安定して動作するため、**フロントエンドではこの層に最も多くのテスト投資を行う**。
1.  **E2E（End-to-End テスト）**: 実際のブラウザとバックエンド（またはステージング環境）を立ち上げ、ログインから決済・主要機能の完了までといったクリティカルなユーザーシナリオを通しで検証する層である。信頼性は最も高いものの実行時間とメンテナンスコストが大きいため、絶対に壊れてはいけない主要シナリオに絞って作成する。

## 2. 実装詳細（Implementation Details）をテストしない原則

Testing Library の中心的な設計思想は、**「テストが実際の使われ方に似ていれば似ているほど、そのテストはより大きな信頼（Confidence）を与えてくれる」** というものである。そのため、エンドユーザーが関知しない「実装詳細（Implementation Details）」をテスト対象にしてはならない。

### 避けるべき「実装詳細」の例

1.  `useState` や `useReducer` の内部変数名、またはストアの内部プロパティ構造を直接参照・検証すること。
1.  スタイリング用の CSS クラス名（`.btn-primary` など）や DOM のタグ階層（`div > span > p` など）に依存して要素を取得すること。
1.  内部の子コンポーネントが特定の Props で呼ばれたかどうかだけをモックで検証すること。

### なぜ実装詳細をテストしてはいけないのか

1.  **False Negative（偽陰性：動くのにテストが落ちる）**: ユーザーから見た画面表示や動作が一切変わっていないのに、内部の state 名を変更したり CSS クラスを整理したりしただけでテストが大量に失敗し、リファクタリングの足かせになる。
1.  **False Positive（偽陽性：壊れているのにテストが通る）**: 子コンポーネントのモックや内部 state の変化だけを検証していると、肝心の「ボタンが `disabled` のままでユーザーがクリックできない」「エラーメッセージが画面に描画されていない」といった実際のバグを見逃す。

### 正しいアプローチ：ユーザーの視点でテストする

1.  コンポーネントの内部状態ではなく、**「画面に表示されているテキスト」** や **「アクセシビリティロール（ボタン、テキストボックス、見出しなど）」** を通して要素を見つける。
1.  ユーザーがキーボードやマウスで操作したときに、**「画面の見た目がどう変化したか（またはどの API リクエストが飛んだか）」** という入出力の結果だけをアサーションする。

## 3. Testing Library のクエリ優先順位

要素を取得するクエリは、視覚障害を持つスクリーンリーダーのユーザーや通常のブラウザユーザーが画面を認識する方法に近い順で優先順位が定められている。原則として上から順に検討し、上位のクエリで取得できない場合のみ下位のクエリを使用する。

### 1. 最優先：誰でもアクセスできるクエリ（Accessible to Everyone）

1.  **`getByRole`（最優先・基本はすべてこれを使う）**: ボタン（`button`）、リンク（`link`）、入力欄（`textbox`）、見出し（`heading`）、チェックボックス（`checkbox`）など、要素の ARIA ロールで取得する。必ず `{ name: '保存する' }` のようにアクセシブルネーム（表示ラベル）を併用して特定の要素を絞り込む。`getByRole` で要素が取得できない場合は、テスト対象コンポーネントの HTML マークアップ自体にアクセシビリティ上の問題（`button` タグではなく `div` を使っている、ラベルが紐づいていない等）があるサインとして捉え、コンポーネント側を改善する。
1.  **`getByLabelText`（フォーム要素で有用）**: `<label>` と紐づいた入力フィールドを取得する。`getByRole('textbox', { name: 'メールアドレス' })` とほぼ同等に機能し、フォーム入力欄を探す際に直感的に使える。
1.  **`getByPlaceholderText`**: プレースホルダー文字列で取得する。ただしプレースホルダーは `<label>` の代替にはならないため、まず `<label>` を用意して `getByRole` や `getByLabelText` を使うことを優先する。
1.  **`getByText`**: ボタンや入力欄以外の、段落（`<p>`）や `<div>`・`<span>` に表示されたメッセージや本文テキストを探す場合に使う。
1.  **`getByDisplayValue`**: すでに値が入力されているフォーム要素を、現在の表示値から探す場合に使う。

### 2. 次点：セマンティッククエリ（Semantic Queries）

1.  **`getByAltText`**: `<img>` や `<area>` など、`alt` 属性を持つ画像要素を取得する場合に使う。
1.  **`getByTitle`**: `title` 属性や SVG 内の `<title>` 要素で取得する場合に使う（スクリーンリーダーで常に読み上げられるとは限らないため優先度は低めである）。

### 3. 最終手段：テスト専用 ID（Test IDs）

1.  **`getByTestId`**: `data-testid="..."` 属性で要素を取得する。ユーザーには見えずアクセシビリティの検証にもならないため、ロールやテキストが動的に変化してどうしても特定できない要素や、キャンバス・複雑なコンテナ要素などを取得する**最終手段**としてのみ使用する。

### クエリ種別（`getBy` / `queryBy` / `findBy`）の使い分け

1.  **`getBy...`**: 要素が現在画面に存在することを検証する場合に使う（見つからない場合は即座にエラーを投げる）。
1.  **`queryBy...`**: **「要素が画面に存在しないこと（消えたこと）」** を `expect(screen.queryByRole(...)).not.toBeInTheDocument()` の形で検証する場合にのみ使う（見つからない場合に `null` を返す）。
1.  **`findBy...`**: 非同期処理（API 通信やアニメーション）の完了後に要素が現れるのを待ってから取得する場合に使う（内部で `waitFor` を伴う Promise を返す）。

### 操作には `fireEvent` ではなく `userEvent` を使う理由

1.  **`fireEvent` の限界**: `fireEvent.click(button)` や `fireEvent.change(input, ...)` は、指定された単一の DOM イベントだけを人工的に発火させる。実際のブラウザで起きる前後の関連イベント（ホバー、フォーカス移動、キーダウン、キーアップなど）が省略されるため、たとえば「要素がフォーカスを得てから文字が1文字ずつ入力される」といった実際の挙動に依存する不具合を検知できない。
1.  **`userEvent`（`@testing-library/user-event`）の利点**: `await user.click(button)` や `await user.type(input, 'hello')` は、実際のユーザーがブラウザ上で行う一連のイベントシーケンス（`pointerOver` → `pointerMove` → `pointerDown` → `focus` → `pointerUp` → `click` など）を忠実にシミュレートする。また、非表示要素や `disabled` な要素に対する操作を適切に拒否してくれるため、原則としてすべてのユーザー操作には `userEvent.setup()` を用いた非同期操作を使用する。

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

test('メールアドレスとパスワードを入力して送信できる', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  // 実装詳細（class や state）ではなく、ロールとラベル名で取得する
  await user.type(screen.getByRole('textbox', { name: 'メールアドレス' }), 'taro@example.com');
  await user.type(screen.getByLabelText('パスワード'), 'secret123');
  await user.click(screen.getByRole('button', { name: 'ログイン' }));

  // 非同期で表示される完了メッセージを検証する
  expect(await screen.findByText('ようこそ、taro@example.com さん')).toBeInTheDocument();
});
```

## See also

- [Testing Library - Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [Testing Library - About Queries (Priority)](https://testing-library.com/docs/queries/about/#priority)
- [Kent C. Dodds - Write tests. Not too many. Mostly integration.](https://kentcdodds.com/blog/write-tests/)
- [Kent C. Dodds - Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
- [モダンなフロントエンドテスト手法（Playwright・Storybook・Vitest）](/learning/testing/modern-frontend-testing-methods.md)
- [テスト設計における AAA パターン](/knowledge/aaa-pattern.md)
