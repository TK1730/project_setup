---
type: guideline
title: 'アクセシビリティ（a11y）とセマンティック HTML の基本'
description: 'キーボード操作やスクリーンリーダーを含め誰でも迷わず操作でき、かつ自動テスト（getByRole）も容易になるセマンティック HTML と React 実装の基本原則を解説する。'
tags: [accessibility, a11y, html, react, frontend, testing]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# アクセシビリティ（a11y）とセマンティック HTML の基本

アクセシビリティ（Accessibility, 略して **a11y**）とは、マウスを使わずキーボードだけで操作するユーザーやスクリーンリーダー利用者を含め、あらゆる人が迷わず機能を利用できるようにする設計品質である。意味に合った正しい HTML 要素（セマンティック HTML）を選ぶことは、ユーザー体験を高めるだけでなく、Testing Library の `getByRole` を使った堅牢な自動テストを書きやすくするうえでも最も重要な土台となる。

## 1. `<button>` と `<a href>` と `<div>` の厳密な使い分け

見た目を CSS でボタン風に整えただけの `<div onClick={...}>` や `<span onClick={...}>` を作ってはいけない。`<div>` は本来ただの箱であるため、キーボードの `Tab` キーでフォーカスが当たらず、`Enter` や `Space` キーで押すこともできず、スクリーンリーダーや自動テストからも「操作可能なボタン」として認識されない。

| 要素                                                   | 使うべき場面                                                                                 | ブラウザが標準で提供する機能                                                                               |
| :----------------------------------------------------- | :------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| **`<a href="...">`**（または Next.js `<Link>`）        | **URL が変わり、別ページや別セクションへ遷移するとき**                                       | 右クリックで「新しいタブで開く」、`Cmd/Ctrl + クリック`、ホバー時のリンク先 URL 表示、`Enter` キーでの遷移 |
| **`<button type="button">`**（または `type="submit"`） | **同じ画面内で処理を起こすとき**（タイマー開始・停止、モーダル開閉、削除実行、フォーム送信） | `Tab` キーでのフォーカス移動、`Enter` / `Space` キーでの実行、`disabled` 属性による操作無効化              |
| **`<div>` / `<span>`**                                 | **レイアウトや装飾のためのグループ化**（クリック操作を持たない要素）                         | インタラクション機能なし（`onClick` を付けてはならない）                                                   |

1.  **ページ遷移なら `<a href>`**: 遷移先 URL が存在するナビゲーションは必ず `<a>`（Next.js では `<Link>`）で実装する。`<button onClick={() => router.push(...)}>` にすると、ユーザーが別タブで開けなくなる。
1.  **画面内アクションなら `<button>`**: フォーム内のボタンが意図せずサブミットを発火するのを防ぐため、送信ボタン以外は明示的に `<button type="button">` を指定する習慣をつける。

```tsx
// NG: div に onClick を付けるとキーボード操作も getByRole('button') もできない
<div className="btn" onClick={handleStart}>スタート</div>

// OK: 画面内の操作には必ず button 要素を使う
<button type="button" className="btn" onClick={handleStart}>
  スタート
</button>
```

## 2. フォーム要素とラベルの紐づけ

入力欄（`<input>`, `<select>`, `<textarea>`）やアイコンのみのボタンには、人間が見てもプログラム（支援技術・テストコード）が読んでも何の要素か特定できる **アクセシブルネーム（名前）** を必ず付与する。

1.  **`<input>` には必ず `<label htmlFor>` を紐づける**: `<label htmlFor="task-title">` と `<input id="task-title">` をセットで記述する。これにより、ラベル文字列をクリックしたときにも入力欄へフォーカスが当たり、クリック領域が広がって操作しやすくなる。
1.  **プレースホルダー（`placeholder`）をラベルの代わりにしない**: `placeholder` は文字を入力し始めると消えてしまうため、「何を入力する欄だったか」を確認できなくなる。`placeholder` はあくまで入力例の補助にとどめ、独立した `<label>` を常時表示する。
1.  **アイコンのみのボタンには `aria-label` を付ける**: 「×（閉じる）」や「ゴミ箱アイコン（削除）」など、テキストを持たないボタンには `<button type="button" aria-label="モーダルを閉じる">` のように目的を表すラベルを指定し、装飾用の SVG アイコン自体には `aria-hidden="true"` を付与する。

