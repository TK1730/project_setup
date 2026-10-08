---
type: guideline
title: 'プログラミングでよく使われる定番命名パターン'
description: 'プログラミングでよく使われる定番の命名パターン集。'
tags: [programming, naming, clean-code, idiom]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# プログラミングでよく使われる定番命名パターン

定数と真偽値には定番の命名パターン（`X_PER_Y`、`MIN_`/`MAX_`/`DEFAULT_`、`is`/`has`/`can`）を使う。意図が名前で伝わり、マジックナンバーを排除できる。

## 1. 単位換算・比率: X_PER_Y

Y あたりの X を表す。英語の `per` を用いた単位換算の代表的パターン。

| 定数名                    | 意味                      | 例     |
| :------------------------ | :------------------------ | :----- |
| `SECONDS_PER_MINUTE`      | 1分あたりの秒数           | `60`   |
| `MINUTES_PER_HOUR`        | 1時間あたりの分数         | `60`   |
| `MILLISECONDS_PER_SECOND` | 1秒あたりのミリ秒         | `1000` |
| `HOURS_PER_DAY`           | 1日あたりの時間数         | `24`   |
| `ITEMS_PER_PAGE`          | 1ページあたりの件数       | `20`   |
| `BYTES_PER_KB`            | 1キロバイトあたりのバイト | `1024` |

## 2. 範囲・境界値: MIN_, MAX_, DEFAULT_

数値の上限・下限・初期値を明示するパターン。

- `MIN_SECONDS = 0`
- `MAX_RETRY_COUNT = 3`
- `DEFAULT_TIMEOUT_MS = 5000`

## 3. 真偽値: 状態や能力を表す接頭辞

- `is...`: 状態を表す。例: `isRunning`, `isOpen`
- `has...`: 所有を表す。例: `hasError`, `hasPermission`
- `can...`: 可能かを表す。例: `canSubmit`, `canRetry`

## See also

- [フロントエンド命名規則](/frontend/naming-conventions.md)
