---
type: reference
title: 'Google HTML/CSS スタイルガイド要約'
description: 'Google HTML/CSS Style Guide の要約（セマンティクス、class 命名、CSS の書き方）。'
tags: [knowledge, google-styleguide, html, css, semantics, accessibility]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# Google HTML/CSS スタイルガイド要約

Google の HTML/CSS スタイルガイドを、React / Next.js 開発者向けに要点だけ要約した参考資料である。外部ガイドの要約であり、本プロジェクトの規約ではない。特に重要なのは、要素を本来の目的で使うこと（セマンティクス）と、クラス名を見た目ではなく役割で付けることの 2 点である。

## HTML

出典の節名を括弧内に示す。

- 要素は本来の目的で使う（Semantics）。見出しには見出し要素、段落には `p`、リンクには `a` を使う。ガイドは `button` や `onClick` に直接触れていないが、この原則に従えば、操作には `button`、遷移には `a` が適切になる。
- 画像などのマルチメディアには代替手段を用意する（Multimedia Fallback）。画像には意味のある `alt` を付ける。
- 構造（マークアップ）・見た目（スタイル）・振る舞い（スクリプト）を厳密に分離する（Separation of Concerns）。
- 妥当な HTML を書く（Validity）。文書の先頭は `<!doctype html>`（Document Type）、文字コードは UTF-8 で `<meta charset="utf-8">` を指定する（Encoding）。
- 画像・スタイルシート・スクリプトは HTTPS で読み込む（Protocol）。
- 小文字のみで書く（Capitalization）。インデントは空白 2 つ（Indentation）。
- スタイルシートとスクリプトの `type` 属性は省略する（type Attributes）。

```html
<!-- 良い例: 目的に合った要素と意味のある alt -->
<button type="button">開始</button>
<img src="timer.png" alt="25 分のタイマー表示" />
```

## CSS

- クラス名は役割を表す意味のある名前か汎用的な名前にする。見た目を表す名前は避ける。語の区切りはハイフンを使い、短く、ただし必要な長さは保つ（ID/Class Naming）。例は `.error-message`（良い）と `.red-text`（悪い）。
- スタイリングに ID セレクタは使わず、クラスセレクタを使う。不要な `id` 属性も避ける（ID Selectors, ID/Class Naming）。
- クラスに要素名を併記しない。ヘルパークラスなど必要な場合を除く（Type Selectors）。例は `.item`（良い）と `li.item`（悪い）。
- `!important` は避ける。カスケードを壊し、スタイルの見通しが悪くなるためである。必要なら詳細度で調整する（Important Declarations）。
- ショートハンドプロパティ（`margin` など）は使えるときに使う（Shorthand Properties）。`0` の単位は省略し（0 and Units）、`0.8em` のように先頭の `0` は省略しない（Leading 0s）。
- 宣言はアルファベット順に並べ、各宣言をセミコロンで終える（Declaration Order, Declaration Stops）。

```css
.error-message {
  margin: 0;
  padding: 0.5em 1em;
}
```

## React / CSS Modules での適用

- JSX の `class` に相当するのは `className` である。HTML の原則（セマンティクス、`alt`、役割ベースの命名）はそのまま当てはまる。
- CSS Modules はクラス名をファイル単位でスコープするため、命名衝突や ID セレクタの必要性は減る。一方で、役割ベースの命名と `!important` の回避は、引き続き有効である。
- ガイドは CSS Modules や CSS-in-JS を想定していない。ハイフン区切りは CSS Modules では `styles['error-message']` のように参照することになるため、採用は各プロジェクトの判断になる。

## See also

- [Markdown の書き方](/guides/markdown-style.md)
- [Google HTML/CSS Style Guide（原典）](https://google.github.io/styleguide/htmlcssguide.html)
