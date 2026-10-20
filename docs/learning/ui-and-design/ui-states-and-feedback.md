---
type: guideline
title: 'UI の「4つの状態（Ideal / Loading / Empty / Error）」と操作フィードバック'
description: 'データ表示コンポーネントにおける状態網羅（Ideal・Loading・Empty・Error・Partial）と、ユーザー操作に対する非同期フィードバック設計の原則をまとめる。'
tags: [react, ui, ux, frontend, state-management]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# UI の「4つの状態（Ideal / Loading / Empty / Error）」と操作フィードバック

画面やデータ表示コンポーネントを実装する際は、データが綺麗に揃った「正常時（Ideal State）」だけを作って終わりにせず、読込中・データ0件・失敗時・極端なデータを含めたすべての状態を最初から設計する必要がある。また、ボタン押下やフォーム送信などのユーザー操作に対しては、「今システムが何をしているか」を即座にフィードバックし、二重送信や操作迷子を防ぐことが不可欠である。

## 画面・データ表示の「4つの状態＋1（UI Stack）」

非同期でデータを取得して表示するすべての画面・コンポーネントは、以下の5つの状態（4つの基本状態＋Partial State）を網羅して実装する。

| 状態                              | 発生するタイミング                                | 設計の最重要ポイント                                                         |
| :-------------------------------- | :------------------------------------------------ | :--------------------------------------------------------------------------- |
| **Ideal State（正常時）**         | データが1件以上正常に取得できたとき               | 情報の優先度（視覚階層）を整理し、主要アクションを見つけやすくする           |
| **Loading State（読込中）**       | API 通信中・初期レンダリング待ちのとき            | レイアウトシフト（ガタつき）を防ぐためスピナーより **Skeleton** を優先する   |
| **Empty State（データ0件）**      | 初回利用時、または検索・フィルタ結果が0件のとき   | 「なぜ空なのか」の理由と「次に押すべきアクション」を必ずセットで配置する     |
| **Error State（失敗時）**         | 通信エラーやサーバーエラーが発生したとき          | 原因の分かりやすい説明と「再試行（Retry）」導線を置き、入力内容を消さない    |
| **Partial State（極端なデータ）** | 1件のみのとき、または文字数・件数が極端に多いとき | 長文の省略（`ellipsis`）や折り返し、数値の桁あふれによるレイアウト崩れを防ぐ |

### 1. Ideal State（正常時）

データが十分に揃っている標準状態であり、デザインカンプや仕様書で最初に描かれる画面である。ただし実際のプロダクトでは、ユーザーがこの状態を見る前に必ず Loading State や Empty State を通過するため、Ideal State だけを実装してタスク完了としてはならない。

### 2. Loading State（読込中）

データの取得中に画面の中央へ小さなスピナー（回転アイコン）だけを置くと、データ取得完了時に突然要素が押し下げられる **レイアウトシフト（CLS: Cumulative Layout Shift）** が発生し、ユーザーの視線やクリック位置がずれてしまう。そのため、読込中は最終的な Ideal State の骨格を模した **Skeleton（スケルトン）** を表示し、表示領域のサイズと高さをあらかじめ確保することを原則とする。

1.  **Skeleton を優先する**: カード一覧、テーブル行、プロフィール欄など、表示される要素のおおよその高さ・幅が分かっている箇所では Skeleton コンポーネントを表示する。
1.  **高速応答時のチラつきを防ぐ**: 通信が 100〜200ms 以内に完了する高速な環境で一瞬だけ Skeleton やスピナーが表示されると、かえって画面がチラついて見えるため、必要に応じて CSS アニメーションの遅延表示やキャッシュ（Stale-While-Revalidate）を活用する。
1.  **どこが読込中かを明確にする**: 画面全体の遷移なのか、特定セクションの再取得なのかに応じて、Skeleton を出す範囲を限定する。

### 3. Empty State（データ0件）

データが0件のときに「データがありません」という文字列だけを表示すると、ユーザーは「バグで表示されていないのか」「まだ登録していないのか」「次に何をすればよいのか」が分からず行き止まりになる。Empty State では **「初回利用時（まだ一度も作っていない）」** と **「検索・フィルタ結果が0件のとき」** を明確に区別し、それぞれの理由と次のアクション（CTA: Call To Action）を提示する。

1.  **初回利用時（Onboarding Empty State）**: 「まだタスクが登録されていません。最初のタスクを追加してポモドーロを始めましょう」のように価値を伝え、すぐ下に「＋ タスクを追加」ボタンを配置する。
1.  **検索・フィルタ結果0件時（No Results State）**: 「『〇〇』に一致するタスクは見つかりませんでした」と条件を明示し、「検索条件をクリアする」ボタンを配置して1クリックで元の状態に戻れるようにする。

### 4. Error State（失敗時）

ネットワーク切断やサーバー障害で通信が失敗した際、コンソールにだけエラーを出して画面を真っ白にしたり、読込中スピナーを無限に回し続けたりしてはならない。ユーザーに何が起きたかを平易な言葉で伝え、自分で復旧を試みられる導線を用意する。

1.  **分かりやすい説明と Retry 導線**: `500 Internal Server Error` のような生ログではなく、「データの読み込みに失敗しました。通信環境をご確認のうえ、もう一度お試しください」というメッセージとともに **「再試行（Retry）」ボタン** を配置する。
1.  **ユーザーの入力内容を絶対に消さない**: フォーム送信時にエラーが起きた場合、ユーザーがせっかく入力したテキストをリセットしてはならない。入力値を保持したままエラーメッセージを表示し、そのまま再送信できるようにする。

