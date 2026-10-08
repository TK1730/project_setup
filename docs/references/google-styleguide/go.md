---
type: reference
title: 'Google Go Style Guide 要約（REST API 開発向け）'
description: 'Google Go Style Guide の要約（命名、interface と context、エラー処理、テスト）。'
tags: [go, backend, google-styleguide, style, errors, testing]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# Google Go Style Guide 要約（REST API 開発向け）

Google の Go スタイルガイド（guide / decisions / best-practices）のうち、Go で REST API を開発するときに知っておく価値が高い点を要約した外部ガイドの参考資料である。本リポジトリの規約ではなく、原典の内容を日本語で整理したものであり、詳細と最新の内容は原典を参照すること。

各項目の末尾に原典のファイルと節を示す（例: decisions / Getters）。

## 判断の優先順位

読みやすい Go コードの属性は、重要な順に Clarity（明確さ）、Simplicity（単純さ）、Concision（簡潔さ）、Maintainability（保守性）、Consistency（一貫性）である。迷ったら上位を優先する（guide / Style principles）。

- コードは `gofmt` の出力に従う（guide / Formatting）。
- 複数語の名前は `MixedCaps` / `mixedCaps` とし、アンダースコアを使わない。定数も `MaxLength` であり `MAX_LENGTH` ではない（guide / MixedCaps）。
- 行長に固定の上限はない。長いと感じたら分割より先にリファクタリングを検討する（guide / Line length）。

## 命名

- パッケージ名は小文字と数字のみで短くし、複数語でも区切らない（`tabwriter`）。`util`、`common`、`helper`、`model` のような情報のない名前は避ける（decisions / Package names）。
- 取得系の関数名に `Get` / `get` を付けず、名詞から始める（`GetCounts` ではなく `Counts`）。HTTP GET のように概念自体が "get" の場合は例外。時間がかかる処理や失敗しうる処理には `Fetch` / `Compute` が使える（decisions / Getters）。
- 略語は同じ大文字小文字で揃える。`URL` / `url`、`ID` / `id`、`DB` / `db` とし、`Url`、`Id` は誤り（decisions / Initialisms）。

  ```go
  func (s *Store) userByID(id string) (*User, error)
  ```

- レシーバ名は短く（1〜2 文字）、型の略語にして、その型の全メソッドで統一する。`this` / `self` は使わない（decisions / Receiver names）。
- パッケージ名と重複する語を避ける。`widget.NewWidget` ではなく `widget.New`。型名や文脈の繰り返しも避ける（decisions / Repetition、Package vs. exported symbol name）。
- 名前の長さはスコープの大きさに比例させ、使用回数に反比例させる。小さいスコープなら 1 語や 1〜2 文字でよく、ファイルスコープなら複数語が必要になりうる（decisions / Variable names）。

## interface と context

- interface は実際に必要になるまで作らない。「service」「repository」のような抽象的なパターン名ではなく、必要な振る舞いに着目する（decisions / Interfaces、best-practices / Avoid unnecessary interfaces）。
- interface は小さく設計し、利用側（consumer）のパッケージで、実際に使うメソッドだけを含めて定義する。パッケージ内だけで使うなら非公開にする。interface 自体が成果物（共通プロトコル）の場合のみ提供側が公開してよい（decisions / Interfaces）。
- 関数は interface を受け取り、具体型を返す。戻り値が具体型であれば、呼び出し側はその実装の公開メソッドとフィールドをすべて使える。ただし `error` のようにカプセル化のために interface を返すのは許容される（decisions / Interfaces）。
- `context.Context` は常に第一引数にする。例外は HTTP ハンドラ（`req.Context()` から取得）、テスト関数（`t.Context()`）、`main` や `init` などのエントリポイント（`context.Background()`）である。呼び出しチェーンの途中で `context.Background()` を作るのはまれで、基本は呼び出し元の context を受け取る（decisions / Contexts）。

  ```go
  func (s *Service) Create(ctx context.Context, in Input) (*Record, error)
  ```

- context を構造体のフィールドに持たせず、必要なメソッドごとに引数で渡す（decisions / Contexts）。
- 独自の context 型や、`context.Context` 以外の interface をシグネチャに使わない。例外はない（decisions / Custom contexts）。
- Context を引数に取る関数は、通常 `error` を返すようにする。呼び出し側が処理中のキャンセルを判別できるため（decisions / Returning errors の Tip）。

## エラー処理

- `error` は最後の戻り値にし、公開関数は具象型ではなく `error` 型で返す。具象型の nil ポインタが interface に包まれると non-nil になるバグを避けるため（decisions / Returning errors）。
- エラーを `_` で捨てない。その場で処理するか、呼び出し元に返す。捨てるなら安全な理由をコメントで添える（decisions / Handle errors）。
- エラーを先に処理して早期 return し、正常系をインデントさせない。`else` に正常系を入れない（decisions / Indent error flow）。

  ```go
  if err != nil {
      return nil, err
  }
  ```

- エラー文字列は小文字で始め、句読点で終えない。他の文脈に埋め込まれて表示されるため。ログやテスト失敗メッセージのような最終表示は大文字で始めてよい（decisions / Error strings）。
- 失敗を `-1` や空文字列などの値で表さない（in-band error）。複数の戻り値で `error` または `ok bool` を返す（decisions / In-band errors）。

  ```go
  func Lookup(key string) (value string, ok bool)
  ```

