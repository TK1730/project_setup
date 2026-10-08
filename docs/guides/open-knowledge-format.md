---
type: guideline
title: 'Open Knowledge Format (OKF) 運用ガイド'
description: 'docs が従う Open Knowledge Format (OKF) の仕様と、本プロジェクトでの使い方。'
tags: [documentation, okf, knowledge-management, operations]
status: stable
verified: { by: claude-code/claude-opus-5-5, at: 2026-10-08T00:00:00Z }
stale_after: 2027-10-08T00:00:00Z
---

# Open Knowledge Format (OKF) 運用ガイド

docs は OKF v0.2 を正として運用する。OKF が定めることは OKF に従い、OKF が任意としていることや決めていないことだけを、本プロジェクトのルールとしてここで決める。作成・更新・削除の流れは [文書の保守](/guides/maintenance.md) に書く。

## OKF とは

OKF は、知識を「YAML Frontmatter 付きの Markdown ファイルを並べたディレクトリ」として表すオープンな形式である。人間と AI エージェントの両方が、専用ツールなしで読み書きできることを目指す。本プロジェクトは OKF v0.2 を参照している。

OKF の用語は次のとおりである。

- Bundle: 知識文書をまとめたディレクトリ。本プロジェクトでは `docs/` が相当する。
- Concept: 1 つの知識を表す 1 つの Markdown ファイル。
- Concept ID: Bundle 内のファイルパスから `.md` を除いたもの。

OKF が必須とするのは、予約ファイル（`index.md`、`log.md`）以外のすべての `.md` に、空でない `type` を含む Frontmatter を付けることだけである。それ以外の規則は推奨や任意であり、OKF の利用側は未知の `type` や未知のキーを理由に文書を拒否してはならない。

## OKF が定義する Frontmatter

OKF が定義するキーは次のとおりである。

| キー          | 区分 | 内容                                                         |
| :------------ | :--- | :----------------------------------------------------------- |
| `type`        | 必須 | 概念の種別を表す短い文字列。値は中央管理されず、自由に決める |
| `title`       | 推奨 | 表示名。省略時はファイル名から導く                           |
| `description` | 推奨 | 1 文の要約。索引や検索結果の表示に使う                       |
| `resource`    | 推奨 | 対象となる実体を一意に示す URI。抽象的な概念には付けない     |
| `tags`        | 推奨 | 横断的な分類に使う短い文字列の配列                           |
| `status`      | 任意 | `draft`、`stable`（既定）、`deprecated` のいずれか           |
| `stale_after` | 任意 | 鮮度の期限。この時刻以降は古いとみなす絶対時刻               |
| `generated`   | 任意 | 内容の作成元。`{ by, at }` の形式で書く                      |
| `verified`    | 任意 | 検証の記録。`{ by, at }` の配列で、複数の検証を並べられる    |
| `sources`     | 任意 | 内容の根拠となった資料の一覧                                 |

補足は次のとおりである。

- 日時の値は、UTC オフセット付きの ISO 8601（例: `2026-06-30T14:00:00Z`）で書く。
- `by` には、エージェントなら `<producer>/<version>`、人間なら `human:<id>`、自動処理なら `process:<id>` と書く。
- `sources` の各項目は `resource` が必須で、`id`、`title`、`author`、`usage_count`、`last_modified` は任意である。本文では、`id` を脚注のラベルにして主張ごとの出典を示す。
- 独自のキーを追加してもよい。
- `verified` の有無から、利用側は信頼度（未検証、機械確認済み、人間レビュー済み）を判断する。
- `Attested Computation` 型と、それに付随する `runtime`、`parameters`、`executor`、`attester` などは、計算結果の検証用の仕様である。本プロジェクトでは使わない。

## OKF が定義する構造

OKF が定義するファイルとリンクの規則は次のとおりである。

- `index.md`: 各ディレクトリに置ける目次。Frontmatter は付けず、見出しごとに `* [タイトル](パス) - 短い説明` の形で並べる。バンドル直下の `index.md` だけは `okf_version` を Frontmatter に書ける。
- `log.md`: 各階層に置ける変更履歴。`## YYYY-MM-DD` の見出しで日付ごとにまとめ、新しい順に並べる。
- 予約名: `index.md` と `log.md` は目次と履歴の専用であり、知識文書の名前には使えない。
- リンク: 通常の Markdown リンクを使う。OKF は、`/` で始まる Bundle 基点の絶対パスを推奨し、相対パスも許容する。リンク切れは不正ではなく、未執筆の知識として扱う。
- 本文: 必須の節はない。見出し、リスト、表などの構造化した書き方を勧め、`# Schema`（項目の説明）と `# Examples`（使用例）に慣例上の意味がある。

