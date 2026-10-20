---
type: reference
title: 'Open Knowledge Format (OKF) v0.2 仕様 要約'
description: 'Open Knowledge Format v0.2 の仕様の要約（Bundle の構造、Frontmatter、出典と信頼と鮮度、リンク、index.md と log.md、適合の条件）。'
tags: [documentation, okf, knowledge-management, specification]
status: stable
verified:
  - { by: claude-code/claude-opus-5-5, at: 2026-10-20T00:00:00Z }
  - { by: human:TK1730, at: 2026-10-20T00:00:00Z }
stale_after: 2027-10-20T00:00:00Z
---

# Open Knowledge Format (OKF) v0.2 仕様 要約

Google Cloud が公開している Open Knowledge Format（OKF）v0.2 の仕様の要約である。
外部仕様の要約であり、最終的な根拠は原典を参照すること。
OKF は、知識を「YAML Frontmatter 付きの Markdown ファイルを並べたディレクトリ」として表す形式である。
人もエージェントも専用の道具なしで読み書きでき、必須とするのは各文書の `type` だけである。

## OKF の目的

出典: 1. Motivation

- 道具なしで人が読めること、専用の SDK なしでエージェントが解析できること、バージョン管理で差分をとれること、道具や組織をまたいで持ち運べることを目指す。
- 知識は一度書いて終わりではなく、エージェントが書き続けて保守するものになりつつある。
  そこで v0.2 は、出典（provenance）、信頼（trust）、鮮度と状態（lifecycle）、計算の証明（attestation）を Frontmatter で表せるようにした。
- `type` の分類を固定すること、保存や検索の仕組みを決めること、OpenAPI などの分野ごとのスキーマを置き換えることは目的に含めない。

## OKF の用語

出典: 2. Terminology

- Bundle: 知識文書をまとめた、自己完結したディレクトリ。配布の単位である。
- Concept: 1 つの知識を表す 1 つの Markdown 文書。
- Concept ID: Bundle の中のファイルのパスから `.md` を除いたもの。
- Actor: 操作した人や仕組みを表す文字列（後述）。

## Bundle の構造と予約名

出典: 3. Bundle structure

- Bundle は Markdown ファイルのディレクトリの木である。
  ディレクトリの分け方は、書く側が内容に合わせて自由に決める。
- 配布は git リポジトリが推奨される（履歴、作者、差分がとれるため）。
  大きなリポジトリの中のサブディレクトリでもよい。
- `index.md`（目次）と `log.md`（変更履歴）はどの階層でも予約名であり、知識文書の名前に使ってはならない。

## Frontmatter のキー

出典: 4. Concept documents / 5. Provenance, trust, and lifecycle

| キー | 区分 | 内容 |
| :-- | :-- | :-- |
| `type` | 必須 | 文書の種類を表す短い文字列。中央で登録せず、自由に決める |
| `title` | 推奨 | 表示名。省略時はファイル名から導いてよい |
| `description` | 推奨 | 1 文の要約。目次や検索結果に使う |
| `resource` | 推奨 | 説明する実体を一意に示す URI。抽象的な概念には付けない |
| `tags` | 推奨 | 横断的な分類に使う短い文字列の配列 |
| `sources` | 任意 | 内容の根拠となった資料の一覧 |
| `generated` | 任意 | 内容を書いた人や仕組みと日時。`{ by, at }` |
| `verified` | 任意 | 内容を確かめた記録。`{ by, at }` の配列 |
| `status` | 任意 | `draft`、`stable`（省略時）、`deprecated` |
| `stale_after` | 任意 | この時刻以降は古いとみなす絶対時刻 |

- 書く側は独自のキーを足してよい。
  読む側は、知らないキーや知らない `type` を理由に文書を拒否してはならない。
- 日時は、UTC からの差を付けた ISO 8601 で書く（例: `2026-06-30T14:00:00Z`）。
- `sources` の各項目は `resource` が必須である。
  本文で主張ごとに出典を示すときは、`sources` の `id` を脚注のラベルにする。
  並び順の番号ではなく `id` を使うのは、エージェントが一覧を並べ替えても出典がずれないためである。
- `generated` は書いた記録、`verified` は確かめた記録であり、別に持つ。
  書いた人と確かめた人は同じとは限らないためである。
  `verified` は配列にせず 1 つの `{ by, at }` で書いてもよい。

## 信頼の段階と鮮度

出典: 5.3 Trust tiers / 5.4 / 5.5 / 7. Actor convention

- Actor は、エージェントや道具なら `<producer>/<version>`、人なら `human:<id>`、自動処理なら `process:<id>` と書く。
- 読む側は `verified` から信頼の段階を判断する。
  `verified` が無ければ未検証、`human:` 以外だけなら機械で確認済み、`human:` があれば人が確認済みである。
  これは目安であり、アクセス制御ではない。
- `stale_after` は相対的な期間ではなく絶対時刻で書く。
  「今の時刻と比べるだけ」で古いかどうかを判断できるようにするためである。

## リンク

出典: 6. Cross-linking and paths

- 文書どうしは通常の Markdown リンクでつなぐ。
- `/` で始まる Bundle 基点のパスを推奨する。サブディレクトリの中で文書を動かしてもリンクが切れにくいためである。相対パスも使える。
- リンク先が無いことは不正ではなく、まだ書かれていない知識として扱う。
- 外部の資料を Bundle の中に写して置くディレクトリを `references/` と呼ぶ慣例がある。必須ではない。

## index.md と log.md

出典: 8. Index files / 9. Log files

- `index.md` はどのディレクトリにも置ける目次で、文書を開く前に何があるかを見せる（progressive disclosure）。
  Frontmatter は付けない。
  例外として、Bundle 直下の `index.md` だけは `okf_version` を書ける。
- `index.md` は見出しごとに `* [タイトル](相対パス) - 短い説明` の形で並べ、説明にはリンク先の `description` を使う。
- `log.md` はその階層の変更履歴である。
  `## YYYY-MM-DD` の見出しで日付ごとにまとめ、新しい順に並べる。

## 計算の証明（Attested Computation）

出典: 10. Attested computations concept

- 数値の意味だけでなく、決められた計算方法も持つ文書の種類である。
  エージェントが計算を勝手に書き換えず、決められた計算を実行したことを確かめられるようにする。
- `runtime`、`parameters`、`executor`、`attester` などのキーを使う。
  データ分析の数値を扱う場面向けの仕組みである。

## 適合の条件

出典: 11. Conformance / 12. Versioning

- OKF v0.2 に適合する条件は、予約名以外のすべての `.md` に解析できる Frontmatter があり、空でない `type` があり、`index.md` と `log.md` が決まった構造に従うことである。
- それ以外は緩い指針である。
  読む側は、任意のキーが無いこと、知らない `type` やキー、リンク切れ、`index.md` が無いことを理由に Bundle を拒否してはならない。
- 版は `<major>.<minor>` で表す。minor は後方互換の追加、major は互換を壊す変更である。

## See also

- [Open Knowledge Format 仕様 (SPEC.md)](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- [Open Knowledge Format (Google Cloud)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