### 5. Partial State（極端なデータ・境界値）

モックデータでは綺麗に揃って見えても、本番データでは極端な件数や文字数が入力されるため、境界値での表示崩れをあらかじめ防いでおく。

1.  **データが1件だけのとき**: グリッドレイアウトやリストで要素が1件しかない場合に、カードが不自然に横へ引き伸ばされたり、フッターが画面中央まで浮き上がったりしないか確認する。
1.  **文字数が極端に長いとき（長文・URL・連続した英数字）**: タイトルが100文字ある場合やスペースのない長い英単語が入った場合に備え、1行に収める箇所には `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;`（または複数行制限の `line-clamp`）を指定し、本文領域には `overflow-wrap: break-word;` を指定して親要素からの突き抜けを防ぐ。

```tsx
// データ表示コンポーネントで 4つの状態を網羅する構成例
export function TaskListSection({
  tasks,
  isLoading,
  error,
  searchQuery,
  onRetry,
  onClearSearch,
  onCreateClick,
}: Props) {
  if (isLoading) {
    return <TaskListSkeleton count={4} />;
  }

  if (error) {
    return (
      <div role="alert" className="error-state">
        <p>タスクの読み込みに失敗しました。時間をおいて再度お試しください。</p>
        <button type="button" onClick={onRetry}>
          再試行する
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    if (searchQuery) {
      return (
        <div className="empty-state">
          <p>「{searchQuery}」に一致するタスクは見つかりませんでした。</p>
          <button type="button" onClick={onClearSearch}>
            検索条件をクリア
          </button>
        </div>
      );
    }
    return (
      <div className="empty-state">
        <p>まだタスクがありません。最初のタスクを作成して作業を始めましょう。</p>
        <button type="button" onClick={onCreateClick}>
          ＋ タスクを作成
        </button>
      </div>
    );
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className="task-item">
          <span className="task-title">{task.title}</span>
        </li>
      ))}
    </ul>
  );
}
```

## ユーザー操作（ボタン押下・フォーム送信）へのフィードバック

画面表示だけでなく、ユーザーがボタンを押してから処理が完了するまでの **アクションの状態遷移（Idle → Pending → Success / Error）** も明確に設計する必要がある。クリックしても画面に何も変化がないと、ユーザーは「押せていない」と判断してボタンを連打し、データの二重登録や意図しない課金・API 負荷を引き起こす。

### 1. アクションの4状態（Idle → Pending → Success / Error）

1.  **Idle（待機中）**: 操作可能な初期状態。ホバーやフォーカス時に視覚的な変化を与え、押せる要素であることを示す。
1.  **Pending（処理中）**: ボタンが押された直後の状態。必ずボタンを `disabled`（または `aria-disabled="true"`）にして **二重送信を防止** し、ボタン内にスピナーを表示するかラベルを「保存中...」に変更して処理が進行中であることを伝える。このときボタンの横幅が変わるとガタつくため、`min-width` 等で幅を維持するとよい。
1.  **Success（成功）**: 処理が完了した状態。モーダルを閉じる、一覧を更新する、あるいは「保存しました」というトースト通知やチェックアイコンで完了を伝える。
1.  **Error（失敗）**: 処理が失敗した状態。Pending を解除してボタンを再度押せる状態に戻し、どの項目がなぜ失敗したのかをフォームの近くまたはアラート領域に明示する。

```tsx
// フォーム送信ボタンでの二重送信防止と Pending フィードバック例
export function SaveButton({ isPending }: { isPending: boolean }) {
  return (
    <button type="submit" disabled={isPending} aria-busy={isPending} className="submit-button">
      {isPending ? '保存中...' : '変更を保存'}
    </button>
  );
}
```

### 2. Optimistic UI（楽観的更新）の使いどころ

サーバーからの応答を待たずに、ユーザーが操作した瞬間に「成功したものとみなして」画面を即座に書き換える手法を **Optimistic UI（楽観的更新）** と呼ぶ。体感速度を劇的に向上させられる一方で、万が一通信が失敗した際には元の状態へ巻き戻し（ロールバック）てエラー通知を出す必要があるため、操作の性質によって使い分ける。

1.  **Optimistic UI が適している操作**: タスクの完了チェックボックスの ON/OFF、お気に入り（いいね）トグル、並び替えなど、**頻度が高く・99%以上成功し・失敗してもすぐやり直せる軽微な操作**。
1.  **Optimistic UI を避けるべき操作**: 決済処理、アカウントやデータの完全削除、複雑なサーバー側バリデーションを伴うフォーム作成など、**失敗時の影響が大きい操作や確定結果を見るまで成否が分からない操作**。これらは必ず Pending（スピナー表示）を経てサーバーの確定レスポンスを待つ。

## See also

- [エンジニアが知っておくべき UI 視覚デザインの原則](/learning/ui-and-design/ui-visual-design-principles.md)
- [アクセシビリティ（a11y）とセマンティック HTML の基本](/learning/ui-and-design/web-accessibility-basics.md)
- [How to Fix the UI Stack (Scott Hurff)](https://www.scotthurff.com/posts/why-your-user-interface-is-awkward-youre-ignoring-the-ui-stack/)
- [React Documentation: Managing State](https://react.dev/learn/managing-state)
