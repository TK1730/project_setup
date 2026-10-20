---
type: guideline
title: 'UI コンポーネントの粒度と分類（Atomic Design と現代の分類法）'
description: 'Atomic Design の 5 階層と、React 開発で起きやすい分類の迷いを解消する「汎用 UI 部品＋機能固有部品」の 2 層構成の比較。'
tags: [react, components, atomic-design, architecture, frontend]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# UI コンポーネントの粒度と分類（Atomic Design と現代の分類法）

React コンポーネントをどのディレクトリにどう分類するかの考え方である。従来よく使われた **Atomic Design** の特徴と課題を整理し、近年の React / Next.js で主流になっている **「汎用 UI プリミティブ ＋ 機能（Feature）固有コンポーネント」** の分け方を説明する。

## 1. Atomic Design とは何か

Brad Frost が提唱した、UI を化学の単位になぞらえて 5 段階の粒度で組み立てるデザイン手法である。

| 階層                          | 意味                                                 | 具体例                                           |
| :---------------------------- | :--------------------------------------------------- | :----------------------------------------------- |
| **Atoms（原子）**             | これ以上分解できない最小の UI 要素                   | `Button`、`Input`、`Icon`、`Badge`               |
| **Molecules（分子）**         | 複数の Atom を組み合わせた小さな機能単位             | 検索バー（`Input` + `Button`）、ラベル付き入力欄 |
| **Organisms（有機体）**       | Molecule や Atom を組み合わせた画面の独立領域        | ヘッダー、商品カード一覧、タイマー設定パネル     |
| **Templates（テンプレート）** | コンポーネントの配置（レイアウト枠）だけを決めたもの | サイドバー付き 2 カラムレイアウト                |
| **Pages（ページ）**           | Template に実際のデータを流し込んだ最終画面          | ポモドーロタイマー画面                           |

## 2. React 開発で Atomic Design を使うときに起きやすい課題

デザインシステムの視覚カタログとしては優れている一方、React のディレクトリ構成にそのまま当てはめると次の問題が起きやすい。

1.  **Molecules と Organisms の境界で迷う**: 「検索フォームは Molecule か Organism か」「子コンポーネントを1つ足したらディレクトリを移動するのか」という議論に時間を取られやすい。
1.  **「見た目の大きさ」と「業務知識（ドメイン）の有無」が混ざる**: たとえば「ポモドーロ開始ボタン」は見た目は小さくても業務知識を持つ。これを `atoms/` や `molecules/` に置くと、汎用部品置き場に特定機能のロジックや API 型が混入する。
1.  **コンポーネントを探す場所が分散する**: 1つの画面を直すのに `atoms/`・`molecules/`・`organisms/` を横断してファイルを探す必要がある。

## 3. 現代の主流：「汎用 UI」と「機能固有」の 2 軸で分ける

近年の React 設計（Bulletproof React や shadcn/ui を採用する構成）では、**「見た目の大きさ」ではなく「どこで使われるか（業務知識を持つか）」** で分けるのが主流である。

```text
src/
├── components/
│   ├── ui/               # 業務知識を持たない汎用 UI 部品（旧 Atoms + 汎用 Molecules）
│   │   ├── button/
│   │   ├── dialog/
│   │   └── input/
│   └── layouts/          # 画面全体の共通枠（Header, Sidebar 等）
└── features/
    └── pomodoro/
        └── components/   # ポモドーロ機能専用の部品（大小問わずここに置く）
            ├── timer-display/
            └── task-selector/
```

### 判断基準（どちらに置くか）

- **`components/ui/`（または `components/atoms/`）に置くもの**:
  - 別のアプリにそのままコピーしても使える部品（`Button`、`Dialog`、`Tabs`、`Input` など）。
  - ドメインの型（`PomodoroTask` など）や API を一切知らない。
- **`features/<機能名>/components/` に置くもの**:
  - その業務機能の言葉やデータ構造を知っている部品。
  - たとえボタン 1 個の小さな部品でも、特定機能でしか使わないなら `features/` 内に置く。

## 決定理由（Rationale）

「大きさ（Atom / Molecule / Organism）」は主観で揺れるが、「業務知識を持つかどうか（汎用か機能固有か）」は import する型を見れば一意に決まるため、配置場所で迷わなくなる。なお、汎用部品のフォルダ名を `components/atoms/` と呼ぶ場合でも、その中身は「業務知識を持たない汎用 UI プリミティブ」に限定するのが安全である。

## See also

- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/)
- [Bulletproof React の全体像](/learning/architecture/bulletproof-react-overview.md)
- [コンポーネント設計およびモジュール解決ガイドライン](/frontend/component-guidelines.md)
