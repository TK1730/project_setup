---
type: architectural-rule
title: Public API & Encapsulation with index.ts
description: Explicit rules for index.ts (Barrel export), internal vs external imports, and module encapsulation.
tags:
  - encapsulation
  - barrel-export
  - public-api
  - imports
---

# 4. `index.ts` によるカプセル化と import 規約

### 1. 内部通信 (Internal Imports)
Feature の内部に存在するファイル同士は、**相対パス**で直接参照します。

```typescript
// 📁 features/<domain>/components/<Domain>Container.tsx
import { use<Domain> } from '../hooks/use<Domain>';
import { calculate<Metric> } from '../utils/<domain>Calculators';
import type { <Domain>Entity } from '../types';
```

---

### 2. 外部公開 (Public Exports via `index.ts`)
Feature の外部（他 Feature やルーティング層）に公開するものは**最小限のインターフェース**に絞ります。

```typescript
// 📁 features/<domain>/index.ts

// ✅ 公開: 外部が利用するエントリーコンポーネント
export { <Domain>Container } from './components/<Domain>Container';

// ✅ 公開: 外部でも共有されるドメイン型
export type { <Domain>Entity, <Domain>Status } from './types';

// ⚠️ 内部専用のサブコンポーネントやユーティリティは export しない
```

---

### 3. 外部からの利用 (Consumer Usage)
利用側はディレクトリの深い階層を指定せず、Feature パスから直接 import します。

```tsx
// 📁 src/app/dashboard/page.tsx
// ✅ GOOD: Public API 経由
import { <Domain>Container } from '@/features/<domain>';

// ❌ BAD: 内部実装への直接アクセス（カプセル化違反）
// import { <Domain>Container } from '@/features/<domain>/components/<Domain>Container';
```
