# React / Next.js フロントエンド開発 学習ガイド

React および Next.js（App Router）を用いたフロントエンド開発において、アーキテクチャ・コンポーネント＆State＆API 通信設計・UI デザイン・テスト手法を体系的に学ぶためのドキュメント群である。関心のある概念ごとのフォルダ、または各ドキュメントから読み進めることができる。

## カテゴリ（フォルダ）一覧

- [architecture/](architecture/) - ディレクトリ構成・アーキテクチャ設計（Bulletproof React、コンポーネント粒度分類、Feature-Sliced Design）
- [components-and-state/](components-and-state/) - コンポーネント・State・API 通信設計（Server / Client Components 境界、State 構造 5 原則、State の置き場所、合成パターン、API の呼び場所）
- [ui-and-design/](ui-and-design/) - UI デザイン・スタイリング・UX・部品カタログ（デザイントークン、UI の 4 状態、視覚デザイン原則、アクセシビリティ、UI コンポーネント図鑑）
- [testing/](testing/) - フロントエンドのテスト・品質保証（Testing Trophy と Testing Library の原則、Vitest / Storybook / Playwright の使い分け）

## 1. ディレクトリ構成・アーキテクチャ設計（[architecture/](architecture/)）

- [Bulletproof React の全体像とアーキテクチャ原則](architecture/bulletproof-react-overview.md) - React アプリケーションの設計リファレンス Bulletproof React の要点（ディレクトリ構成、単方向依存ルール、コンポーネント・状態管理・API 層の設計）。
- [UI コンポーネントの粒度と分類（Atomic Design vs 現代の分割手法）](architecture/react-component-classification.md) - Atomic Design の 5 階層と、React 開発で起きやすい分類の迷いを解消する「汎用 UI 部品＋機能固有部品」の 2 層構成の比較。
- [Feature-Sliced Design (FSD) の概要と使い分け](architecture/feature-sliced-design-overview.md) - フロントエンド特化のアーキテクチャ手法である Feature-Sliced Design (FSD) の3階層（Layers・Slices・Segments）と依存ルール、プロジェクト規模に応じた採用判断基準を整理する。

## 2. コンポーネント・State・API 通信設計（[components-and-state/](components-and-state/)）

- [Server Components と Client Components の境界設計](components-and-state/nextjs-server-and-client-components.md) - Next.js App Router と React 19 における Server Components と Client Components の役割分担と、バンドルサイズおよびパフォーマンスを最適化する境界設計の原則を解説する。
- [State 構造の設計原則（Choosing the State Structure）](components-and-state/choosing-the-state-structure.md) - React 公式ドキュメント「Choosing the State Structure」に基づき、状態の不整合や更新漏れバグを防ぐための5つの State 設計原則を悪い例・良い例の対比とともに整理する。
- [State の置き場所（Colocation / Lifting Up）とデータフロー設計](components-and-state/react-state-ownership-and-data-flow.md) - React における State Colocation（状態の局所化）、Lifting State Up（状態のリフトアップ）、単方向データフロー、および Controlled / Uncontrolled コンポーネントの判断基準。
- [React のコンポーネント合成パターン（Composition Patterns）](components-and-state/react-component-composition.md) - Props 爆発やバケツリレー（Prop Drilling）を防ぐための、children による Containment、Named Slots、および Compound Components の設計パターン。
- [React / Next.js における API 通信の設計と呼び場所](components-and-state/api-fetching-and-layer-design.md) - React と Next.js（App Router）において、API 通信コードをどのディレクトリのファイルに配置し、どのコンポーネント・どのタイミングで呼び出すべきかの設計原則を整理する。

## 3. UI デザイン・スタイリング・UX・部品カタログ（[ui-and-design/](ui-and-design/)）

- [デザイントークンと CSS 変数の 2 層設計（Primitive / Semantic）](ui-and-design/design-tokens-and-css-variables.md) - 色・余白・タイポグラフィ等をマジックナンバー化せず、Primitive（基礎）トークンと Semantic（意味・役割）トークンの 2 層で体系化する CSS 設計ガイド。
- [UI の 4 状態（Ideal / Loading / Empty / Error）とフィードバック設計](ui-and-design/ui-states-and-feedback.md) - データ表示コンポーネントにおける状態網羅（Ideal・Loading・Empty・Error・Partial）と、ユーザー操作に対する非同期フィードバック設計の原則をまとめる。
- [エンジニアのための UI 視覚デザイン原則（Refactoring UI / Web Interface Guidelines）](ui-and-design/ui-visual-design-principles.md) - 『Refactoring UI』や Vercel の『Web Interface Guidelines』に基づき、感覚に頼らず数値とルールで画面を美しく整えるための視覚デザイン原則を解説する。
- [Web アクセシビリティ（a11y）とセマンティック HTML の基礎](ui-and-design/web-accessibility-basics.md) - キーボード操作やスクリーンリーダーを含め誰でも迷わず操作でき、かつ自動テスト（getByRole）も容易になるセマンティック HTML と React 実装の基本原則を解説する。
- [標準 UI コンポーネント図鑑（見た目・動きと名前の対応表）](ui-and-design/ui-component-catalog.md) - Web アプリケーションで頻出する定番 UI コンポーネントの英語・日本語名称、見た目と振る舞い、および類似部品との使い分け基準を整理したリファレンス。

## 4. フロントエンドのテスト・品質保証（[testing/](testing/)）

- [フロントエンドのテスト戦略（Testing Trophy と Testing Library の原則）](testing/frontend-testing-strategy.md) - Kent C. Dodds の Testing Trophy と Testing Library の設計思想に基づき、フロントエンドで何をどの粒度・どのクエリでテストすべきかを定めたガイドライン。
- [現代のフロントエンドテスト手法（Vitest / Storybook Interaction Test / Playwright）](testing/modern-frontend-testing-methods.md) - React / Next.js 開発で主流となっている Playwright、Storybook Interaction Test、Vitest（および Browser Mode）の特徴・強み・使い分けを解説するガイドライン。

## おすすめの読む順番

初めて読む場合は、次の順序で読み進めると全体像から実装詳細・品質保証までスムーズに理解できる。

1. **まず部品の名前と全体像を知る**: [標準 UI コンポーネント図鑑](ui-and-design/ui-component-catalog.md) → [Bulletproof React の全体像](architecture/bulletproof-react-overview.md) → [UI コンポーネントの粒度と分類](architecture/react-component-classification.md)
1. **React / Next.js の設計の勘所を押さえる**: [Server / Client Components の境界設計](components-and-state/nextjs-server-and-client-components.md) → [API 通信の設計と呼び場所](components-and-state/api-fetching-and-layer-design.md) → [State の置き場所とデータフロー設計](components-and-state/react-state-ownership-and-data-flow.md) → [State 構造の設計原則](components-and-state/choosing-the-state-structure.md) → [コンポーネント合成パターン](components-and-state/react-component-composition.md)
1. **見た目と使いやすさの品質を高める**: [UI の 4 状態とフィードバック設計](ui-and-design/ui-states-and-feedback.md) → [UI 視覚デザイン原則](ui-and-design/ui-visual-design-principles.md) → [デザイントークンと CSS 変数](ui-and-design/design-tokens-and-css-variables.md) → [Web アクセシビリティの基礎](ui-and-design/web-accessibility-basics.md)
1. **テストの書き方を知る**: [フロントエンドのテスト戦略](testing/frontend-testing-strategy.md) → [現代のフロントエンドテスト手法](testing/modern-frontend-testing-methods.md)
