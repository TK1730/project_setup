---
type: guideline
title: 'ハーネスの前後比較（probe.sh）'
description: '同じ確認用の依頼を変更前と変更後のハーネスで実行し、結果を並べて保存するスクリプト probe.sh の使い方。'
tags: [development, harness, ai, scripts]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-19T00:00:00Z }
stale_after: 2027-10-19T00:00:00Z
---

# ハーネスの前後比較（probe.sh）

同じ確認用の依頼を、変更前と変更後のハーネスで実行し、結果を並べて保存するスクリプトの使い方。改善案を採用する前に、その案で振る舞いが本当に変わるかを確かめるために使う。再発防止と作業の質の改善で共通に使う。

## 使い方

1. 確認用の依頼文を 1 つのテキストファイルに書く。改善案に付いている確認用の依頼文をそのまま使う。
1. ハーネスのファイル（`docs/AGENTS.md`、スキルなど）を、改善案のとおりに書き換える。まだコミットしない。
1. リポジトリのルートで、変更前の git ref と依頼文のファイルを渡して実行する。

   ```bash
   scripts/harness/probe.sh HEAD .local/harness/probes/no-guess.txt
   ```

1. 表示された `diff` のコマンドで、変更前と変更後の結果を比べる。
1. 振る舞いが良くなっていれば変更をコミットし、そうでなければ元に戻す。

`HEAD` の代わりに、コミットのハッシュやブランチ名も渡せる。

## 何が起きるか

- 変更前: `<ref>` の時点の状態を、一時的な別の作業フォルダ（git worktree）に用意して実行する。終わると作業フォルダは消す。
- 変更後: 今の作業フォルダで実行する。コミットしていない変更も含まれる。
- 結果: `.local/harness/probe-results/<日時>-<依頼文のファイル名>/` に `prompt.txt`、`before.md`、`after.md` を保存する。`.local/` は git の管理外である。

## 費用と安全のための設定

`claude -p` は、ふだんの依頼 1 回と同じくらいトークンを使う。1 回の実行で `claude -p` を 2 回呼ぶ。

| 設定                                                | 目的                                                 |
| :-------------------------------------------------- | :--------------------------------------------------- |
| `--permission-mode plan`                            | 計画を立てるだけのモードで動かし、変更を実行させない |
| `--disallowed-tools "Edit Write NotebookEdit Bash"` | ファイルの書き換えとコマンドの実行を禁止する         |
| `--permission-prompts none`                         | 許可を求める操作は、聞かずに自動で拒否する           |
| `--no-session-persistence`                          | 比較用のセッションを履歴に残さない                   |
| `--max-budget-usd 1`                                | API キーで使う場合に、1 回あたりの費用の上限を決める |

`claude` を呼ばずに流れだけ確かめるときは、`DRY_RUN=1` を付ける。

```bash
DRY_RUN=1 scripts/harness/probe.sh HEAD .local/harness/probes/no-guess.txt
```

## 比べられないもの

比べられるのは、リポジトリの中のハーネスだけである。メモリ（`~/.claude/projects/` 配下）や `~/.claude/settings.json` は、変更前と変更後で同じものが使われる。

AI の出力は毎回少しずつ変わる。1 回の比較で差が小さいときは、同じ依頼を何回か実行してから判断する。

## 決定理由（Rationale）

- shell で書いた。worktree の用意、`claude` の実行、結果の保存といった、コマンドをつなぐ処理が中心のためである。
- 変更後は今の作業フォルダで実行する。ハーネスの変更は、確かめる前はコミットしないことが多いためである。
- 読み取り専用で動かす。比べたいのは振る舞いの違いであり、比較のたびにファイルが書き換わると、変更前と変更後の条件が揃わなくなるためである。

## See also

- [前後比較スクリプト](../../../scripts/harness/probe.sh)
- [同じミスの再発防止（mistake-retro）](/development/harness-improvement/mistake-retro.md)
- [ハーネス改善の仕組み](/development/harness-improvement/index.md)
