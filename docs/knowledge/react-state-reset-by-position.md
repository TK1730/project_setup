---
type: guideline
title: 'React の画面の切り替えと state のリセット'
description: 'React の state がツリー上の位置で管理されることを使い、画面を切り替えたときに state を作り直す設計の指針。'
tags: [knowledge, frontend, react, state, lifecycle]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-18T00:00:00Z }
stale_after: 2027-10-18T00:00:00Z
---

# React の画面の切り替えと state のリセット

React の state は、コンポーネントがツリーのどの位置に描画されているかで管理される。同じ位置に別のコンポーネントを描画すると、前のコンポーネントの state は捨てられる。これを使い、画面ごとに「フックを呼ぶコンポーネント」を分けて出し分けると、画面に入るたびに state が初期値から作り直され、外から state を上書きする処理が要らなくなる。

## 1. 仕組み

- React は、state をどのコンポーネントのものとして持つかを、ツリー上の位置で決める。[^preserving]
- 同じ位置に同じコンポーネントを描画し続ける限り、props が変わっても state は残る。[^preserving]
- 同じ位置に別のコンポーネントを描画すると、その下のツリーの state はすべて捨てられる。[^preserving]
- 同じコンポーネントでも、`key` を変えると別物として扱われ、state が作り直される。[^preserving][^no-effect]
- `useState(initialState)` の `initialState` は、最初の描画のときだけ使われ、それ以降は無視される。[^usestate]

## 2. 画面の切り替えに使う

```tsx
// 入口: 今どちらの画面かと、画面の間で受け渡す値だけを持つ
return phase === 'setup' ? (
  <SetupScreen
    onStart={(seconds) => {
      setSeconds(seconds);
      setPhase('timer');
    }}
  />
) : (
  <TimerScreen seconds={seconds} />
);
```

- `TimerScreen` の中で呼ぶフック（`useState(seconds * 1000)` など）は、`phase` が `timer` になった時点で初めて動くので、選んだ値で始まる。
- `setup` に戻ると `TimerScreen` が取り除かれ、その中の state も捨てられる。次に開始したときは、また新しく作られる。

## 3. 避けたい形

入口で両方の画面のフックを呼んでおき、値が決まったら state を上書きする形は避ける。

- `useState` の初期値は最初の 1 回しか読まれないので、後から決まった値は `useEffect` や `reset` の呼び出しで上書きするしかない。
- props が変わったときに `useEffect` で state を初期値に戻すのは、React 公式が避けるよう勧めている形である。代わりに `key` やコンポーネントの出し分けで作り直す。[^no-effect]
- 下の層（フック）が持つ state を、外側で辻褄を合わせて管理することになり、状態の持ち主が 2 か所に分かれる。

## 決定理由（Rationale）

- 画面の「始まり」と「終わり」を、コンポーネントのマウントとアンマウントに一致させると、初期化と後片付けを React に任せられる。自分で書くリセット処理が減り、リセットし忘れも起きない。
- 画面ごとにフックを呼ぶコンポーネントを分けると、それぞれの画面が必要なフックだけを呼ぶ。開始前の画面ではタイマーのフックが動かない。

## See also

- [Next.js の app/ と features/ の分担](/knowledge/nextjs-app-and-features.md)
- [React カスタムフックの責務分離とライフサイクル設計指針](/knowledge/react-hook-separation-and-lifecycle.md)

[^preserving]: [React: Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)。"When you render a different component in the same position, it resets the state of its entire subtree." とある。

[^usestate]: [React: useState](https://react.dev/reference/react/useState) の Parameters。`initialState` について "This argument is ignored after the initial render." とある。

[^no-effect]: [React: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) の "Resetting all state when a prop changes"。props の変化に合わせて Effect で state を戻すのではなく、`key` を渡して作り直す方法を示している。
