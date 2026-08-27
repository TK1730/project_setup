---
type: architectural-matrix
title: Shared vs Feature Boundary Matrix
description: Decision matrix for determining whether a component, hook, or utility belongs in the Shared layer or a Feature module.
tags:
  - shared-layer
  - feature-layer
  - boundary-decision
---

# 8. 共通層（Shared）と Feature層の境界判定マトリクス

新しいファイルを作成する際、「共通層（`src/components/` や `src/lib/`）」に置くべきか、「Feature層（`src/features/<domain>/`）」に置くべきかの判断基準です。

| 判定基準 | Feature層 (`src/features/<domain>/`) | 共通層 (`src/components/`, `src/lib/`) |
| :--- | :--- | :--- |
| **業務知識 (Domain Knowledge)** | 含む（特定のビジネスルールやデータ構造に依存） | 含まない（抽象的・汎用的な仕組み） |
| **再利用の範囲** | 同一機能内、または限定的な連携 | アプリケーション全体、別プロジェクトでも流用可能 |
| **削除時の影響** | 当該 Feature フォルダを削除すれば安全に消滅 | 他の多数の画面に影響が出るため慎重な変更が必要 |