```tsx
// ラベル紐づけとアイコンボタンの実装例
<div className="form-field">
  <label htmlFor="pomodoro-minutes">作業時間（分）</label>
  <input
    id="pomodoro-minutes"
    type="number"
    placeholder="例: 25"
  />
</div>

<button type="button" aria-label="タスクを削除" onClick={onDelete}>
  <TrashIcon aria-hidden="true" />
</button>
```

## 3. キーボード操作とフォーカス管理

マウスを使わずに `Tab` / `Shift + Tab` キーで画面を移動するとき、**「今どの要素にフォーカスが当たっているか」** が視覚的に一目で分かる状態を維持しなければならない。

1.  **`outline: none` でフォーカス枠を単純に消さない**: ブラウザ標準の枠線がデザインに合わないという理由で `outline: none` だけを指定すると、キーボード利用者が現在位置を完全に失う。必ず **`:focus-visible`** 疑似クラスを使い、キーボード操作時に視認性の高いカスタムフォーカスリングを表示する。
1.  **モーダル（Dialog）のフォーカス管理 3原則**: モーダルダイアログを開く際は、標準の `<dialog>` 要素や Radix UI / Headless UI などのアクセシブルなプリミティブを活用し、以下の3つの挙動を確実に満たす。
    - **フォーカストラップ（Focus Trap）**: モーダルが開いている間、`Tab` キーを押しても背後の画面へフォーカスが抜け出さず、モーダル内の要素だけを循環するようにする。
    - **`Escape` キーで閉じる**: マウスで閉じるボタンを押さなくても、`Esc` キー1つでモーダルを閉じられるようにする。
    - **フォーカスの復帰（Restore Focus）**: モーダルを閉じた直後は、そのモーダルを開くきっかけとなった元のボタンへフォーカスを戻す。

```css
/* マウスクリック時は不要な枠を出さず、キーボード移動時（:focus-visible）に明確なリングを出す */
.button:focus-visible,
.input:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

## 4. 動的な変化の通知（`aria-live`）

SPA（Single Page Application）では、ページ遷移を伴わずに画面の一部だけが非同期で書き換わる。画面を見ているユーザーにはトースト通知やエラー表示が見えても、スクリーンリーダー利用者には変化が伝わらないため、**ライブリージョン（Live Region）** を使って動的な変化を通知する。

1.  **通常の通知・ステータスメッセージには `role="status"`（`aria-live="polite"`）**: 「タスクを保存しました」「検索結果が5件見つかりました」「ポモドーロが完了しました」といった通知には `role="status"` を指定する。現在読み上げ中の内容を遮らず、区切りの良いタイミングで穏やかに通知される。
1.  **緊急性の高いエラーには `role="alert"`（`aria-live="assertive"`）**: フォーム送信失敗や通信切断など、ユーザーの操作を止めてでも即座に伝えるべきエラーメッセージには `role="alert"` を指定する。

```tsx
// 非同期処理の結果をライブリージョンで通知する例
{
  statusMessage && (
    <div role="status" className="toast-notification">
      {statusMessage}
    </div>
  );
}

{
  errorMessage && (
    <div role="alert" className="error-banner">
      {errorMessage}
    </div>
  );
}
```

## See also

- [UI の「4つの状態（Ideal / Loading / Empty / Error）」と操作フィードバック](/learning/ui-and-design/ui-states-and-feedback.md)
- [フロントエンドのテスト戦略（Testing Trophy と Testing Library の原則）](/learning/testing/frontend-testing-strategy.md)
- [MDN Web Docs: Accessibility](https://developer.mozilla.org/ja/docs/Web/Accessibility)
- [Testing Library: About Queries (Priority of getByRole)](https://testing-library.com/docs/queries/about/#priority)
