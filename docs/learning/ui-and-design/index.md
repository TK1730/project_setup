# UI デザイン・スタイリング・UX・部品カタログ

エンジニアが UI 実装で押さえておくべきデザイントークン、UI の 4 状態、視覚デザイン原則、Web アクセシビリティ、および標準 UI コンポーネントの名称・用途図鑑に関する学習ガイドの目次である。

## 文書一覧

- [デザイントークンと CSS 変数の 2 層設計（Primitive / Semantic）](design-tokens-and-css-variables.md) - 色・余白・タイポグラフィ等をマジックナンバー化せず、Primitive（基礎）トークンと Semantic（意味・役割）トークンの 2 層で体系化する CSS 設計ガイド。
- [UI の 4 状態（Ideal / Loading / Empty / Error）とフィードバック設計](ui-states-and-feedback.md) - データ表示コンポーネントにおける状態網羅（Ideal・Loading・Empty・Error・Partial）と、ユーザー操作に対する非同期フィードバック設計の原則をまとめる。
- [エンジニアのための UI 視覚デザイン原則（Refactoring UI / Web Interface Guidelines）](ui-visual-design-principles.md) - 『Refactoring UI』や Vercel の『Web Interface Guidelines』に基づき、感覚に頼らず数値とルールで画面を美しく整えるための視覚デザイン原則を解説する。
- [Web アクセシビリティ（a11y）とセマンティック HTML の基礎](web-accessibility-basics.md) - キーボード操作やスクリーンリーダーを含め誰でも迷わず操作でき、かつ自動テスト（getByRole）も容易になるセマンティック HTML と React 実装の基本原則を解説する。
- [標準 UI コンポーネント図鑑（見た目・動きと名前の対応表）](ui-component-catalog.md) - Web アプリケーションで頻出する定番 UI コンポーネントの英語・日本語名称、見た目と振る舞い、および類似部品との使い分け基準を整理したリファレンス。
