---
type: guideline
title: 'README の書き方'
description: 'README.md をディレクトリの案内役として書くための考え方（役割、名前、置き場所、中身）。'
tags: [knowledge, documentation, readme, google-docguide]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# README の書き方

`README.md` の役割、名前、置き場所、中身をまとめる。
要点は、README はディレクトリの短い案内であり、詳しい内容は書かずに文書へリンクすることである。
内容は Google の docguide の READMEs と Documentation Best Practices をもとにしている。

## README の役割

- README は、ディレクトリの中身の短い要約である。
- GitHub などでディレクトリを開くと、README の中身が表示される。
  そのため、コードを見て回る人、特に初めての人に大事な情報を伝えられる。
- 初めての人に、そのディレクトリを案内し、詳しい説明や手引きの場所を示す。

## README の名前と置き場所

- 名前は `README.md` にする。
  拡張子 `.md` が必須で、大文字と小文字を区別する。
- ほかの Markdown と違い、文書用のディレクトリの中には置かない。
  コード本体の最上位ディレクトリに置く。
- コードのパッケージの最上位ディレクトリには、すべて最新の `README.md` を置く。
  ほかのチームにインターフェースを提供するパッケージでは特に大事である。

## README の中身

最低限、利用者向けやチーム向けの文書へのリンクを入れる。
パッケージ単位の `README.md` には、次の 5 点を書くか、書いてある場所を示す。

1. 何が入っていて、何に使うか。
1. 連絡先（誰が保守しているか）。
1. 状態（非推奨か、一般公開前かなど）。
1. 使い方（サンプルコード、コピーできるコマンドなど）。
1. 関連文書へのリンク。

あわせて、最初に見るべきファイルはどれかも示す。

## See also

- [書く場所の選び方](/knowledge/where-to-document.md)
- [Google docguide: READMEs 要約](/references/google-styleguide/docguide-readmes.md)
- [Google docguide: Documentation Best Practices 要約](/references/google-styleguide/docguide-best-practices.md)
