---
type: reference
title: 'Google TypeScript スタイルガイド要約（参考）'
description: 'Google TypeScript Style Guide の要約（型、null と undefined、export、例外）。'
tags: [typescript, styleguide, google, nextjs, react, reference]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# Google TypeScript スタイルガイド要約（参考）

Google TypeScript Style Guide を Next.js / React フロントエンド向けに要約した外部ガイドの参考資料である。型は `any` より `unknown`、`as` や `!` は避ける、named export を使う、が中心で、Next.js の規約と衝突する点（default export、`@/` エイリアス）は例外として扱う。

出典の各項目はセクション名を併記している。ツール設定の項目のうち、ガイドに記載がないものは一般的なプラクティスとして区別する。

## 型の使い方

### オブジェクト型は interface（Type System: Prefer interfaces over type literal aliases）

オブジェクトの型には、オブジェクトリテラルの type alias ではなく interface を使う。

```ts
interface TimerState {
  remaining: number;
  running: boolean;
}
```

- ガイドが述べているのはオブジェクト型についてのみである。ユニオン、タプル、プリミティブの別名は type alias で書く（interface では表現できない）。
- React の props は type alias で書かれることも多い。チーム内で一貫していることを優先する。

### any を避け unknown を使う（Type System: any Type）

`any` はあらゆる型への代入とプロパティ参照を許すため危険である。中身が不明な値には `unknown` を使い、絞り込んでから参照する。API レスポンスや `catch` で受けた値が典型例である。

```ts
const data: unknown = await res.json(); // 検証してから使う
```

### 型アサーションと非 null アサーション（Control structures: Type and non-nullability assertions）

`x as T` と `y!` は安全でないため、明白な理由か明示的な根拠がない限り使わない。`@ts-ignore`、`@ts-expect-error`、`@ts-nocheck` も使わない。

```ts
if (el === null) return; // el! ではなく実行時チェックで絞り込む
```

## null と undefined

### 省略可能は `?` で書く（Type System: Prefer optional over |undefined）

省略可能なフィールドや引数は `field?: T` で表し、`T | undefined` にはしない。

```ts
interface Options {
  label?: string;
}
```

### type alias に null / undefined を含めない（Type System: Nullable/undefined type aliases）

type alias のユニオンに `| null` や `| undefined` を含めない。含めると、null 許容の扱いが利用側の抽象化層を越えて広がるためである。null 許容は使う場所で付ける。

```ts
type UserId = string; // type UserId = string | null は避ける
```

### 等価比較（Control structures: Equality checks）

`===` と `!==` を使う。例外として、リテラル `null` との比較に限り `== null` / `!= null` で null と undefined を同時に判定してよい。

```ts
if (value == null) return; // null と undefined の両方
```

## export と import

### named export のみ（Source file structure: Exports）

すべてのコードで named export を使い、default export は使わない。import の書き方が統一されるためである。

```ts
export function Timer() {
  /* ... */
}
```

Next.js との衝突: `page.tsx`、`layout.tsx`、`loading.tsx` などのルーティング用ファイルは default export を要求する。ガイドはこれを想定していないため、フレームワークが要求するファイルは例外として default export にし、それ以外は named export にするのが現実的な運用である（これは要約者の整理であり、ガイドの記述ではない）。

### 相対 import（Source file structure: Import paths）

同じプロジェクト内のファイルへは、絶対パスではなく相対 import（`./foo`）を使うことをガイドは推奨している（should）。Next.js では `tsconfig.json` の `paths` による `@/` エイリアスが一般的で、この推奨とは異なる。採用する場合はプロジェクト内で規約として明文化し、混在させない。

## 例外

出典: Control structures: Exception handling。

- `Error` またはそのサブクラスのみを throw する。文字列やオブジェクトを throw しない。
- try ブロックは、可読性を損なわない範囲で小さく保つ。
- 例外を捕捉して何もしないことはほとんど正しくない。空の catch にする場合は、理由をコメントで説明する。

```ts
try {
  await save();
} catch {
  /* 失敗しても UI 状態は変わらないため無視する */
}
```

## 命名

出典: Naming。

- クラス、interface、type、enum、React コンポーネントは `UpperCamelCase`。変数、関数、プロパティ、メソッドは `lowerCamelCase`。グローバル定数は `CONSTANT_CASE`。
- 略語は単語として扱う。`loadHttpUrl` とし、`loadHTTPURL` とはしない。
- `const enum` は使わず、通常の `enum` を使う。
- 識別子の先頭や末尾に `_` を付けない。

## ツールで強制する

ガイド自体は tsconfig の `strict` や ESLint に触れていない（`tsetse` / `tsec` という Google 内部の適合性チェックのみ言及）。以下は上記のルールを機械的に守らせるための一般的なプラクティスである。

- tsconfig で `"strict": true` を有効にする。
- ESLint で `@typescript-eslint/no-explicit-any`（any の禁止）、`@typescript-eslint/no-non-null-assertion`（`!` の禁止）、`@typescript-eslint/ban-ts-comment`（`@ts-ignore` の禁止）を有効にする。
- `eqeqeq` を `["error", "always", { "null": "ignore" }]` に設定すると、`== null` だけを許可できる。
- default export の禁止は `import/no-default-export` などで行い、`page.tsx` などのフレームワーク用ファイルは `overrides` で除外する。

## See also

- [命名パターン](/knowledge/naming-patterns.md)
- [括弧と文字のルール](/knowledge/bracket-and-character-rules.md)
- [Google TypeScript Style Guide（出典）](https://google.github.io/styleguide/tsguide.html)
