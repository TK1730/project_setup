---
type: reference
title: 'Feature-Sliced Design (FSD) の考え方'
description: 'フロントエンド特化のアーキテクチャ手法である Feature-Sliced Design (FSD) の3階層（Layers・Slices・Segments）と依存ルール、プロジェクト規模に応じた採用判断基準を整理する。'
tags: [frontend, architecture, fsd, react, nextjs]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Feature-Sliced Design (FSD) の考え方

Feature-Sliced Design（FSD）は、フロントエンドアプリケーションを業務ドメインと責務の抽象度によって体系的に分割するためのアーキテクチャ設計手法である。コードを **Layers（レイヤー）**・**Slices（スライス）**・**Segments（セグメント）** の3階層で整理し、「上位レイヤーは下位レイヤーのみを参照でき、同一レイヤー内の別スライスは参照できない」という単方向依存ルールによって、機能追加や変更時の影響範囲を局所化する。小〜中規模プロジェクトでは全6層をそのまま導入すると過剰になるため、プロジェクトの複雑度に応じて必要な概念を選択的に採り入れることが重要である。

## Feature-Sliced Design (FSD) とは

従来の技術役割別ディレクトリ構成（トップレベルに `components/`・`hooks/`・`apis/` を並べる構成）では、規模が大きくなるにつれて「ある画面や仕様を変更したときにどのファイル群が影響を受けるか」を追跡しづらくなる。FSD（公式ドキュメント: `feature-sliced.design`）は、この課題を解決するために標準化されたフロントエンド特化のアーキテクチャ手法であり、暗黙の知識に頼らずディレクトリ名と依存方向のルールだけでコードの置き場所と参照可否を決定できるように設計されている。

## 3つの概念階層（Layers / Slices / Segments）

FSD では、すべてのコードを「Layers（抽象度と影響範囲）」「Slices（業務ドメイン）」「Segments（技術的役割）」の3段階の階層で分類する。

```text
src/
├── app/                  # [Layer] アプリケーション全体の初期化・ルーティング・Provider
├── pages/                # [Layer] 画面（ルート）単位の組み立て
├── widgets/              # [Layer] 複数 feature / entity を組み合わせた自立した UI ブロック
├── features/             # [Layer] ユーザーに価値を提供する操作・ユースケース
│   └── auth-by-email/    #   [Slice] 業務ドメイン・機能単位の分割
│       ├── ui/           #     [Segment] UI コンポーネント
│       ├── model/        #     [Segment] 状態管理・ビジネスロジック・スキーマ
│       ├── api/          #     [Segment] 通信処理・データ取得
│       └── index.ts      #     Public API（外部公開エントリポイント）
├── entities/             # [Layer] ビジネスエンティティ（データモデルと基本表示）
│   └── user/             #   [Slice]
│       ├── ui/           #     [Segment]
│       ├── model/        #     [Segment]
│       └── index.ts
└── shared/               # [Layer] ドメイン知識を持たない共通基盤
    ├── ui/               #   [Segment] 汎用 UI パーツ（Button, Modal など）
    ├── api/              #   [Segment] API クライアント基盤
    ├── lib/              #   [Segment] 汎用ヘルパー・ユーティリティ
    └── config/           #   [Segment] 環境変数・定数設定
```

### 1. Layers（レイヤー）

最上位のディレクトリ階層であり、責務の重さと他モジュールへの影響度に応じて上から下へ以下の **6層** に標準化されている（旧仕様に存在した `processes` レイヤーは現在廃止されている）。

