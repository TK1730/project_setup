---
name: work-retro
description: coding や docs の作業の区切りに、変更の質を振り返り、作業のルール（docs/conventions/ やコーディング規約）への改善案を出す。「作業の振り返り」「work-retro」と言われたとき、PR を出す前に使う。改善案を書き出すところまでで止め、コードや docs は直さない。
---

# work-retro

作業の区切りに、変更の質を振り返り、作業のルールへの改善案を書き出す。採用するかはユーザーが決める。

## 1. 振り返る範囲を決める

既定は、今のブランチで `main` から変えたファイルとする。`git diff --name-only main...HEAD` とコミットしていないファイルを合わせる。ユーザーが範囲を指定したら、それに従う。

## 2. 機械で確かめられる結果を集める

- docs: `python3 scripts/harness/docs_check.py` の結果
- TS: `pnpm exec oxlint <変えたファイル>` の結果
- Go: `backend/` で `go vet ./...` の結果

## 3. 機械では確かめにくいことを読む

変えたファイルを読み、次の観点で決まりから外れた箇所を探す。各観点の決まりの正は、括弧内の文書である。

- docs の文章（`docs/conventions/documentation-writing.md`、`docs/conventions/markdown-style.md`）
- 1 つの文書に 1 つの関心ごとか（`docs/conventions/document-structure.md`）
- `knowledge/`、`references/`、`learning/` にプロジェクト固有の内容がないか（`docs/conventions/open-knowledge-format.md`）
- コードの命名・構成・コメント（`docs/frontend/` と `docs/backend/` の規約、`docs/knowledge/coding-mindset.md`）

この会話で受けたレビューの指摘があれば、それも材料にする。

## 4. 改善案を出す

見つけた箇所を直すのではなく、**同じことが起きないようにルールをどう変えるか**を考える。改善案は最大 3 つにし、それぞれに次の 4 つを書く。

- 変える場所（ファイルと見出し）と、変える内容の差分
- 根拠（どの箇所・どの指摘から出た案か）
- 分類（coding / docs）
- 確認用の依頼文（そのルールで振る舞いが変わるかを確かめる 1 文）

同じ種類の指摘が 2 回以上あり、機械で判定できるなら、`scripts/harness/docs_check.py` に確認を足す案も出す。

次のファイルは、改善案の対象にしても書き換えない。「メンターへの提案」として書くだけにする。

- ルート直下の `AGENTS.md`
- `~/.antigravity-gate/`・`~/.claude-gate/` 配下のファイル
- ゲートの hook

## 5. 書き出す

`.local/harness/proposals/YYYY-MM-DD-work-<短い名前>.md` に、見つけた箇所の一覧と改善案を書き出し、ユーザーに要点を伝える。

見つけた箇所の修正と、ルールの変更は、ユーザーが採用を決めてから行う。コードの修正は、言語軸のランクに応じた AGENTS.md の応対モードに従う。
