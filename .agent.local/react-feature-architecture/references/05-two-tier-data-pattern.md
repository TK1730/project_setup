---
type: architectural-pattern
title: Two-Tier Data Pattern within a Domain
description: Pattern for sharing API data across multiple UI parts within the same domain while isolating View-specific transformations.
tags:
  - data-layer
  - viewmodel
  - dry
  - decoupling
---

# 5. ドメイン内でのAPI共通化とパーツ別データ変換 (Two-Tier Data Pattern)

同一ドメイン内で複数のUIパーツが同じAPIデータを必要とする場合（例: Header, Graph, BillingStatus）、以下の**2層分離アプローチ**を適用します。

```mermaid
flowchart TD
    subgraph DataLayer["🌐 共通データ層 (DRY: 1箇所に集約)"]
        API["features/<domain>/api/get<Domain>.ts\n(純粋API通信関数)"]
        Hook["features/<domain>/hooks/use<Domain>.ts\n(キャッシュ & データ取得Hook)"]
        API --> Hook
    end

    subgraph PartsLayer["🎨 プレゼンテーション層 (パーツごとに閉じる)"]
        PartA["パーツA (<Domain>Header.tsx)\n・use<Domain>() 呼出\n・名前やアバター等の表示加工"]
        PartB["パーツB (<Domain>Summary.tsx)\n・use<Domain>() 呼出\n・集計・ステータス判定の計算"]
    end

    Hook -->|生データ / キャッシュ共有| PartA
    Hook -->|生データ / キャッシュ共有| PartB
```

---

### 分離の基準
- **共通化するもの (DRY)**: 
  API通信関数 (`api/`) と キャッシュ管理Hook (`hooks/`)。重複fetchを防ぎ、データ整合性を担保する。
- **パーツに閉じるもの (疎結合)**: 
  画面表示のための加工・フォーマット・計算（ViewModel変換）。他パーツへの影響を遮断する。
