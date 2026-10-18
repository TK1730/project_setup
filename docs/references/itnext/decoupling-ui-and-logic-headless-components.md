---
type: reference
title: 'Headless Component で React の UI とロジックを分離する'
description: 'Juntao Qiu の記事「Decoupling UI and Logic in React: A Clean Code Approach with Headless Components」の要約。useToggle の抽出と Downshift を例に、振る舞いと見た目を分ける考え方。'
tags: [react, frontend, headless-component, custom-hooks, separation-of-concerns, downshift]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-09T00:00:00Z }
stale_after: 2027-10-09T00:00:00Z
---

# Headless Component で React の UI とロジックを分離する

ITNEXT の記事 [Decoupling UI and Logic in React: A Clean Code Approach with Headless Components][article]（Juntao Qiu、2023-07-06）の要約。同じ著者が後に martinfowler.com で書いた [Headless Component パターン](/references/martinfowler/headless-component.md) の前身にあたる短い入門記事で、小さなカスタムフックの抽出から、Headless Component ライブラリの利用、UI 内のレイヤー構造へと話を広げている。

## 出発点: よく似た 2 つのコンポーネント

記事は、見た目も用途も違う 2 つのコンポーネントから始める。

- `ToggleButton`: 「おやすみモード」のような ON / OFF を切り替えるボタン。`isToggled` 状態と `toggle` 関数を持つ。
- `ExpandableSection`: 見出しをクリックすると詳細を開閉するセクション。`isOpen` 状態と `toggleOpen` 関数を持つ。

どちらも「真偽値の状態を持ち、反転させる」という同じ振る舞いを、それぞれのコンポーネントの中で書いている。

## 共通の振る舞いをカスタムフックに抜き出す

共通部分を `useToggle` フックに抜き出す。

```tsx
const useToggle = (init = false) => {
  const [state, setState] = useState(init);

  const toggle = useCallback(() => {
    setState((prevState) => !prevState);
  }, []);

  return [state, toggle];
};
```

単純なリファクタリングだが、振る舞いを見た目から分けるという重要な考え方を示している。このフックは JSX から独立した状態機械であり、`ToggleButton` も `ExpandableSection` も同じロジックの上に乗る。

記事は、中規模のフロントエンド開発では、変更やバグの多くが見た目ではなく UI の状態管理（ロジック）に関するものだと指摘する。フックはそのロジックを 1 か所に集め、調べやすく、最適化しやすく、保守しやすくする。

## Headless Component: 例としての Downshift

