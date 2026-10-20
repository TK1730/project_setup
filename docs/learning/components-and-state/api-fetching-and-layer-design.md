---
type: reference
title: 'React / Next.js における API 通信の設計と呼び場所'
description: 'React と Next.js（App Router）において、API 通信コードをどのディレクトリのファイルに配置し、どのコンポーネント・どのタイミングで呼び出すべきかの設計原則を整理する。'
tags: [frontend, react, nextjs, api, data-fetching, architecture]
status: draft
verified: { by: antigravity/claude-opus-4-6, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# React / Next.js における API 通信の設計と呼び場所

「API をどこで呼ぶべきか」という疑問は、**① 通信コードをどのファイルに置くか（アーキテクチャ上の配置）** と **② どのコンポーネントのどのタイミングで実行するか（コンポーネント上の呼び場所）** の 2 つに分けて整理すると明確に判断できる。UI コンポーネントの中に `fetch()` の URL や通信処理を直接書かず `features/<機能名>/api/` に切り出すこと、初期表示のデータ取得（GET）は Server Component で行い、ユーザー操作による更新（POST / PUT / DELETE）は Client Component のイベントハンドラから直接呼ぶこと（`useEffect` で API を呼ばないこと）が現代の React / Next.js 開発における標準原則である。

## なぜ「API の呼び場所」で迷うのか

React や Next.js を学び始めた際、「API の呼び場所がわからない」と悩む原因の多くは、性質の異なる 2 つの問題が同時に絡み合っていることにある。

1. **ファイルの置き場所（ディレクトリ設計）**: `fetch('/api/...')` のような通信処理を、コンポーネントファイル（`.tsx`）の中に直接書いてよいのか、別ファイルに切り出すならどのフォルダに置くべきか。
1. **コンポーネントと実行タイミング（コンポーネント設計）**: ページの親（`page.tsx`）と子コンポーネントのどちらで呼ぶべきか、Server Component と Client Component のどちらで呼ぶべきか、`useEffect` と `onClick` のどちらで呼ぶべきか。

この 2 つの観点を順番に整理することで、どの機能を作るときも同じ基準で迷わず実装できるようになる。

## ファイルの置き場所：API レイヤの 2 層構成

Bulletproof React の API Layer ガイドラインや OpenAPI を用いたスキーマ駆動開発では、**UI コンポーネント（`.tsx`）の中に URL パスや HTTP ヘッダの設定を直接書かない**ことを原則としている。API 通信に関するファイルは、役割に応じて次の 2 層に分けて配置する。

| 配置場所                                                   | 役割                                                                                                                                                                                                    | 具体的なファイル例                                                               |
| :--------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------- |
| **`src/lib/api-client.ts`**<br>（共通 API クライアント層） | アプリ全体で 1 つだけ用意する通信の土台。ベース URL の設定、認証トークンや Cookie の付与、共通エラー処理（401 未認証や 500 エラーの変換）を担う。OpenAPI から自動生成したクライアントの設定もここで行う | `src/lib/api-client.ts`                                                          |
| **`src/features/<機能名>/api/`**<br>（機能別 API 層）      | 各機能で必要な個別のエンドポイント呼び出し関数（一覧取得、詳細取得、新規作成、更新、削除）を定義する。コンポーネントからはこの関数を呼び出す                                                            | `src/features/tasks/api/get-tasks.ts`<br>`src/features/tasks/api/create-task.ts` |

このように分けることで、「バックエンドの URL やレスポンス形式が少し変わった」「認証ヘッダの付け方を変えたい」といった変更が起きたときに、画面の UI コンポーネントを一切触らずに API 層の修正だけで対応できる。

```ts
// 1. 共通 API クライアント層 (src/lib/api-client.ts)
const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080';

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }

  return res.json() as Promise<T>;
}
```

```ts
// 2. 機能別 API 層 (src/features/tasks/api/get-tasks.ts)
import { apiFetch } from '@/lib/api-client';
import type { Task } from '../types';

export async function getTasks(): Promise<Task[]> {
  return apiFetch<Task[]>('/api/v1/tasks', {
    cache: 'no-store',
  });
}
```

```ts
// 2. 機能別 API 層 (src/features/tasks/api/create-task.ts)
import { apiFetch } from '@/lib/api-client';
import type { CreateTaskInput, Task } from '../types';

export async function createTask(input: CreateTaskInput): Promise<Task> {
  return apiFetch<Task>('/api/v1/tasks', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}
```

## コンポーネント上の呼び場所とタイミング：3 つの基本パターン

次に、作成した API 関数を「どのコンポーネントの、どこから呼ぶか」を決める。Next.js（App Router）では、やりたい処理の性質によって呼び場所が次の 3 パターンに分かれる。

| パターン                                            | やりたいこと                                                   | 呼ぶコンポーネント                              | 呼ぶ場所・タイミング                                                                             |
| :-------------------------------------------------- | :------------------------------------------------------------- | :---------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| **① 初期表示のデータ取得（GET）**                   | 画面を開いたときに一覧や詳細データを表示する                   | **Server Component**<br>（`'use client'` なし） | コンポーネント関数の直下で **`await` して呼ぶ**                                                  |
| **② ユーザー操作による更新（POST / PUT / DELETE）** | ボタンを押した・フォームを送信したときにデータを保存・削除する | **Client Component**<br>（`'use client'` あり） | **`onClick` や `onSubmit` などのイベントハンドラ関数の中**で呼ぶ（または Server Actions を呼ぶ） |
| **③ ブラウザ操作に応じた動的な再取得（GET）**       | 入力中のリアルタイム検索候補、無限スクロール、定期ポーリング   | **Client Component**<br>（`'use client'` あり） | **TanStack Query や SWR** などのデータ取得フック経由で呼ぶ                                       |

### パターン ①：初期表示のデータ取得（Server Component）

画面を開いたときに最初から表示したいデータは、ブラウザ側（Client Component）ではなくサーバー側（Server Component）で `async / await` を使って取得する。サーバー上でデータを取得してから HTML を組み立てるため、ローディング用の State（`isLoading`）を手動で管理する必要がなく、ブラウザに余計な通信コードも送られない。

```tsx
// src/app/tasks/page.tsx（Server Component）
import { getTasks } from '@/features/tasks/api/get-tasks';
import { TaskList } from '@/features/tasks/components/task-list';
import { CreateTaskForm } from '@/features/tasks/components/create-task-form';

export default async function TasksPage() {
  // Server Component の中で直接 await して呼ぶ
  const tasks = await getTasks();

  return (
    <main>
      <h1>タスク一覧</h1>
      <CreateTaskForm />
      <TaskList tasks={tasks} />
    </main>
  );
}
```

### パターン ②：ボタン押下・フォーム送信でのデータ更新（Client Component のイベントハンドラ）

ユーザーのクリックやフォーム送信をきっかけに発生する API 通信（登録・更新・削除）は、Client Component の**イベントハンドラ（`handleSubmit` や `handleClick`）の中**で直接呼び出す。通信完了後に画面の一覧データを最新化したい場合は、Next.js の `useRouter().refresh()` を呼ぶことで Server Component のデータを再取得できる。

```tsx
// src/features/tasks/components/create-task-form.tsx（Client Component）
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createTask } from '../api/create-task';

export function CreateTaskForm() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // イベントハンドラの中で API を呼ぶ（useEffect は使わない）
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!title.trim() || isSubmitting) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await createTask({ title });
      setTitle('');
      // Server Component（一覧画面）のデータを再取得して画面を更新する
      router.refresh();
    } catch {
      setErrorMessage('タスクの作成に失敗しました。もう一度お試しください。');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="新しいタスクを入力"
      />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '追加中...' : '追加'}
      </button>
      {errorMessage && <p role="alert">{errorMessage}</p>}
    </form>
  );
}
```

## 親（`page.tsx`）で呼ぶか、子コンポーネントで呼ぶか

Server Component でデータを取得するとき、「ページの入り口である `page.tsx` でまとめて呼んで Props で子に渡すべきか、それともデータを表示する子コンポーネント自身の中で呼ぶべきか」という設計判断が生じる。Next.js 公式ドキュメントや『Next.js の考え方』（Data Fetch Colocation）では、次の基準で使い分けることが推奨されている。

### 1. `page.tsx` でまとめて取得し Props で渡す場合

ページ内の複数のコンポーネントが同じデータを使う場合や、画面がシンプルでページ全体を一度に表示したい場合は、`page.tsx` で取得して子に Props で渡すのが最もわかりやすい。複数の API を `page.tsx` で呼ぶ場合は、1 つずつ順番に `await` すると通信の順番待ち（ウォーターフォール）が発生して表示が遅くなるため、`Promise.all` で並列に呼び出す。

```tsx
// 複数の独立した API を呼ぶときは Promise.all で並列化する
const [user, tasks] = await Promise.all([getCurrentUser(), getTasks()]);
```

### 1. 子 Server Component 自身で取得する場合（Data Fetch Colocation）

ダッシュボード画面のように「ユーザー情報はすぐ返ってくるが、統計グラフの API だけ重くて 2 秒かかる」といった場合、`page.tsx` で全部揃うのを待つと画面全体が 2 秒間真っ白になってしまう。この場合は、統計グラフを表示する子 Server Component 自身の中で `await getHeavyStats()` を呼び、親の `page.tsx` 側でその子コンポーネントを `<Suspense fallback={<Skeleton />}>` で囲む。こうすると、軽い部分だけ先に表示し、重い部品だけをスケルトン表示から後から差し込む（ストリーミング表示）ことができる。

## アンチパターン：なぜ `useEffect` で API を呼んではいけないのか

React 公式ドキュメントの『エフェクトは必要ないかもしれない（You Might Not Need an Effect）』では、初学者が陥りやすい `useEffect` での API 呼び出しについて明確に注意喚起されている。

### 1. イベント起点の通信に `useEffect` を使う誤り

「送信ボタンを押したら `isSubmitted` という State を `true` に変え、`useEffect` で `isSubmitted` を監視して POST 通信を行う」という書き方は代表的なアンチパターンである。処理の流れが間接的になり、再レンダーのたびに意図しない二重送信が起きる原因になる。「ユーザーが何かをしたから通信する」処理は、必ず `onClick` や `onSubmit` のイベントハンドラ関数の中に直接書く。

### 1. 初期データ取得を生の `useEffect + fetch` で書く問題

Client Component で次のように `useEffect` の中で直接 `fetch` を呼ぶコードは、一見動くように見えて多くの欠陥を抱えている。

```tsx
// ❌ 避けるべきパターン：生の useEffect でのデータ取得
useEffect(() => {
  fetch(`/api/tasks/${categoryId}`)
    .then((res) => res.json())
    .then((data) => setTasks(data));
}, [categoryId]);
```

この書き方には次の問題がある。

1. **競合状態（Race Condition）のバグ**: ユーザーがカテゴリ A → カテゴリ B と素早く切り替えたとき、通信が遅れたカテゴリ A のレスポンスが後から返ってくると、画面が古いカテゴリ A のデータで上書きされてしまう。
1. **初期表示の遅れ**: ブラウザに JavaScript がダウンロードされ、最初の描画が終わってから初めて API 通信が始まるため、Server Component で取得するよりも画面表示が遅くなる。
1. **状態管理の肥大化**: ローディング中（`isLoading`）、エラー発生時（`error`）、データのキャッシュや再取得などをすべて手動で書かなければならない。

そのため、初期表示のデータ取得は原則として **Server Component** で行い、どうしてもブラウザ側で動的なデータ取得（入力に応じた検索やポーリング等）が必要な場合は、生の `useEffect` ではなく **TanStack Query（React Query）** や **SWR** といったデータフェッチライブラリを使用する。

## See also

- [Bulletproof React の全体像とアーキテクチャ原則](/learning/architecture/bulletproof-react-overview.md)
- [Server Components と Client Components の境界設計](/learning/components-and-state/nextjs-server-and-client-components.md)
- [State の置き場所（Colocation / Lifting Up）とデータフロー設計](/learning/components-and-state/react-state-ownership-and-data-flow.md)
- [UI の 4 状態（Ideal / Loading / Empty / Error）とフィードバック設計](/learning/ui-and-design/ui-states-and-feedback.md)
- [You Might Not Need an Effect — React Official Documentation](https://ja.react.dev/learn/you-might-not-need-an-effect)
- [Fetching Data — Next.js Official Documentation](https://nextjs.org/docs/app/getting-started/fetching-data)
- [API Layer — Bulletproof React](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md)
- [Next.jsの考え方（データフェッチ） — Zenn](https://zenn.dev/akfm/books/nextjs-basic-principle)
