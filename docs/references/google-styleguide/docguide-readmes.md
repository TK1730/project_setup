---
type: reference
title: 'Google docguide: READMEs 要約'
description: 'Google docguide の READMEs の要約（README の役割、名前、置き場所、中身）。'
tags: [documentation, readme, google-styleguide, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Google docguide: READMEs 要約

Google の docguide のうち、READMEs の要約である。
外部ガイドの要約であり、最終的な根拠は原典を参照すること。
要点は「README はディレクトリの中身の短い案内である」「コードの最上位ディレクトリに置く」「中身には最低限、詳しい文書へのリンクを入れる」の 3 つである。

## README の役割

出典: Overview

- README は、ディレクトリの中身の短い要約である。
- GitHub や Gitiles では、ディレクトリを開くと README の中身が表示される。
  そのため、コードを見て回る人、特に初めての人に大事な情報を伝えられる。

## README の名前

出典: Readable README files

- 名前は `README.md` にしなければならない。
  拡張子 `.md` が必須で、大文字と小文字を区別する。

## README の置き場所

出典: Where to put your README

- ほかの Markdown と違い、`README.md` は文書用のディレクトリの中に置かない。
  プロダクトやライブラリのコード本体の最上位ディレクトリに置く。
- コードのパッケージの最上位ディレクトリには、すべて最新の `README.md` を置く。
  ほかのチームにインターフェースを提供するパッケージでは特に大事である。

## README の中身

出典: What to put in your README

最低限、利用者向けやチーム向けの文書へのリンクを入れる。
パッケージ単位の `README.md` には、次の 5 点を書くか、書いてある場所を示す。

1. 何が入っていて、何に使うか。
1. 連絡先。
1. 状態（非推奨か、一般公開前かなど）。
1. 使い方（サンプルコード、コピーできるコマンドなど）。
1. 関連文書へのリンク。

## See also

- [Google docguide: Documentation Best Practices 要約](/references/google-styleguide/docguide-best-practices.md)
- [Google docguide: READMEs.md](https://github.com/google/styleguide/blob/gh-pages/docguide/READMEs.md)
