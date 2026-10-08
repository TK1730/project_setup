---
type: guideline
title: 'README の書き方'
description: 'README.md の名前、置き場所、中身のルール。'
tags: [documentation, readme, google-docguide]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# README の書き方

`README.md` の名前、置き場所、中身のルール。`README.md` はディレクトリの案内役であり、他の文書とは置き場所の考え方が違う。

## 名前と置き場所

- 名前は `README.md` に固定する。拡張子 `.md` が必須で、大文字小文字を区別する。
- 他の Markdown と違い、文書用ディレクトリの中ではなく、コード本体の最上位ディレクトリに置く。
- コードパッケージの最上位ディレクトリには、最新の `README.md` を置く。他から使われるインターフェースを持つパッケージでは特に重要である。
- `docs/` には `README.md` を置かない。docs の目次は OKF の `index.md` で表す。

## 中身

最低限、利用者向けまたはチーム向け文書へのリンクを含める。パッケージ単位の `README.md` には、次の 5 点を含めるか、参照先を示す。

- 何が入っていて、何に使うか
- 連絡先
- 状態（非推奨、一般公開前など）
- 使い方（サンプルコード、コピーできるコマンドなど）
- 関連文書へのリンク

## See also

- [文書の種類と置き場所](/guides/document-types.md)
- [Open Knowledge Format 運用ガイド](/guides/open-knowledge-format.md)
- [Google docguide: READMEs.md](https://github.com/google/styleguide/blob/gh-pages/docguide/READMEs.md)