1.  **`app`**: アプリケーション全体の起動処理、グローバル CSS、Provider（認証・テーマ・クエリクライアント等）の注入、ルーティング定義など、アプリ横断の設定を担う層である。（Slice を持たず、直接 Segment に分ける）
1.  **`pages`**: URL ルートに対応する1画面全体を構成する層である。独自の複雑なロジックは極力持たず、`widgets`・`features`・`entities` を配置して画面を組み立てる責務に集中する。（Next.js App Router と併用する場合は、ルート定義用の `app/` と混同を避けるため FSD 側を `src/views/` や `src/pages-flat/` と呼ぶか、Next.js の `app/` をルーティングアダプタとして薄く保つ構成が採られる）
1.  **`widgets`**: ヘッダー、サイドバー、商品一覧パネル、コメント欄全体など、複数の `features` と `entities` を組み合わせて1つの意味ある大きな UI の塊（画面内の独立したセクション）として完結させた層である。
1.  **`features`**: 「商品をカートに追加する」「記事にいいねする」「フィルタ条件で絞り込む」など、ユーザーのアクションを伴いビジネス上の価値を生むインタラクション（ユースケース）を扱う層である。
1.  **`entities`**: `user`（ユーザー）、`product`（商品）、`order`（注文）など、業務ドメインの中心となる名詞（概念・データモデル）を扱う層である。データの型定義、ステータス判定ロジック、アクションを持たない基本的な表示枠（アバターや商品カードの枠組みなど）を配置する。
1.  **`shared`**: 特定の業務ドメインに一切依存しない再利用可能な基盤コード（UI キット、HTTP クライアント、日付フォーマット関数、共通定数など）を配置する最下層である。（Slice を持たず、直接 Segment に分ける）

### 2. Slices（スライス）

`pages`・`widgets`・`features`・`entities` の各レイヤー直下に作られる第2階層であり、**業務ドメインや機能単位** でコードを分割する。Slice の名前は技術用語ではなくプロジェクトの業務知識（`user`, `post`, `checkout`, `add-to-cart` など）を反映させる。なお、`app` はシステム全体の統合層であり、`shared` はドメインを持たない共通層であるため、この2つのレイヤーには Slice を作らず直接 Segment を配置する。

### 3. Segments（セグメント）

各 Slice（または `app` / `shared`）の内部を **技術的な役割** で整理する第3階層である。代表的な Segment 名は以下の通りである。

1.  **`ui`**: コンポーネント、スタイル、フォーマッタなどの画面表示に関する要素を配置する。
1.  **`model`**: 状態（State）、ストア、フォームのバリデーションスキーマ、ドメイン計算ロジック、型定義などを配置する。
1.  **`api`**: その Slice が必要とするバックエンド API リクエスト関数や DTO 変換、データフェッチフックを配置する。
1.  **`lib`**: その Slice 内部だけで使われる補助関数やカスタムフックを配置する。
1.  **`config`**: 機能フラグや定数、設定値を配置する。

## 厳格な依存ルールと Public API

FSD が高い保守性を維持できる理由は、ディレクトリ名だけでなく以下の2つのアクセス制御ルールを強制する点にある。

### 1. 単方向レイヤー依存ルール（Import Rule on Layers）

**「ある Slice は、自分より下位のレイヤーにある Slice しか import できない。また、同じレイヤーにある別の Slice を import してはならない」** という絶対規則である。

```text
[依存の方向（上から下へのみ import 可能）]
app  ──▶  pages  ──▶  widgets  ──▶  features  ──▶  entities  ──▶  shared
```

1.  **NG 例（逆方向の依存）**: `entities/user` から `features/auth` を import する（下位レイヤーが上位レイヤーに依存してしまう）。
1.  **NG 例（同一レイヤー間の横断依存）**: `features/cart` から `features/coupon` を直接 import する（機能同士が密結合になる）。
1.  **解決策（上位レイヤーでの合成）**: `features/cart` と `features/coupon` を連携させたい場合は、お互いを直接 import させるのではなく、1つ上の `widgets/checkout-panel` や `pages/cart` で両者を並べて配置し、props や `children`（コンポジション）、あるいは下位の `entities` を介して組み合わせる。

### 2. Public API（`index.ts`）を通じたカプセル化

各 Slice（および `shared` の各 Segment）の直下には必ずエントリポイントとなる `index.ts` を配置し、外部に公開するコンポーネント・関数・型だけを re-export する。外部のモジュールは Slice の内部ファイル（例: `features/auth/ui/LoginForm.tsx`）を深いパスで直接 import してはならず、必ず `features/auth`（`index.ts`）経由でアクセスする。これにより、Slice 内部のディレクトリ構造や実装詳細を外部に影響を与えずにリファクタリングできる。

