---
type: guideline
title: '作業の質の振り返り（work-retro）'
description: 'coding や docs の変更の質を振り返り、作業のルールへの改善案を出すスキル work-retro の使い方。'
tags: [development, harness, ai, skills, docs, coding]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-19T00:00:00Z }
stale_after: 2027-10-19T00:00:00Z
---

# 作業の質の振り返り（work-retro）

coding や docs の変更の質を振り返るスキル `work-retro` の使い方。良くする対象は、作業のルール（`docs/conventions/`、`docs/frontend/` と `docs/backend/` の規約）である。見つけた箇所を直すだけで終わらせず、同じことが起きないようにルールを変える案を出す。

## 使う時

作業の区切りや、PR を出す前に使う。Claude Code で次のどちらかを入力する。

```text
/work-retro
```

```text
docs/frontend/ の変更を work-retro で振り返って
```

範囲を指定しなければ、今のブランチで `main` から変えたファイルと、コミットしていないファイルを振り返る。スキル本体は `.claude/skills/work-retro/SKILL.md` にある。

## スキルがすること

1. 振り返る範囲のファイルを決める。
1. 機械で確かめられる結果を集める。docs は [docs の機械チェック](/development/harness-improvement/docs-check.md)、TS は oxlint、Go は `go vet` を使う。
1. 機械では確かめにくいこと（文章の書き方、関心の分離、依存の向きのうちリンク以外、コードの命名・構成）を、決まりの文書と照らし合わせて読む。
1. 同じことが起きないようにルールを変える改善案を、最大 3 つ出す。各案には、変える場所と差分、根拠、分類、確認用の依頼文を付ける。
1. 見つけた箇所の一覧と改善案を `.local/harness/proposals/` に書き出す。コードや docs は直さない。

同じ種類の指摘が 2 回以上あり、機械で判定できるときは、`docs_check.py` に確認を足す案も出す。

## 人がすること

1. 見つけた箇所の一覧を読み、直すものを決める。コードの修正は、言語軸のランクに応じて自分で書くか、AI に頼む。
1. 改善案を読み、採用するものを伝える。
1. 採用したルールの変更が効くかを、[ハーネスの前後比較](/development/harness-improvement/probe.md) で確かめる。

## 書き換えないファイル

次のファイルは、改善案の対象になっても書き換えない。改善案には「メンターへの提案」として書かれる。

- ルート直下の `AGENTS.md`（組織から配られた習熟度ゲートの規定）
- `~/.antigravity-gate/`・`~/.claude-gate/` 配下のファイル
- ゲートの hook

## 決定理由（Rationale）

- 機械で確かめられることはスクリプトに任せ、スキルは機械では判定しにくいことだけを読む。同じ確認を AI に毎回させると、見落としや判定のぶれが起きるためである。
- 改善の対象を、見つけた箇所ではなくルールにした。箇所を直すだけでは、次の作業で同じことが起きるためである。
- 繰り返す指摘を機械チェックに移す案を出させる。ルールを文章で書き足すより、機械で止めるほうが確実なためである。
- コードの修正をスキルの中で行わない。言語軸のランクによって、AI がコードを書いてよいかが変わるためである。

## See also

- [docs の機械チェック（docs_check.py）](/development/harness-improvement/docs-check.md)
- [同じミスの再発防止（mistake-retro）](/development/harness-improvement/mistake-retro.md)
- [ハーネス改善の仕組み](/development/harness-improvement/index.md)
