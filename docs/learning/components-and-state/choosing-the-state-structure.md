---
type: reference
title: 'State の構造の原則（Choosing the State Structure）'
description: 'React 公式ドキュメント「Choosing the State Structure」に基づき、状態の不整合や更新漏れバグを防ぐための5つの State 設計原則を悪い例・良い例の対比とともに整理する。'
tags: [react, state, frontend]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# State の構造の原則（Choosing the State Structure）

React コンポーネントにおけるバグ（画面の表示ズレ、あり得ない状態の組み合わせ、更新漏れ）の多くは、イベントハンドラの書き方ではなく **`useState` の構造設計（どの値を state として持ち、どの値を state に持たないか）** に起因する。React 公式ドキュメント「Choosing the State Structure」が示す5つの原則に従い、状態から「矛盾・冗長・重複・深いネスト」を取り除くことで、状態更新がシンプルになりバグが構造的に発生しないコンポーネントを実現できる。

## State 構造化の5原則

State を設計する際は、常に「最小限のソース・オブ・トゥルース（唯一の情報源）だけで画面のすべての状態を表現できているか」を確認する。以下の5原則は、そのための具体的なチェックリストである。

1.  **関連する state をグループ化する**（Group related state）
1.  **矛盾する state を避ける**（Avoid contradictions in state）
1.  **冗長な state を避ける**（Avoid redundant state）
1.  **state の重複を避ける**（Avoid duplication in state）
1.  **深くネストした state を避ける**（Avoid deeply nested state）

## 1. 関連する state をグループ化する（Group related state）

2つ以上の state 変数が **「常に同じタイミングで一緒に更新される」** のであれば、それらを別々の `useState` に分けるのではなく、1つのオブジェクトまたは配列の state にまとめる。別々にしておくと、将来どちらかの更新を書き忘れた際に不整合が生じるほか、カスタムフックや子コンポーネントへの受け渡しも煩雑になる。

### 悪い例：常に一緒に動く X 座標と Y 座標を別々の state に持つ

```tsx
const [x, setX] = useState(0);
const [y, setY] = useState(0);

function handlePointerMove(e: React.PointerEvent) {
  setX(e.clientX);
  setY(e.clientY);
}
```

### 良い例：1つのオブジェクト state にまとめる

```tsx
const [position, setPosition] = useState({ x: 0, y: 0 });

function handlePointerMove(e: React.PointerEvent) {
  setPosition({
    x: e.clientX,
    y: e.clientY,
  });
}
```

注意点として、オブジェクトや配列を state にまとめた場合は、一部のプロパティだけを更新するときにも必ずスプレッド構文（`setPosition({ ...position, x: 100 })`）などで新しいオブジェクトを生成して渡す必要がある。

## 2. 矛盾する state を避ける（Avoid contradictions in state）

互いに排他的であり「同時に `true` になることは業務上あり得ない」複数の状態を、個別の boolean 型 `useState` で表現してはならない。複数の boolean に分けると、片方を `false` に戻し忘れた際に「送信中（`isSending: true`）でありながら送信完了（`isSent: true`）でもある」という矛盾した状態（Impossible State）が作り出されてしまう。これを防ぐには、とり得る状態を1つの文字列リテラル共用体型（Union Type）の `status` に集約する。

### 悪い例：複数の boolean で進行状態を管理する

```tsx
const [isSending, setIsSending] = useState(false);
const [isSent, setIsSent] = useState(false);

async function handleSubmit() {
  setIsSending(true);
  await sendMessage();
  // NG: もし setIsSending(false) を書き忘れると、isSending と isSent が両方 true になる
  setIsSending(false);
  setIsSent(true);
}
```

### 良い例：単一の `status` ユニオン型で管理する

```tsx
type FormStatus = 'typing' | 'sending' | 'sent';

const [status, setStatus] = useState<FormStatus>('typing');

async function handleSubmit() {
  setStatus('sending');
  await sendMessage();
  setStatus('sent'); // OK: 状態が1つしかないため、sending と sent が同時に成立することは絶対にない
}

// 必要であればレンダー中に読みやすい boolean 定数を導出する
const isSending = status === 'sending';
const isSent = status === 'sent';
```

## 3. 冗長な state を避ける（Avoid redundant state）

コンポーネントの **props や既存の state から、レンダリング中に計算して求められる値（派生値 / Derived State）** を別の `useState` に入れてはならない。派生値を state として保持すると、元の値が変わったときに派生側の state を同期させるための無駄な更新処理や `useEffect` が必要になり、同期漏れによる表示バグの温床になる。React ではレンダリングのたびに関数本体が再実行されるため、単なるローカル変数として計算するだけで常に最新の値が得られる（計算コストが極端に高い場合のみ `useMemo` を使う）。

