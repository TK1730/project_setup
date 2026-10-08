---
type: guideline
title: 'テスト設計における AAA パターン'
description: '単体テストを Arrange・Act・Assert の 3 段で構成する原則。'
tags: [knowledge, testing, clean-code, aaa-pattern]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# テスト設計における AAA パターン

AAA（Arrange・Act・Assert）は、テストを「準備・実行・検証」の 3 フェーズに分けて書くパターンである。テストの可読性と構造の一貫性を保つために、本プロジェクトのテストはこの構造で書く。

## 1. AAA パターンとは

テストの内部処理を「準備・実行・検証」の 3 つの明確なフェーズに分離する構造化手法である。

| フェーズ | 日本語 | 責務                 | 主な処理内容                                     |
| :------- | :----- | :------------------- | :----------------------------------------------- |
| Arrange  | 準備   | 前提条件の構築       | 入力データの生成、モック設定、インスタンス化     |
| Act      | 実行   | テスト対象の呼び出し | テスト対象関数やメソッドの実行、戻り値の受取     |
| Assert   | 検証   | 期待結果の照合       | 戻り値の比較、ステータスコード確認、副作用の検証 |

## 2. 実装例

### Go による HTTP ハンドラーテストの例

以下は説明用の簡略例で、現在のパッケージ構成（`handler` パッケージは `pomodoro` パッケージへ統合済み）とは異なる。実際のテストは `backend/internal/pomodoro/handler_test.go` の `TestCreatePomodoro`（テーブル駆動。各ケースの `t.Run` 内が準備・実行・検証の順になっている）を参照。

```go
func TestCreatePomodoro_InvalidJSON(t *testing.T) {
	// 1. Arrange（準備）
	h := handler.New(nil)
	body := strings.NewReader("invalid-json")
	req := httptest.NewRequest(http.MethodPost, "/api/pomodoros", body)
	rec := httptest.NewRecorder()

	// 2. Act（実行）
	h.CreatePomodoro(rec, req)

	// 3. Assert（検証）
	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected status %d, got %d", http.StatusBadRequest, rec.Code)
	}
}
```

## 3. 決定理由（Rationale）

1. 認知的負荷の低減:
   - すべてのテストが同一のリズム（準備 → 実行 → 検証）で書かれるため、コードリーディングが迅速になる。
1. 単一責任の維持:
   - 1 つのテスト内で Act（実行）が複数回現れるのを防ぎ、1 テスト 1 関心ごとの原則を守りやすくなる。
1. 境界の明確化:
   - テストのセットアップ（準備）と、真にテストしたい対象（実行）の境界が曖昧になるのを防止する。

## See also

- [テーブル駆動テスト](/knowledge/table-driven-tests.md)
- [`backend/internal/pomodoro/handler_test.go`](../../backend/internal/pomodoro/handler_test.go)
