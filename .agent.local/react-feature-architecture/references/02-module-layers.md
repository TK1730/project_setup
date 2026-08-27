---
type: architectural-structure
title: Abstract Layers of a Feature Module
description: The six abstract layers that make up a Feature module in a React & TypeScript project.
tags:
  - architecture
  - layers
  - clean-architecture
  - module-structure
---

# 2. 汎用 Feature モジュールの6つの抽象層 (Module Layers)

Feature ディレクトリは、以下の **6つの抽象責務（Layer）** で構成されます。プロジェクトの必要性に応じて必要な層のみを選択・配置します。

| 抽象層 (Layer) | 役割・責務 | 含まれる要素の例 |
| :--- | :--- | :--- |
| **1. Public Interface** | 外部に公開する成果物・型の定義 | `index.ts` |
| **2. Presentation** | 画面描画・UIコンポーネント | `[Domain]View.tsx`, `[Item]Card.tsx`, `[Form].tsx` |
| **3. State & Lifecycle** | 状態管理・カスタムHook・ストア | `use[Domain].ts`, `use[Domain]Filter.ts` |
| **4. Domain Logic** | 純粋な計算・バリデーション・変換 | `[domain]Calculators.ts`, `[domain]Rules.ts` |
| **5. Data Access** | 外部API通信・ストレージ連携 | `[domain]Api.ts`, `[domain]Repository.ts` |
| **6. Models & Contracts** | ドメインエンティティの型定義・スキーマ | `types.ts`, `schema.ts` |