Headless Component とは、UI を一切描画せずに振る舞いと状態を管理するコンポーネントである。状態と操作の集まりを提供し、利用側がそれを自分の UI につなぐ。代表例として記事は [Downshift](https://www.downshift-js.com/) を挙げる。

ドロップダウンを一から作ると、ブラウザやデバイスの違いを含むアクセシビリティの細かな考慮が大量に必要になる。Downshift の `useSelect` を使うと、数行の JSX で完全にアクセシブルな選択リスト（記事の `StateSelect`）を作れる。

- `isOpen`・`selectedItem`・`highlightedIndex` は、`useSelect` が管理する状態である。
- `getToggleButtonProps`・`getLabelProps`・`getMenuProps`・`getItemProps` は、各要素に渡す props を返す関数（prop getter）である。
- prop getter の戻り値をスプレッド構文で要素に渡すと、クリック処理、キーボード操作、ARIA 属性がまとめて付く。
- 描画は利用側が完全に握るので、見た目はアプリケーションに合わせて自由に作れる。

同じパターンに従うライブラリとして、記事は次を挙げている。

- Reakit: アクセシブルな UI ライブラリやデザインシステムを作るための Headless Component 群（現在は [Ariakit](https://ariakit.org/) に改名）。
- [React Table（現 TanStack Table）](https://tanstack.com/table): フックベースで、組み合わせて様々なテーブルを作るユーティリティ。
- [react-use](https://github.com/streamich/react-use): Headless Component を含むフック集。

## UI の中のレイヤー構造

ロジックを意識して UI から分け続けると、UI 部分の中にレイヤー構造ができてくる。アプリケーション全体にまたがる従来のレイヤードアーキテクチャではなく、UI に限った構造である。

| 層                     | 責務                                                                                        |
| :--------------------- | :------------------------------------------------------------------------------------------ |
| JSX（最上層）          | 渡された props を表示することだけを担う                                                     |
| Headless Component     | 振る舞いと状態をすべて管理し、JSX が使うインターフェースを提供する                          |
| データモデル（最下層） | ドメイン固有のロジックを持つ。UI や状態には関心を持たず、データ管理と業務ロジックに集中する |

## 利点と欠点

| 観点                 | 内容                                                                                                 |
| :------------------- | :--------------------------------------------------------------------------------------------------- |
| 利点: 再利用性       | ロジックを独立させれば、複数の UI 要素で使い回せる。重複が減り、アプリケーション全体の一貫性も上がる |
| 利点: 関心の分離     | ロジックと見た目がはっきり分かれる。役割分担のある大きなチームで特に効く                             |
| 利点: 柔軟性         | 見た目を指定しないので、ロジックに影響を与えずに UI を自由に変えられる                               |
| 利点: テストしやすさ | ロジックが見た目から分かれているので、業務ロジックの単体テストを書きやすい                           |
| 欠点: 初期コスト     | 単純なアプリケーションや部品では過剰設計になり、不要な複雑さを生む                                   |
| 欠点: 学習コスト     | 概念に慣れていない開発者には、最初は理解しにくい                                                     |
| 欠点: 使いすぎ       | 必要のない部品まで何でもヘッドレスにしたくなり、コードベースが複雑になる                             |
| 欠点: 性能           | 大きな問題になることは少ないが、共有ロジックを使う複数のコンポーネントの再描画には注意が要る         |

記事は、他のアーキテクチャパターンと同じく万能ではなく、採用はプロジェクトの必要と複雑さで判断すべきだと締めている。

## まとめ（記事の結論）

- 振る舞いを描画から分けると、保守しやすく再利用しやすいコードになり、重複や潜在的なバグが減る。
- 小さな例では `useToggle` を 2 つのコンポーネントで共有し、大きな例では Downshift で高機能な入力部品を作った。
- この考え方を理解すれば、拡張しやすく保守しやすい UI を作れる。

## 解説: 本プロジェクトで読み取れるポイント

以下は記事そのものではなく、本要約での補足である。

- `useToggle` の例は「同じ振る舞いが 2 か所に出てきたら抜き出す」という順序を示している。最初からヘッドレスに設計するのではなく、重複に気づいてから抽出すると、欠点にある過剰設計や使いすぎを避けやすい。
- 記事の 3 層は、本プロジェクトでは「コンポーネント（JSX）」「`hooks/` のカスタムフック」「`lib/` などの純粋関数（例: [タイマー基盤](/frontend/lib/timer.md) の `time.ts`）」に対応させて読める。データモデル層を React から切り離しておくと、フックを経由せずに単体テストできる。
- Downshift の prop getter は、ARIA 属性やキーボード操作のような「正しく書くのが難しい部分」を利用側に書かせない工夫である。自前のフックでも、要素に渡す props の組をまとめて返すと、利用側の書き漏れを防げる。
- フックの責務の切り方は [React カスタムフックの責務分離とライフサイクル設計指針](/knowledge/react-hook-separation-and-lifecycle.md) に従う。

## 用語

| 用語               | 意味                                                                                         |
| :----------------- | :------------------------------------------------------------------------------------------- |
| Headless Component | UI を描画せず、振る舞いと状態だけを提供するコンポーネント（多くはフック）                    |
| Headless UI        | Headless Component を使って振る舞いと見た目を分ける UI の作り方                              |
| Prop getter        | 要素に渡すべき props（イベント処理や ARIA 属性）を返す関数。Downshift の `getItemProps` など |
| 状態機械           | 状態と、その状態を変える操作の組。記事では `useToggle` をこう呼んでいる                      |

## See also

- [Decoupling UI and Logic in React: A Clean Code Approach with Headless Components (ITNEXT)][article]
- [Headless Component パターン](/references/martinfowler/headless-component.md)
- [React カスタムフックの責務分離とライフサイクル設計指針](/knowledge/react-hook-separation-and-lifecycle.md)
- [Downshift](https://www.downshift-js.com/)

[article]: https://itnext.io/decoupling-ui-and-logic-in-react-a-clean-code-approach-with-headless-components-82e46b5820c
