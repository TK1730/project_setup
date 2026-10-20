# コンポーネント・State・API 通信設計

React / Next.js（App Router）における Server / Client Components の境界設計、State の構造・所有権、コンポーネント合成パターン、および API 通信の設計と呼び場所に関する学習ガイドの目次である。

## 文書一覧

- [Server Components と Client Components の境界設計](nextjs-server-and-client-components.md) - Next.js App Router と React 19 における Server Components と Client Components の役割分担と、バンドルサイズおよびパフォーマンスを最適化する境界設計の原則を解説する。
- [State 構造の設計原則（Choosing the State Structure）](choosing-the-state-structure.md) - React 公式ドキュメント「Choosing the State Structure」に基づき、状態の不整合や更新漏れバグを防ぐための5つの State 設計原則を悪い例・良い例の対比とともに整理する。
- [State の置き場所（Colocation / Lifting Up）とデータフロー設計](react-state-ownership-and-data-flow.md) - React における State Colocation（状態の局所化）、Lifting State Up（状態のリフトアップ）、単方向データフロー、および Controlled / Uncontrolled コンポーネントの判断基準。
- [React のコンポーネント合成パターン（Composition Patterns）](react-component-composition.md) - Props 爆発やバケツリレー（Prop Drilling）を防ぐための、children による Containment、Named Slots、および Compound Components の設計パターン。
- [React / Next.js における API 通信の設計と呼び場所](api-fetching-and-layer-design.md) - React と Next.js（App Router）において、API 通信コードをどのディレクトリのファイルに配置し、どのコンポーネント・どのタイミングで呼び出すべきかの設計原則を整理する。
