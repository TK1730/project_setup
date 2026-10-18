---
type: reference
title: 'Headless Component パターン'
description: 'Juntao Qiu の記事「Headless Component: a pattern for composing React UIs」の要約。見た目を持たないコンポーネント（カスタムフック）に状態とロジックを集め、UI と切り離す設計パターン。'
tags:
  [
    react,
    frontend,
    headless-component,
    custom-hooks,
    separation-of-concerns,
    accessibility,
    testing,
  ]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-09T00:00:00Z }
stale_after: 2027-10-09T00:00:00Z
---

# Headless Component パターン

martinfowler.com の記事 [Headless Component: a pattern for composing React UIs][article]（Juntao Qiu、2023-11-07）の要約。React のコンポーネントから、見た目に関わらない状態とロジックをすべて取り出し、「頭脳」と「見た目」を分ける Headless Component パターンを、ドロップダウンの実装を題材に説明している。

## 問題: ロジックと見た目が絡み合う

高機能な React コンポーネントほど、複雑なロジックと見た目の表現が 1 つのコンポーネントに混ざりやすい。その結果、次の問題が起きる。

- 保守しにくい。見た目を変えるつもりがロジックに影響する。
- テストしにくい。ロジックを確かめるのに DOM の描画が必要になる。
- 見た目だけが違う同じ振る舞いのコンポーネントを、何個も作る羽目になる。

## 解決策: Headless Component

Headless Component は、見た目に関わらないロジックと状態管理をすべて抽出したコンポーネントである。記事の言葉では「コンポーネントの頭脳を見た目から切り離す」。React では、カスタムフックとして実装するのが基本形になる。

## 記事の流れ: ドロップダウンを段階的に育てる

| 段階                    | 内容                                                                                                                                                                                       |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. 素朴なドロップダウン | 開閉状態と選択項目を持つ。`Trigger` と `DropdownMenu` に分け、子は props だけを受け取り状態を持たない                                                                                      |
| 2. キーボード操作       | `selectedIndex` 状態と `handleKeyDown`（Enter / Space / ↓ / ↑）を足し、ARIA 属性でアクセシビリティを確保する                                                                               |
| 3. カスタムフック化     | 状態と操作を `useDropdown` に移す。`isOpen`・`selectedItem`・`selectedIndex` と `toggleDropdown`・`handleKeyDown`・`setSelectedItem` を返す。これが Headless Component の本体              |
| 4. テスト               | フックを `renderHook` と `act` で単体テストし、フックを使う簡易な `SimpleDropdown` で利用者の操作を結合テストする                                                                          |
| 5. Context API 版       | `HeadlessDropdown` を Provider とし、`Trigger`・`List`・`Option` の子コンポーネントが `useDropdownContext` で状態を共有する宣言的な書き方。各子は `as` prop で描画する要素を差し替えられる |
| 6. 新しい UI 要件       | Tailwind CSS で見た目も構造も違う `DropdownTailwind` を作り、`useDropdown` をそのまま再利用できることを示す                                                                                |
| 7. 状態の追加           | 読み込み中・エラーといった状態が増えても、ロジック側に閉じ込められる                                                                                                                       |
| 8. リモートデータ取得   | 汎用の `useService` フックで、任意の非同期関数の loading / error / data を管理する                                                                                                         |
| 9. 合成                 | `useService` と `useDropdown` を組み合わせ、`Dropdown` コンポーネント自体は単純なまま非同期ドロップダウンを作る                                                                            |

## 利点と欠点

| 観点                   | 内容                                                                 |
| :--------------------- | :------------------------------------------------------------------- |
| 利点: 再利用性         | 1 つのフックを複数の見た目の実装で使い回せる                         |
| 利点: 関心の分離       | ロジックと描画がはっきり分かれ、保守しやすい                         |
| 利点: 柔軟性           | 同じ振る舞いのまま、見た目を自由に変えられる                         |
| 利点: テストしやすさ   | ロジックを DOM と切り離して検証できる                                |
| 利点: アクセシビリティ | キーボード操作や ARIA 属性をロジック側で一度だけ正しく作れる         |
| 欠点: 学習コスト       | パターンに慣れていない開発者は、最初は遅くなる                       |
| 欠点: 間接化           | 使いすぎると抽象化の層が増え、かえって読みにくくなる                 |
| 欠点: 本番品質         | 本番向けの部品を一から作るのは大変で、既存ライブラリを使うほうがよい |

