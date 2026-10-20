---
type: guideline
title: 'コンポーネントの合成パターン（Composition / Compound Components）'
description: 'Props 爆発やバケツリレー（Prop Drilling）を防ぐための、children による Containment、Named Slots、および Compound Components の設計パターン。'
tags: [react, composition, compound-components, components, frontend]
status: draft
verified: { by: antigravity/gemini-4-argon, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# コンポーネントの合成パターン（Composition / Compound Components）

コンポーネントに機能を追加する際、安易に `hasIcon`・`showFooter`・`isCompact`・`primaryButtonText` のような設定用 Props を増やし続けると、条件分岐だらけで保守不能になる **「Props 爆発」** や、深い階層へ Props を素通しするだけの **「バケツリレー（Prop Drilling）」** が発生する。これらを防ぐため、React では「設定 Props で分岐する」のではなく **「小さな部品を外から差し込んで組み立てる（Composition：合成）」** パターンを用いる。

## 1. アンチパターン：設定 Props の肥大化（Props 爆発）

次のように、見た目のバリエーションや内部要素の有無をすべて Props で受け取る設計は避ける。

```tsx
// 悪い例：要件が増えるたびに Props と内部の if 文が増殖する
<Card
  title="ポモドーロ設定"
  subtitle="作業時間と休憩時間を調整します"
  headerIcon={<SettingsIcon />}
  showCloseButton={true}
  onClose={handleClose}
  primaryActionText="保存"
  onPrimaryAction={handleSave}
  secondaryActionText="キャンセル"
  onSecondaryAction={handleCancel}
/>
```

この設計では「ボタンを 3 つにしたい」「タイトルの横にバッジを置きたい」といった変更のたびに `Card` 本体の改修が必要になり、他の画面への影響リスクも高まる。

## 2. パターン1：`children` による Containment（枠と中身の分離）

`Card`、`Modal`、`Panel`、`Layout` などの「枠（コンテナ）」を表すコンポーネントは、**中身に何が置かれるかを知らない状態** にし、特別な Prop である `children` をそのまま描画する。

```tsx
type CardProps = {
  children: React.ReactNode;
};

export function Card({ children }: CardProps) {
  return <section className="card-surface">{children}</section>;
}

// 呼び出し側：中身を自由に組み立てて差し込める
<Card>
  <h2>ポモドーロ設定</h2>
  <p>作業時間と休憩時間を調整します</p>
  <Button onClick={handleSave}>保存</Button>
</Card>;
```

**効果**:

1.  **枠と中身の責務分離**: `Card` は枠線・背景・余白・影だけを担当し、中身の変更によって `Card` を修正する必要がなくなる。
1.  **Prop Drilling の解消**: 親コンポーネントが `Card` の中身を直接記述できるため、`Card` を経由して孫コンポーネントへ Props をバケツリレーする必要がない。

## 3. パターン2：Named Slots（複数の差し込み口）

「ヘッダー領域」「本文領域」「フッター（アクションボタン）領域」のように、枠の中で配置場所が決まっている箇所が複数ある場合は、`children` に加えて `React.ReactNode` 型の Props（**Named Slots**）を受け取る。

```tsx
type PageLayoutProps = {
  header: React.ReactNode;
  sidebar?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
};

export function PageLayout({ header, sidebar, children, footer }: PageLayoutProps) {
  return (
    <div className="layout-grid">
      <header className="layout-header">{header}</header>
      {sidebar && <aside className="layout-sidebar">{sidebar}</aside>}
      <main className="layout-main">{children}</main>
      {footer && <footer className="layout-footer">{footer}</footer>}
    </div>
  );
}

// 呼び出し側：各スロットに任意の JSX を差し込む
<PageLayout
  header={<AppHeader user={currentUser} />}
  sidebar={<TaskFilterMenu />}
  footer={<TimerStatusBar />}
>
  <PomodoroTimerView />
</PageLayout>;
```

`headerTitle: string` や `showSidebar: boolean` を渡すのではなく、**描画したい要素（`React.ReactNode`）そのものを渡す** ことで、レイアウト部品が業務ロジックや子部品の Props に依存しなくなる。

## 4. パターン3：Compound Components（複合コンポーネント）

`<Tabs>` や `<Dialog>`、`<Accordion>` のように、**「複数のパーツが裏側で状態（現在選択中のタブや開閉状態）を共有しつつ、呼び出し側でパーツの並び順や中身を自由に組み替えたい」** 場合には **Compound Components（複合コンポーネント）** パターンを使う。HTML の `<select>` と `<option>` の関係と同じ考え方である。

### 仕組み（Context による暗黙の状態共有）

親コンポーネント（例: `Tabs`）が React Context を通じて内部状態を保持・配信し、子パーツ（`Tabs.List`、`Tabs.Trigger`、`Tabs.Content`）がその Context を参照する。

```tsx
const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (value: string) => void;
} | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* コンポーネントは <Tabs> の内部で使用してください');
  return ctx;
}

export function Tabs({
  defaultValue,
  children,
}: {
  defaultValue: string;
  children: React.ReactNode;
}) {
  const [activeTab, setActiveTab] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs-root">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
};

Tabs.Trigger = function TabsTrigger({
  value,
  children,
}: {
  value: string;
  children: React.ReactNode;
}) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      type="button"
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
};

Tabs.Content = function TabsContent({
  value,
  children,
}: {
  value: string;
  children: React.ReactNode;
}) {
  const { activeTab } = useTabsContext();
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
};
```

### 呼び出し側の記述

```tsx
<Tabs defaultValue="work">
  <Tabs.List>
    <Tabs.Trigger value="work">作業タイマー</Tabs.Trigger>
    <Tabs.Trigger value="stats">統計グラフ</Tabs.Trigger>
  </Tabs.List>

  <Tabs.Content value="work">
    <WorkTimerPanel />
  </Tabs.Content>
  <Tabs.Content value="stats">
    <StatisticsPanel />
  </Tabs.Content>
</Tabs>
```

### 3つのパターンの選び方

| パターン                      | 状態の共有           | 差し込み口の数             | 代表的な使いどころ                                                                     |
| :---------------------------- | :------------------- | :------------------------- | :------------------------------------------------------------------------------------- |
| **`children`（Containment）** | なし                 | 1つ                        | `Card`、`Badge`、`Section`、単一枠のラッパー                                           |
| **Named Slots**               | なし                 | 2〜3個（固定レイアウト）   | `PageLayout`（`header` / `sidebar` / `children`）、`PageHeader`（`title` / `actions`） |
| **Compound Components**       | あり（Context 共有） | 任意（構造を自由に組める） | `Dialog`、`Tabs`、`Accordion`、`DropdownMenu`（Radix UI / shadcn/ui 等で標準採用）     |

## 決定理由（Rationale）

条件分岐 Props でバリエーションを増やす設計は、初期実装は簡単に見えるが、画面ごとの微妙な差分を吸収するたびにコンポーネントの複雑度が指数関数的に増大する。`children`・Named Slots・Compound Components によって「枠・状態管理」と「中身の要素」を分離すれば、既存のコンポーネントコードを一切書き換えずに新しい画面要件へ対応できる（開放閉鎖原則：Open-Closed Principle）。

## See also

- [Passing JSX as children – React 公式ドキュメント](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children)
- [Passing Data Deeply with Context – React 公式ドキュメント](https://react.dev/learn/passing-data-deeply-with-context)
- [どの部品で State を持ち、どう渡すか（State の所有権とデータフロー）](/learning/components-and-state/react-state-ownership-and-data-flow.md)
- [UI コンポーネントの粒度と分類（Atomic Design と現代の分類法）](/learning/architecture/react-component-classification.md)
