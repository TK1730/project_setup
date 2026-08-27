---
type: architectural-principle
title: Core Principles of Feature-Based Architecture
description: Fundamental principles of Feature-based Architecture in React, including Colocation, Public API Encapsulation, and Tri-Layer Logic Separation.
tags:
  - architecture
  - colocation
  - encapsulation
  - logic-separation
---

# 1. 設計原則 (Core Architectural Principles)

```mermaid
flowchart TD
    subgraph FeatureDomain["🎯 Feature Module: <domain> (自己完結ドメイン)"]
        direction TB
        PublicAPI["📄 index.ts (Public Interface / 唯一の公式窓口)"]
        UI["🎨 Presentation Layer (UI / Views)"]
        State["⚡ State & Lifecycle Layer (Hooks / Store)"]
        Logic["🧠 Domain Logic Layer (Pure Functions / Rules / Utils)"]
        Data["🌐 Data Access Layer (API / Storage / Services)"]
        Model["📐 Model & Contract Layer (Types / Schemas)"]
        
        UI -.-> PublicAPI
        State -.-> PublicAPI
        Model -.-> PublicAPI
        
        Logic --> State
        Data --> State
        State --> UI
    end

    External["🌐 Application Shell / Routing Layer / Other Features"]
    External -->|Allowed (index.ts 経由のみ)| PublicAPI
```

---

### 原則 1: コロケーション (Colocation)
> **「同じ理由・同じタイミングで変化する要素は、同じドメイン内に配置する」**

UI、状態管理、API通信、ビジネスルール、型、テストを1つのドメインモジュール内に閉じ込めます。ファイルの種類別（components/ や hooks/）にプロジェクト全体へ散らばらせません。

---

### 原則 2: Public API とカプセル化 (Encapsulation)
> **「外部には契約（Public Interface）だけを公開し、内部実装は隠蔽する」**

各ドメインのルートにある `index.ts` が唯一の公開窓口です。ドメイン内部のファイル構造がどう変化・リファクタリングされても、外部の利用コードには影響を与えません。

---

### 原則 3: 関心の分離と3層ロジックモデル (Tri-Layer Logic Separation)
> **「React依存と純粋なビジネスルールを分離する」**

1. **Pure Logic (Utils / Rules)**: React非依存の純粋関数。引数を受け取り結果を返す。最もテストが容易で再利用性が高い。
2. **State & Lifecycle (Hooks)**: React の状態（State）や副作用（Effects）を束ねるオーケストレーター。
3. **Data Access (API / Services)**: 外部通信や永続化のI/O処理。
