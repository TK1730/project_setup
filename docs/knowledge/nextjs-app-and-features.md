---
type: guideline
title: 'Next.js の app/ と features/ の分担'
description: 'Next.js の App Router で、app/ をルーティング専用の薄い入口にし、機能のコードを features/ にまとめる指針。'
tags: [knowledge, frontend, nextjs, architecture, package-by-feature]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-18T00:00:00Z }
stale_after: 2027-10-18T00:00:00Z
---

# Next.js の app/ と features/ の分担

`app/` は URL と画面を結び付けるだけの薄い入口にし、画面の組み立てや機能のコードは `features/<機能名>/` に置く。feature は「画面 1 枚」ではなく「関心ごと（ドメイン）1 つ」の単位であり、1 つの feature が複数の画面を持ってよい。URL を変えても feature の中を触らずに済むようにするための分担である。

## 1. 役割の分担

| 場所                              | 役割                                                      | 例                                      |
| :-------------------------------- | :-------------------------------------------------------- | :-------------------------------------- |
| `app/<segment>/page.tsx`          | どの URL に何を出すかを決め、feature の入口を差し込むだけ | `app/page.tsx` が `<Pomodoro />` を返す |
| `features/<機能名>/<機能名>.tsx`  | feature の入口。その機能の画面を組み立てる                | `features/pomodoro/pomodoro.tsx`        |
| `features/<機能名>/{api,hooks,…}` | その機能だけで使う部品                                    | `api/create-pomodoro.ts`                |
| `components/`・`lib/`             | 複数の機能で共有する部品                                  | `components/atoms/button`・`lib/timer`  |

依存の向きは `共有（components/・lib/）→ features/ → app/` の一方向にする。feature から別の feature を import せず、複数の feature を組み合わせたいときは `app/` 側で組み合わせる。[^bulletproof]

## 2. feature の中のフォルダ

feature の中は、必要なものだけを置く。[^bulletproof]

```text
features/<機能名>/
├── api/         # API の呼び出し
├── components/  # この機能だけで使うコンポーネント
├── hooks/       # この機能だけで使うフック
├── stores/      # 状態管理
├── types/       # 型
└── utils/       # 小さな関数
```

画面にあたるコンポーネント（フックを呼んで見た目の部品に渡すもの）を置くフォルダは、一般的な決まりがない。参照した bulletproof-react には `screens/` のようなフォルダはなく、画面も `components/` に入る形である。独自のフォルダを作るなら、その理由をこのリポジトリの文書に書いておく。

## 3. URL を 1 つにして画面を切り替えるとき

1 つの URL の中で画面を切り替える（例: 開始前の画面とタイマーの画面）なら、切り替えは feature の入口が持つ。`app/` に「今どちらの画面か」を持たせると、feature の内側の都合が `app/` に漏れる。切り替えたときの state の扱いは [React の画面の切り替えと state のリセット](/knowledge/react-state-reset-by-position.md) を参照する。

URL を分けたい（ブラウザの「戻る」で前の画面に戻したい、画面を直接開きたい）なら、`app/` にページを足し、それぞれのページが feature の入口を差し込む。

## 決定理由（Rationale）

- Next.js 自体はファイルの整理の仕方を決めていない（unopinionated）。公式ドキュメントは方針の 1 つとして「プロジェクトのファイルを `app` の外に置き、`app` をルーティング専用にする」を挙げ、どの方針でもチームで一貫させることを勧めている。[^nextjs]
- `app/` を薄くすると、URL の変更（ページの移動、分割）が feature の中に波及しない。逆に feature を別の URL に置き直すときも、差し込む 1 行を動かすだけで済む。
- feature を関心ごとの単位にするのは、backend の [Package by Feature](/knowledge/package-by-feature.md) と同じ境界を frontend でも共有するためである。

## See also

- [Package by Feature 設計指針](/knowledge/package-by-feature.md)
- [React の画面の切り替えと state のリセット](/knowledge/react-state-reset-by-position.md)
- [モジュールインポートのパス設計ルール](/frontend/import-path-rules.md)
- [コンポーネント設計およびモジュール解決ガイドライン](/frontend/component-guidelines.md)

[^nextjs]: [Next.js: Project structure and organization](https://nextjs.org/docs/app/getting-started/project-structure) の "Organizing your project" と "Store project files outside of app"。

[^bulletproof]: [bulletproof-react: docs/project-structure.md](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)。コードの大半を `features/` に置くこと、依存を `shared → features → app` の一方向にすること、feature 同士を import せず app 側で組み合わせることを勧めている。
