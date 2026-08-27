---
type: architectural-pattern
title: Server State Cache & Smart vs Dumb Components
description: Best practices for using TanStack Query / SWR caches to eliminate prop drilling, and guidelines for Smart (Container) vs Dumb (Presentational) components.
tags:
  - tanstack-query
  - swr
  - server-state
  - smart-dumb-components
  - prop-drilling
---

# 7. サーバー状態キャッシュと Smart vs Dumb コンポーネント設計

TanStack Query や SWR などのキャッシュライブラリを導入している場合、親からの深い Props バケツリレー（Prop Drilling）を回避し、**各画面パーツが直接共通 Hook を参照するパターン**が推奨されます。

```mermaid
flowchart TD
    subgraph Traditional["❌ 従来の React (Props バケツリレー)"]
        Parent["親コンポーネント\n(fetchしてState保持)"] -->|props| Child["子コンポーネント"]
        Child -->|props (バケツリレー)| GrandChild["孫コンポーネント\n(データを使う場所)"]
    end

    subgraph Modern["✅ キャッシュ共有時代 (欲しい場所で直接Hook呼出)"]
        Cache["🧠 グローバルキャッシュ\n(queryKey: ['users'])"]
        CompA["画面パーツ A\nuseUsers() を直接呼出"]
        CompB["画面パーツ B\nuseUsers() を直接呼出"]
        
        Cache <-->|自動リクエスト統合 & キャッシュ共有| CompA
        Cache <-->|自動リクエスト統合 & キャッシュ共有| CompB
    end
```

---

### Smart Component vs Dumb Component の使い分け

| コンポーネント種別 | 推奨する実装 | 理由 |
| :--- | :--- | :--- |
| **画面パーツ (Smart / Container)**<br>例: `UserHeader`, `UserBillingCard` | 👉 **`useUsers()` を直接呼ぶ** | 親のバケツリレーを排除し、コンポーネント単位で自由に移動・配置できるようにするため |
| **汎用UI部品 (Dumb / Presentational)**<br>例: `Avatar`, `Button`, `Badge` | 👉 **Props で値を受け取る** | API やドメインを知らない純粋な部品にし、全画面で100%再利用できるようにするため |
