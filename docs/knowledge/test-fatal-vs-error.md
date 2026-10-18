---
type: guideline
title: 'Go のテストで t.Fatalf と t.Errorf を使い分ける'
description: 'Go のテストで、失敗したときに後ろの確認へ進むかどうかで t.Fatalf と t.Errorf を選ぶ基準。'
tags: [knowledge, testing, go, t-fatalf, t-errorf]
status: stable
verified:
  - { by: claude-code/claude-sonnet-5-5, at: 2026-10-17T00:00:00Z }
  - { by: claude-code/claude-opus-5-5, at: 2026-10-17T00:00:00Z }
stale_after: 2027-10-17T00:00:00Z
---

# Go のテストで t.Fatalf と t.Errorf を使い分ける

`t.Errorf` は失敗を記録してテストを続け、`t.Fatalf` は失敗を記録してそのテストケースをそこで終わらせる。選ぶ基準は 1 つで、「この確認が失敗したら、後ろの確認に意味がなくなるか」である。意味がなくなる（または `nil` を触って panic する）なら `Fatalf`、ならないなら `Errorf` を使う。基本は `Errorf` で、`Fatalf` は後ろの確認の前提を確かめる行だけに使う。

## 1. 2 つの違い

- `t.Errorf`: 失敗を記録し、そのテストの続きを実行する。標準ライブラリの説明では「`Logf` に続けて `Fail` を呼ぶのと同じ」である。[^go-testing]
- `t.Fatalf`: 失敗を記録し、そのテストをその場で止める。「`Logf` に続けて `FailNow` を呼ぶのと同じ」である。[^go-testing]
- 止まるのは、呼んだテストケースだけである。サブテスト（`t.Run` の 1 ケース）で呼べば、そのケースだけが終わり、ほかのケースは続けて実行される。
- `FailNow`（`Fatalf` の中身）は、テスト関数を実行しているゴルーチンから呼ぶ必要がある。テスト中に自分で作った別のゴルーチンから呼んでも、そのゴルーチンは止まらない。[^go-testing]

## 2. 判断基準

確認の行ごとに、次の問いに答える。

> この確認が失敗したら、後ろの確認に意味がなくなるか。または、`nil` を触って panic するか。

- なる: `t.Fatalf`。後ろの確認は、この確認が成り立つことを前提にしている。
- ならない: `t.Errorf`。後ろの確認は、この確認が失敗していても確かめる価値がある。

Go のスタイルガイドも、まず `t.Error` を選び、`t.Fatal` は後ろの確認が無意味になるときに使うとしている。[^go-test-comments][^google-go-decisions] `t.Fatal` が向くのは、テストの準備が失敗して、それがないとテストを続けられないときである。[^go-test-comments]

## 3. 変数名が `err` だから `Fatalf`、ではない

判断するのは変数名ではなく、「失敗したら後ろがどうなるか」である。次の表は、よくある確認を並べたものである。

| 確認の行                                     | 確認していること                       | 失敗したら後ろはどうなるか                                             | 使うもの |
| :------------------------------------------- | :------------------------------------- | :--------------------------------------------------------------------- | :------- |
| Usecase の戻り値 `err` が期待と違う          | 予想と違う分岐（出口）を通っていないか | 違う出口を通ったので、戻り値や呼び出し記録を比べても無意味             | `Fatalf` |
| HTTP ハンドラの `rec.Code` が期待と違う      | 予想と同じ道を通ったか                 | 違う道を通ったので、応答の中身を比べても無意味（`err` ではないが前提） | `Fatalf` |
| 応答 JSON の `Decode` の `err`               | テストの準備（読み取り）ができたか     | 比べる値が作れていないので、比較できない                               | `Fatalf` |
| 戻り値 `res` の比較                          | 結果の値が期待どおりか                 | 呼び出し記録の確認とは独立で、続けて確かめる価値がある                 | `Errorf` |
| 偽物リポジトリの呼び出し記録（`saveCalled`） | 保存処理が呼ばれたか                   | `res` の確認とは独立で、続けて確かめる価値がある                       | `Errorf` |

表の見どころは次の 3 点である。

- 同じ `err` でも意味が違う。Usecase の `err` は「テスト対象の結果」であり、期待と違えば別の出口を通ったことを意味する。`Decode` の `err` は「テストの準備がうまくいったか」の確認である。どちらも後ろを無意味にするので `Fatalf` だが、理由は別である。
- `err` ではない `rec.Code` も、後ろの前提なので `Fatalf` になる。
- `res` と `saveCalled` が両方 `Errorf` なのは、「満たしてほしい条件だから」ではない。`err` も満たしてほしい条件だからである。決め手は、互いに独立していて、片方が違ってももう片方を確かめる意味があることである。