```ts
// 良い例: Public API (index.ts) 経由で import する
import { LoginForm, useAuth } from '@/features/auth';

// 悪い例: Slice の内部構造に直接立ち入って import する
import { LoginForm } from '@/features/auth/ui/LoginForm';
```

## Bulletproof React との違いと採用判断基準

実務でよく比較されるディレクトリ設計として **Bulletproof React**（`app/`, `features/`, `components/`, `hooks/`, `lib/` 等に分ける構成）がある。両者の違いと、プロジェクト規模に応じた使い分けの基準は以下の通りである。

### Bulletproof React と FSD の構造的な違い

| 観点                     | Bulletproof React                                                                                     | Feature-Sliced Design (FSD)                                                                                                                        |
| :----------------------- | :---------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **基本思想**             | 機能を `features/<domain>/` に集約し、共通要素を `components/` や `lib/` に置くシンプルで実践的な構成 | 抽象度と責務の重さに応じて **6層（Layers）** に厳密に階層化する構成                                                                                |
| **ドメインと機能の分離** | `features/users/` の中に「User の型・表示」も「User の編集・削除操作」も同居する                      | **名詞（データと基本表示）は `entities/user`**、**動詞（ユーザー操作）は `features/edit-user`**、**大きな複合 UI は `widgets`** へと明確に分離する |
| **判断の迷いやすさ**     | 導入コストが低く直感的だが、規模が拡大すると1つの `feature` が肥大化しやすい                          | 「これは `entity` か `feature` か `widget` か」の境界判断に学習コストがかかるが、大規模化しても1つの Slice が肥大化しにくい                        |

### 小〜中規模プロジェクトでどこまで採り入れるべきか

小〜中規模のチームや CRUD 中心の Web アプリケーションにおいて、最初から FSD の全6層（特に `entities` / `features` / `widgets` の厳密な分離）をフルスペックで導入すると、「ボイラープレートが増える」「どの層に置くべきかの議論に時間を取られる」というオーバーヘッドが生じやすい。そのため、以下の基準で段階的にエッセンスを採り入れるのが現実的である。

1.  **最初から必ず採り入れるべき原則**: **単方向依存の意識**（共通基盤 `shared`/`components` から業務機能 `features` を逆参照しない、機能間で相互参照しない）と、**機能単位の凝集（Colocation）**、および **Public API（`index.ts`）による境界の明示** は規模を問わず有効である。
1.  **小〜中規模（数名〜10名程度・画面数10〜30程度）**: Bulletproof React ベース（`app` + `features` + `shared` 相当の3層構造）から始めるのが最も費用対効果が高い。この段階では `entities` や `widgets` を無理に分けず、ドメインごとの `features/<domain>/` 内で Segment（`components/`, `api/`, `hooks/`, `types/`）を整理するだけで十分に保守できる。
1.  **中〜大規模への移行サイン（FSD の層を追加するタイミング）**: 「複数の feature（例: 注文機能・お気に入り機能・レビュー機能）から同じドメインモデルやカード UI（例: 商品 `Product`）を参照したくなり、feature 間 import が発生し始めた」ときが `entities` 層を切り出すタイミングである。また、「複数の feature を組み合わせた巨大なヘッダーやダッシュボードパネルが `pages` を圧迫し始めた」ときに初めて `widgets` 層を導入すると、FSD の恩恵を無理なく活かせる。

## See also

- [Feature-Sliced Design 公式ドキュメント](https://feature-sliced.design/)
- [Bulletproof React の全体像](/learning/architecture/bulletproof-react-overview.md)
- [UI コンポーネントの粒度と分類（Atomic Design と現代の分類法）](/learning/architecture/react-component-classification.md)
- [Next.js の app/ と features/ の分担](/knowledge/nextjs-app-and-features.md)