- エラーに情報を足すときは、元のエラーが既に持つ情報を繰り返さない。失敗を示すだけで新しい情報がない注釈（`"failed: %w"`）は付けず、そのまま返す（best-practices / Adding information to errors）。
- `%w` と `%v` の使い分け（best-practices / Adding information to errors）:
  - 呼び出し側が `errors.Is` / `errors.As` で調べる必要があるときは `%w` を使う。パッケージの API として公開・テストしている場合も `%w` が適切である。
  - 注釈や表示だけが目的のとき、およびRPCやストレージなどのシステム境界でエラーを別のエラー空間（例: gRPC ステータスコード）に変換するときは `%v` を使う。
- `%w` を使うなら文字列の末尾に置き（`"...: %w"`）、エラー文字列の並びとエラーチェーンの構造を一致させる（best-practices / Placement of %w in errors）。

  ```go
  return fmt.Errorf("find pomodoro record: %w", err)
  ```

- 同じエラーをログに出しつつ返すと重複する。エラーを返すなら通常は自分ではログに出さず、呼び出し側に判断を委ねる（best-practices / Logging errors）。REST API ではどの層でログに出すかを決めておくと重複を避けやすい。
- `log.Error` は控えめに使い、ERROR レベルは「より深刻」ではなく「対応が必要」なものにする。個人情報（PII）をログに出さないよう注意する（best-practices / Logging errors）。

## テスト

- 標準の `testing` パッケージのみを使い、アサーションライブラリは作らない・使わない（decisions / Assertion libraries、Use package testing）。
- 失敗メッセージは `関数(入力) = got, want want` の形にする。関数名と入力を含め、実際の値（got）を期待値（want）より先に書く（decisions / Identify the function、Identify the input、Got before want）。

  ```go
  t.Errorf("Add(%d, %d) = %d, want %d", a, b, got, want)
  ```

- 大きな値の比較は `cmp.Diff` で差分を出す。差分の向きを `(-want +got)` のようにメッセージで明示する（decisions / Print diffs、Got before want、Keep going の例）。

  ```go
  if diff := cmp.Diff(want, got); diff != "" {
      t.Errorf("Get() mismatch (-want +got):\n%s", diff)
  }
  ```

- 不一致の報告には `t.Error` を使い、1 回の実行で複数の失敗を見られるようにする。`t.Fatal` は、後続の検証が無意味になるとき（セットアップ失敗など）に使う（decisions / Keep going、best-practices / t.Error vs. t.Fatal）。
- テーブル駆動テストで `t.Run` を使うなら、行ごとの継続不能な失敗は `t.Fatal` でよい。`t.Run` を使わないなら `t.Error` と `continue` を使う（best-practices / t.Error vs. t.Fatal）。
- セットアップ用ヘルパーは `*testing.T` を受け取り、`t.Helper()` を呼んで失敗位置を呼び出し元に向ける。`t.Helper` でアサーションライブラリを作らない（decisions / Test helpers）。
- テスト内で起動した goroutine から `t.Fatal` などを呼ばない。`t.Error` を呼んで `return` する（best-practices / Don't call t.Fatal from separate goroutines）。

## コメント

- 公開されたトップレベルの名前には doc コメントを付ける。完全な文で、対象の名前から書き始める（decisions / Doc comments）。

  ```go
  // Encode writes the JSON encoding of req to w.
  func Encode(w io.Writer, req *Request) { ... }
  ```

- パッケージコメントは `package` 句の直前に空行なしで置き、`// Package math provides ...` の形で書く。複数ファイルのパッケージでは 1 ファイルにだけ書く（decisions / Package comments）。

## よくある間違い

| 避ける                                        | 推奨                             | 原典                                    |
| :-------------------------------------------- | :------------------------------- | :-------------------------------------- |
| `GetUser()`、`userId`                         | `User()`、`userID`               | decisions / Getters、Initialisms        |
| `user.UserService`、`widget.NewWidget`        | `user.Service`、`widget.New`     | decisions / Repetition                  |
| `func (this *Server)`                         | `func (s *Server)`               | decisions / Receiver names              |
| `package util` / `common`                     | 役割を表すパッケージ名           | decisions / Package names               |
| 提供側パッケージで先回りして interface を定義 | 利用側で必要なメソッドだけ定義   | decisions / Interfaces                  |
| 構造体フィールドに `ctx` を持つ               | メソッド引数で渡す               | decisions / Contexts                    |
| `fmt.Errorf("Failed to X.")`                  | `fmt.Errorf("x: %w", err)`       | decisions / Error strings               |
| エラーをログに出して、さらに返す              | 返すか、境界で一度だけログに出す | best-practices / Logging errors         |
| `t.Errorf("got %v, want %v")` のみ            | 関数名と入力を含める             | decisions / Identify the function       |
| goroutine 内で `t.Fatal`                      | `t.Error` + `return`             | best-practices / Don't call t.Fatal ... |

## See also

- [テーブル駆動テスト](/knowledge/table-driven-tests.md)
- [AAA パターン](/knowledge/aaa-pattern.md)
- [命名パターン](/knowledge/naming-patterns.md)
- [Google Go Style Guide](https://google.github.io/styleguide/go/guide)
- [Google Go Style Decisions](https://google.github.io/styleguide/go/decisions)
- [Google Go Style Best Practices](https://google.github.io/styleguide/go/best-practices)