## 4. 実装例

テーブル駆動テストのループ内で、`err` を `Fatalf`、`res` を `Errorf`、呼び出し記録を `Errorf` にした 3 段の例である。`UpdateUser` と偽物リポジトリは説明用の架空のものである。

```go
for _, tt := range tests {
	t.Run(tt.name, func(t *testing.T) {
		// Arrange（準備）
		repo := &fakeUserRepo{}
		uc := NewUserUsecase(repo)

		// Act（実行）
		res, err := uc.UpdateUser(ctx, tt.input)

		// Assert（検証）
		// 1 段目: 出口の確認。違う出口を通ったなら、下の比較は無意味なので止める。
		if !errors.Is(err, tt.wantErr) {
			t.Fatalf("UpdateUser() error = %v, want %v", err, tt.wantErr)
		}
		// 2 段目: 戻り値の確認。下の確認とは独立なので続ける。
		if res != tt.wantRes {
			t.Errorf("UpdateUser() = %v, want %v", res, tt.wantRes)
		}
		// 3 段目: 偽物リポジトリの呼び出し記録。上の確認とは独立なので続ける。
		if repo.saveCalled != tt.wantSaveCalled {
			t.Errorf("saveCalled = %v, want %v", repo.saveCalled, tt.wantSaveCalled)
		}
	})
}
```

- 各ケースは `t.Run` の中にあるので、`Fatalf` で止まるのはそのケースだけである。ほかのケースは実行される。テーブル駆動テストでサブテストを使うときは、`t.Error` と `continue` の代わりに `t.Fatal` を使う書き方がスタイルガイドにもある。[^google-go-decisions][^google-go-best-practices]
- `res` が `nil` になりうる型（ポインタなど）で、`res` の中身を読んでから比較するなら、その手前の確認は `Fatalf` にする。`nil` を触って panic するのを避けるためである。

## 5. Errorf にするうれしさ

独立した確認が 2 つとも間違っているとき、`Fatalf` だと 1 回目の実行では片方しか見えない。直して再実行して、初めてもう片方が見える。`Errorf` なら 1 回の実行で両方が見える。Go のスタイルガイドも、テストは「1 回の実行で失敗した確認をすべて出すために、できるだけ続けるべき」としている。[^go-test-comments][^google-go-decisions]

たとえば `res` の比較を `Fatalf` にしていると、`res` が違ったケースでは呼び出し記録（`saveCalled`）の確認まで進まない。呼び出し記録の側にも間違いがあっても、`res` を直して再実行するまで見えない。`res` の比較を `Errorf` にしていれば、1 回で両方が分かる。

## Rationale（決定理由）

- `Errorf` を基本にするのは、1 回の実行で見える失敗を増やし、直して再実行する回数を減らすためである。
- `Fatalf` を「後ろの確認の前提」に限るのは、前提が崩れた後の比較は、失敗の原因を見えにくくするだけで情報にならず、`nil` への参照で panic する危険もあるためである。
- 判断基準を変数名ではなく「後ろの確認が無意味になるか」にするのは、`err` の意味がテスト対象の結果と準備の確認で違うことや、`rec.Code` のように `err` 以外の前提もあることを、1 つの基準で説明できるからである。

## See also

- [テーブル駆動テストの設計指針](/knowledge/table-driven-tests.md)
- [テスト設計における AAA パターン](/knowledge/aaa-pattern.md)
- [Go の Repository 層のテストの設計指針](/knowledge/go-repository-testing.md)

[^go-testing]: [Go 標準 testing パッケージ](https://pkg.go.dev/testing) の `T.Errorf`、`T.Fatalf`、`T.Fail`、`T.FailNow`。`FailNow` は「テスト関数を実行しているゴルーチンから呼ぶ必要があり、テスト中に作った別のゴルーチンからは呼ばない」と書かれている。

[^go-test-comments]: [Go Wiki: Go Test Comments](https://go.dev/wiki/TestComments) の "Keep going"。`t.Error` を `t.Fatal` より優先し、`t.Fatal` はテストの準備が失敗して続けられないときに使うとしている。

[^google-go-decisions]: [Google Go Style Decisions](https://google.github.io/styleguide/go/decisions) の "Keep going"。不一致の報告には `t.Error` を優先し、`t.Fatal` は後ろの確認が無意味になるときに使うとしている。テーブル駆動テストではサブテストと `t.Fatal` の利用を勧めている。

[^google-go-best-practices]: [Google Go Style Best Practices](https://google.github.io/styleguide/go/best-practices) の `t.Fatal` に関する節。テストの準備の失敗には `t.Fatal` が適切で、サブテストなら `t.Fatal` で現在のサブテストだけが終わり次のサブテストへ進むとしている。