## 既存のライブラリ

記事は、本番では次のような実績のあるライブラリを使うことを勧めている。

- [React Aria](https://react-spectrum.adobe.com/react-aria/)（Adobe）: キーボード操作、フォーカス管理、ARIA 属性のためのフック群。
- [Headless UI](https://headlessui.com/): Tailwind CSS と組み合わせやすい、スタイルを持たないアクセシブルな部品。
- [TanStack Table（React Table）](https://tanstack.com/table): テーブルやデータグリッドを作るためのヘッドレスなユーティリティ。
- [Downshift](https://www.downshift-js.com/): アクセシブルなドロップダウンやコンボボックスを、描画を自由にして作れるライブラリ。

## 歴史的な位置づけ

記事は、このパターンが新しい発明ではなく、Presentation Model や MVVM といった GUI アーキテクチャの古典的なパターンを、React のコンポーネント中心の世界に当てはめ直したものだと述べる。ロジックをビューから分けるという原則は今も有効である。一方で、かつての動機の一部（ビューのテストが難しいこと）は、現代のテストツールによって和らいでいる。

## まとめ（記事の結論）

- 同じ振る舞いに複数の見た目が必要なときや、ロジックが複雑で見た目から隔離したいときに特に効く。
- 記事のドロップダウンは学習用の例であり、本番では Headless UI や React Table などの実績あるライブラリを使うとよい。
- UI 開発における関心の分離は、拡張しやすく、アクセシブルで、保守しやすい React アプリケーションの要である。

## 解説: 本プロジェクトで読み取れるポイント

以下は記事そのものではなく、本要約での補足である。

- 本プロジェクトの `useTimer`（[タイマー基盤](/frontend/lib/timer.md)）や `features/pomodoro/hooks/` のフックは、見た目を持たずに状態と操作を返すという点で、すでに Headless Component の形をしている。新しいフックを作るときも、戻り値を「状態」と「操作」に分け、JSX を返さない形にそろえるとよい。
- フックの責務の切り方は [React カスタムフックの責務分離とライフサイクル設計指針](/knowledge/react-hook-separation-and-lifecycle.md) に、コンポーネント側の分割は [コンポーネント設計およびモジュール解決ガイドライン](/frontend/component-guidelines.md) に従う。
- 記事の `useService` + `useDropdown` のように、小さなフックを合成して機能を組み立てる。1 つのフックに取得・状態・操作を全部入れない。
- 記事の「欠点: 間接化」は重要である。見た目が 1 種類しかなく、ロジックも単純な部品まで無理にヘッドレス化しない。
- テストは記事と同じく、フックを `renderHook` で単体テストし、振る舞いの仕様として書く（[テスト設計における AAA パターン](/knowledge/aaa-pattern.md)）。

## 用語

| 用語               | 意味                                                                          |
| :----------------- | :---------------------------------------------------------------------------- |
| Headless Component | 見た目を持たず、状態とロジックだけを提供するコンポーネント（多くはフック）    |
| Compound Component | Provider と子コンポーネント群が Context で状態を共有する宣言的な部品の組み    |
| `as` prop          | 子コンポーネントが描画する要素やコンポーネントを利用側が差し替えるための prop |
| Presentation Model | ビューの状態と振る舞いを、ビューから独立したモデルに持たせる GUI パターン     |
| MVVM               | Model-View-ViewModel。ViewModel がビュー向けの状態と操作を提供するパターン    |

## See also

- [Headless Component: a pattern for composing React UIs (martinfowler.com)][article]
- [Headless Component で React の UI とロジックを分離する](/references/itnext/decoupling-ui-and-logic-headless-components.md) - 同じ著者による前身の入門記事
- [React カスタムフックの責務分離とライフサイクル設計指針](/knowledge/react-hook-separation-and-lifecycle.md)
- [コンポーネント設計およびモジュール解決ガイドライン](/frontend/component-guidelines.md)
- [タイマー基盤（useTimer / time.ts）仕様・設計](/frontend/lib/timer.md)

[article]: https://martinfowler.com/articles/headless-component.html
