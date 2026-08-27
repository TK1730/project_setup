---
type: architectural-pattern
title: Progressive Scaling of Feature Folders
description: How to scale Feature folders across 3 complexity levels (Minimal, Standard, Enterprise) without over-engineering.
tags:
  - architecture
  - folder-structure
  - scaling
---

# 3. 規模に応じた段階的スケーリング (Progressive Scaling)

「フォルダを細かく作りすぎて空フォルダだらけになる」のを防ぐため、機能の複雑さに応じて以下の3段階で柔軟に適用します。

---

### Level 1: Minimal (小規模・シンプルな機能)
> ファイル数が少ない場合は、サブフォルダを作らずフラットに配置する。

```text
features/<domain>/
├── types.ts              # モデル
├── use<Domain>.ts        # ロジック & 状態
├── <Domain>View.tsx      # UI
└── index.ts              # 公開窓口
```

---

### Level 2: Standard (中規模・一般的な機能) ⭐【推奨】
> 責務ごとにフォルダを分割し、UIとロジックを明確に分ける。

```text
features/<domain>/
├── components/           # UI部品群
├── hooks/                # 状態・ライフサイクル
├── utils/                # 純粋計算・ヘルパー
├── types/ (または types.ts)
└── index.ts
```

---

### Level 3: Enterprise / Scaled (大規模・DDD / 複雑な業務機能)
> API層やバリデーションスキーマ、テストを完全に分離・コロケーション。

```text
features/<domain>/
├── api/                  # エンドポイント別通信 (※手動API定義の場合)
│   ├── getTask.ts
│   └── getTask.test.ts   # (テストは実装のすぐ隣に配置)
├── components/           # UI部品
│   ├── TaskItem.tsx
│   └── TaskItem.test.tsx
├── hooks/                # React Hooks
│   ├── useTaskManager.ts
│   └── useTaskManager.test.ts
├── utils/                # ドメイン計算ルール
│   ├── taskStats.ts
│   └── taskStats.test.ts
├── schemas/              # Zod / Valibot 等のバリデーション定義
├── types/                # ドメイン型
└── index.ts              # Public API
```

---

### 💡 OpenAPI 採用プロジェクトにおける Level 3 のバリエーション

OpenAPI（Swagger）から Orval、openapi-typescript、openapi-zod-client 等でクライアントコード・型・スキーマを自動生成している場合、**Feature 内に `api/` や `schemas/` フォルダを自前で作る必要はありません**。

通信関数や型は共通基盤層（`src/api/generated/`）に集約されるため、Feature 内部はよりスッキリした構成になります。

```text
# 🌐 共通基盤層 (自動生成)
src/api/generated/
├── <domain>.ts           # 生API通信関数 (getUsers, updateUser など)
└── schemas.ts            # 自動生成された型・Zodスキーマ

# 🎯 Feature 配下 (OpenAPI採用時)
features/<domain>/
├── components/           # UI部品
├── hooks/                # React Hooks (src/api/generated のクライアントを呼出・キャッシュ)
├── utils/                # ドメイン計算ルール
├── types/ (任意)         # UI固有の追加型 (※API型は @/api/generated から参照)
├── __tests__/            # 結合・単体テスト
└── index.ts              # Public API
```

> [!TIP]
> OpenAPI 導入時は **「共通基盤で自動生成された通信クライアントを、Feature 配下の Hook で束ねて UI に提供する」** という構成が最も重複がなく安全です。詳しくは [06-cross-feature-and-openapi.md](./06-cross-feature-and-openapi.md) を参照してください。
