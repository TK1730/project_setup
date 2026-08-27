---
type: quality-checklist
title: Feature Architecture Quality & Review Checklist
description: Verification checklist for human developers and AI agents during feature development and pull request reviews.
tags:
  - code-review
  - quality-assurance
  - checklist
---

# 9. 開発・レビュー時品質チェックリスト (Quality Checklist)

コード実装時や Pull Request レビュー時に、人間および AI エージェントが以下の項目を検証します。

- [ ] **凝集度**: 特定機能の変更時に、複数の離れたディレクトリを行き来せず 1つの Feature ディレクトリ内で作業が完結しているか？
- [ ] **カプセル化**: 外部コードが Feature 内部の非公開ファイル（サブコンポーネントや内部ヘルパー）を直接 import していないか？
- [ ] **テスタビリティ**: 計算ロジックやビジネスルールが React Hook から純粋関数（Utils）として分離され、単体テスト可能になっているか？
- [ ] **段階的スケーリング**: 機能の規模に対して過剰に深いフォルダ階層を作らず、適切なレベル（Minimal / Standard / Enterprise）を選択しているか？
- [ ] **単方向依存**: クロスドメイン参照時に、相互依存（循環参照）が発生していないか？
- [ ] **スマート/ダム分離**: 汎用UI部品（Avatar, Button等）がドメイン知識やAPI Hookを持たず、純粋に Props のみを受け取っているか？
