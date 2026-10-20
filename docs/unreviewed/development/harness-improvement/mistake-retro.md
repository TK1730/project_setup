---
type: guideline
title: '同じミスの再発防止（mistake-retro）'
description: 'AI が指摘されたミスを過去の記録と照らし合わせ、ハーネスへの改善案を出すスキル mistake-retro の使い方。'
tags: [development, harness, ai, skills]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-19T00:00:00Z }
stale_after: 2027-10-19T00:00:00Z
---

# 同じミスの再発防止（mistake-retro）

AI が同じミスを繰り返さないようにするスキル `mistake-retro` の使い方。良くする対象は、AI 側のハーネス（`docs/AGENTS.md`、メモリ、スキル）である。

## 使う時

AI のミスを指摘した直後に使う。Claude Code で次のどちらかを入力する。

```text
/mistake-retro
```

```text
今のミスを mistake-retro で振り返って
```

スキル本体は `.claude/skills/mistake-retro/SKILL.md` にある。

## スキルがすること

1. ミスを「何をしたか / 本来どうすべきだったか」の 1 文にまとめ、人に確かめる。
1. `AGENTS_LEARNING.md`、メモリの feedback、`docs/AGENTS.md`、スキルを読み、初めてのミスか再発かを判定する。
1. 改善案を最大 3 つ出す。各案には、変える場所と差分、根拠、分類、確認用の依頼文を付ける。
1. 改善案を `.local/harness/proposals/` に書き出す。ハーネスのファイルは書き換えない。

## 人がすること

1. スキルが 1 文にまとめたミスが合っているかを確かめる。
1. 書き出された改善案を読み、採用するものを伝える。
1. 採用した案が効いたかを確かめる。案に付いた確認用の依頼文を、変更前と変更後で実行して比べる。比べ方は [ハーネスの前後比較（probe.sh）](/development/harness-improvement/probe.md) を参照する。

## 書き換えないファイル

次のファイルは、改善案の対象になっても書き換えない。改善案には「メンターへの提案」として書かれる。

- ルート直下の `AGENTS.md`（組織から配られた習熟度ゲートの規定）
- `~/.antigravity-gate/`・`~/.claude-gate/` 配下のファイル
- ゲートの hook

## 決定理由（Rationale）

- 再発したときは、対策を書き足すのではなく、対策が効かなかった理由を考えさせる。`AGENTS_LEARNING.md` には再発防止チェックリストがすでにあり、それでも同じ種類のミスが起きているため、書き足すだけでは同じことが繰り返される。
- 改善案は、git の管理外の `.local/` に書き出す。採用されなかった案がリポジトリに残らないようにするためである。
- 改善案を出すところまでで止め、採用は人が決める。作る側と評価する側を分けるためである。

## See also

- [ハーネス改善の仕組み](/development/harness-improvement/index.md)
- [依頼の書き方の改善（逆質問の集計）](/development/harness-improvement/prompt-quality.md)