### 悪い例：計算で求められる `fullName` を state や `useEffect` で同期する

```tsx
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState(''); // NG: 冗長な state

useEffect(() => {
  // NG: 不要な再レンダリングが発生し、データフローも追いにくくなる
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

### 良い例：レンダリング中に通常の変数として計算する

```tsx
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');

// OK: レンダー中に直接計算する（state の数を最小に保てる）
const fullName = `${firstName} ${lastName}`;
```

## 4. state の重複を避ける（Avoid duplication in state）

一覧データ（配列）の中からユーザーが1つを選択・編集するような UI において、**配列内の要素オブジェクト丸ごとを `selectedItem` として別 state にコピーして保持** してはならない。同じデータが2箇所（`items` 配列の中と `selectedItem` の中）に重複して存在すると、`items` 側の内容を更新したときに `selectedItem` 側が古いまま取り残されるという深刻な不整合が発生する。代わりに、選択中の **ID（`selectedId`）だけを state に保持** し、選択中のオブジェクト自体は配列から検索して導出する。

### 悪い例：選択中のオブジェクト丸ごとを state に重複保持する

```tsx
const [items, setItems] = useState(initialItems);
// NG: items の要素と同じオブジェクト内容を丸ごと別 state にコピーしている
const [selectedItem, setSelectedItem] = useState(items[0]);

function handleItemTitleChange(id: number, newTitle: string) {
  setItems(items.map((item) => (item.id === id ? { ...item, title: newTitle } : item)));
  // NG: items は更新されたが、selectedItem.title は古いまま画面に残り続ける
}
```

### 良い例：ID だけを state に持ち、オブジェクトは配列から導出する

```tsx
const [items, setItems] = useState(initialItems);
// OK: ID だけを state として保持する
const [selectedId, setSelectedId] = useState<number>(items[0].id);

// OK: 選択中のオブジェクトはレンダー中に items から検索して導出する
const selectedItem = items.find((item) => item.id === selectedId);

function handleItemTitleChange(id: number, newTitle: string) {
  // OK: items を更新するだけで、次回レンダー時に selectedItem も自動的に最新になる
  setItems(items.map((item) => (item.id === id ? { ...item, title: newTitle } : item)));
}
```

## 5. 深くネストした state を避ける（Avoid deeply nested state）

フォルダツリー、コメントの返信階層、旅行プラン（地域 > 国 > 都市）のように階層構造を持つデータを、そのまま深くネストしたオブジェクト・配列として state に持つと、末端の1要素を更新するだけでも親からルートまで何段階ものスプレッド構文（コピー）を書く必要が生じる。コードが複雑で読みづらくなるため、データベースのテーブル設計と同様に **ID をキーとしたフラットな構造（正規化 / Normalized State）** に平坦化して管理する。

### 悪い例：深い入れ子構造のまま state に保持する

```tsx
// NG: 深い階層構造をそのまま持つと、末端の都市を追加・削除する更新ロジックが極めて複雑になる
const [plan, setPlan] = useState({
  id: 0,
  title: '(Root)',
  childPlaces: [
    {
      id: 1,
      title: 'Asia',
      childPlaces: [
        { id: 2, title: 'Japan', childPlaces: [] },
        { id: 3, title: 'Thailand', childPlaces: [] },
      ],
    },
  ],
});
```

### 良い例：ID をキーにしたフラットなマップ（正規化構造）にする

```tsx
type Place = {
  id: number;
  title: string;
  childIds: number[]; // OK: 子要素のオブジェクト自体ではなく、子の ID 配列だけを持つ
};

// OK: どの階層にある要素でも ID で O(1) で直接参照・更新できる
const [placesById, setPlacesById] = useState<Record<number, Place>>({
  0: { id: 0, title: '(Root)', childIds: [1] },
  1: { id: 1, title: 'Asia', childIds: [2, 3] },
  2: { id: 2, title: 'Japan', childIds: [] },
  3: { id: 3, title: 'Thailand', childIds: [] },
});

function handleRemoveChild(parentId: number, childId: number) {
  const parent = placesById[parentId];
  // OK: 親要素1つを更新するだけで完了し、深い再帰コピーが不要になる
  setPlacesById({
    ...placesById,
    [parentId]: {
      ...parent,
      childIds: parent.childIds.filter((id) => id !== childId),
    },
  });
}
```

## See also

- [React Documentation - Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure)
- [React Documentation - You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [どの部品で State を持ち、どう渡すか（State の所有権とデータフロー）](/learning/components-and-state/react-state-ownership-and-data-flow.md)
- [React の画面の切り替えと state のリセット](/knowledge/react-state-reset-by-position.md)
