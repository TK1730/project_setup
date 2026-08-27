---
name: react-feature-architecture
title: React & TypeScript Feature-Based Architecture Guidelines
description: Practical guide and modular standards for Feature-based Architecture (Domain-driven component structure) in React and TypeScript projects. Provides a scalable blueprint split into single-concept reference modules.
type: architectural-standard
category: frontend-architecture
tags:
  - react
  - react19
  - nextjs
  - typescript
  - architecture
  - feature-based
  - colocation
  - encapsulation
  - barrel-export
  - tanstack-query
author: antigravity
version: "2.0.0"
updated_at: "2026-08-27"
---

# React & TypeScript Feature構成・設計ガイドライン (Feature-Based Architecture)

## 📌 概要 (Overview & Purpose)

あらゆる React / Next.js / TypeScript プロジェクトにおいて、保守性・テスタビリティ・開発生産性を最大化するための **「Feature構成（機能別・ドメイン駆動設計）」** の標準ナレッジベースです。

本スキルは **1ファイル1概念（Atomic Knowledge）** にモジュール分割されており、人間が必要な項目をピンポイントで参照できるだけでなく、AI エージェントがタスクに応じて局所的な知識を高速・高精度に読み込める構造になっています。

---

## 📚 概念別リファレンス一覧 (Single-Concept Modules)

| # | タイトル / 概念 | ファイルリンク | 概要 |
| :--- | :--- | :--- | :--- |
| **01** | **設計原則** | [01-core-principles.md](./references/01-core-principles.md) | コロケーション、カプセル化、ロジック3層分類の3大原則 |
| **02** | **モジュールの抽象層** | [02-module-layers.md](./references/02-module-layers.md) | プレゼンテーション、状態、ドメインロジック等6つの抽象層 |
| **03** | **段階的スケーリング** | [03-progressive-scaling.md](./references/03-progressive-scaling.md) | 規模に応じた3段階のフォルダ構造（Minimal / Standard / Enterprise） |
| **04** | **Public API & カプセル化** | [04-public-api-and-encapsulation.md](./references/04-public-api-and-encapsulation.md) | `index.ts` の役割、内部相対importと外部公開規約 |
| **05** | **ドメイン内API共通化** | [05-two-tier-data-pattern.md](./references/05-two-tier-data-pattern.md) | 同一ドメイン内でのAPI共通化とパーツ別ViewModel分離 |
| **06** | **クロスドメイン & OpenAPI** | [06-cross-feature-and-openapi.md](./references/06-cross-feature-and-openapi.md) | ドメイン間データ共有、OpenAPI生成コード配置、循環参照防止 |
| **07** | **サーバー状態 & Smart/Dumb** | [07-server-state-and-smart-dumb.md](./references/07-server-state-and-smart-dumb.md) | TanStack Queryキャッシュ活用、Propsバケツリレー解消 |
| **08** | **共通層 vs Feature層判定** | [08-shared-vs-feature-boundary.md](./references/08-shared-vs-feature-boundary.md) | 共通部品（Shared）とFeature部品の境界判定マトリクス |
| **09** | **品質チェックリスト** | [09-quality-checklist.md](./references/09-quality-checklist.md) | 実装時・Pull Requestレビュー時のセルフチェック項目 |
| **10** | **テスト配置 (コロケーション)** | [10-test-colocation-patterns.md](./references/10-test-colocation-patterns.md) | テストを実装ファイルのすぐ隣に置くコロケーション設計 |

---

## 🚀 クイックスタート: アプリ全体の基本構造

```text
src/ (または app/)
├── features/                      # 🎯 業務ドメイン別モジュール群 (Colocation & Encapsulation)
│   ├── auth/                      # 認証ドメイン
│   ├── users/                     # ユーザー管理ドメイン
│   └── <business-domain>/         # 各業務ドメイン
│
├── components/                    # 🌐 全機能共通の汎用UI部品 (Atoms / Design System)
├── hooks/                         # 🌐 全機能共通のユーティリティHook
├── lib/ (または utils/)           # 🌐 全機能共通の基盤処理 (httpClient, logger 等)
├── api/                           # 🌐 全社共通API・OpenAPI自動生成クライアント
└── app/ (または routes/, pages/)  # 🚦 ルーティング層 / ページシェル (Featureを呼んで配置するだけ)
```