OKF は、ディレクトリの分け方、`type` の分類、検証ツールを定めていない。参照実装（`reference_agent`）は、Bundle を生成・可視化するための例であり、文書を検証する仕組みではない。

## 本プロジェクトのルール

OKF が任意としていること、決めていないことについての本プロジェクトの決まりである。OKF と食い違うルールは置かない。

### Frontmatter

すべての文書（`index.md` と `log.md` を除く）に、次のキーをこの順で付ける。

| キー          | 本プロジェクトでの扱い | 書き方                                                                                     |
| :------------ | :--------------------- | :----------------------------------------------------------------------------------------- |
| `type`        | 必須                   | `spec`、`guideline`、`architecture`、`database-schema`、`decision`、`reference` のいずれか |
| `title`       | 必須                   | 本文の H1 と同じ文字列                                                                     |
| `description` | 必須                   | 1 文の要約。`index.md` の説明文にも使う                                                    |
| `tags`        | 必須                   | 検索用キーワードの配列（例: `[backend, go, architecture]`）                                |
| `status`      | 必須                   | `draft`、`stable`、`deprecated` のいずれか                                                 |
| `verified`    | 必須                   | `{ by: <actor>, at: <日時> }`。確かめた人や AI を書く                                      |
| `stale_after` | 必須                   | 鮮度の期限の日時。原則として `verified` の 1 年後                                          |

```yaml
---
type: guideline
title: '文書の構成'
description: '1 つの文書の組み立て方とファイル名のルール。'
tags: [documentation, structure]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---
```

- `type` の値は OKF では自由だが、本プロジェクトでは上の 6 種から選ぶ。外部資料の要約は `reference` にする。
- `verified` の `by` は事実どおりに書く。AI が確かめたなら `claude-code/<モデル名>`、人が読んで確かめたなら `human:<GitHub のユーザー名>` を書く。人が確かめたら、AI の記録を消さずに配列で追記する。
- `resource`、`generated`、`sources` は使わない。

### ディレクトリの役割と依存の向き

docs のディレクトリを、プロジェクトに依存しない知識と、プロジェクト固有の文書の 2 つに分ける。

| 区分               | ディレクトリ                                                             | 書くこと                             |
| :----------------- | :----------------------------------------------------------------------- | :----------------------------------- |
| プロジェクト非依存 | `knowledge/`                                                             | 汎用の設計知識と考え方               |
| プロジェクト非依存 | `references/`                                                            | 外部資料の要約                       |
| プロジェクト固有   | `guides/`、`frontend/`、`backend/`、`database/`、`dev-environment/` など | このプロジェクトのルール、設計、仕様 |

- 依存（リンクや「〜に従う」という参照）は、プロジェクト固有の文書から非依存の文書への一方向にする。
- `knowledge/` と `references/` には、プロジェクト固有の内容を書かない。プロジェクト固有の文書やソースコードへのリンク、「このプロジェクトでは〜」という記述、プロジェクトのルールの正であるという宣言がこれにあたる。
- `knowledge/` と `references/` の文書どうしは、互いにリンクしてよい。
- プロジェクトのルールを決めるときは、`knowledge/` や `references/` の文書を土台にしてリンクし、プロジェクトへの当てはめだけを書く。

こう分けるのは、`knowledge/` と `references/` を別のリポジトリへ持ち出し、他のプロジェクトでもルールの土台として使えるようにするためである。

### 目次（index.md）

- `docs/` と、その下のすべてのディレクトリに `index.md` を置く。
- `docs/index.md` だけは、Frontmatter に `okf_version: "0.2"` を書く。
- 各項目の説明文には、リンク先の `description` をそのまま使う。サブディレクトリは `[名前](サブディレクトリ/)` で載せる。
- 文書を追加・削除・改名したら、同じ変更でそのディレクトリの `index.md` を更新する。

### リンク

- docs 内の文書へのリンクは、`/` で始まる Bundle 基点のパスで書く（例: `/guides/writing.md`）。`/` は `docs/` を指す。
- `index.md` の中のリンクは、そのディレクトリからの相対パスで書く。
- docs の外（ソースコードなど）へのリンクは、相対パスで書く。
- GitHub の画面では `/` 始まりのリンクはリポジトリの最上位を基準に解釈され、辿れない。これは承知のうえで OKF の推奨に従う。

### 使わない機能

`log.md` と `Attested Computation` 型は使わない。変更履歴は git で追う。

## See also

- [文書の保守](/guides/maintenance.md)
- [文書の構成](/guides/document-structure.md)
- [Markdown の書き方](/guides/markdown-style.md)
- [Open Knowledge Format 仕様 (SPEC.md)](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- [Open Knowledge Format (Google Cloud)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
