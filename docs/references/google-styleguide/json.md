---
type: reference
title: 'Google JSON Style Guide（要約）'
description: 'Google JSON Style Guide の要約（API の JSON の命名と値の形式）。'
tags: [json, api-design, openapi, google-styleguide, reference]
status: stable
verified: { by: claude-code/claude-sonnet-5-5, at: 2026-10-01T00:00:00Z }
stale_after: 2027-10-01T00:00:00Z
---

# Google JSON Style Guide（要約）

REST API のリクエスト/レスポンス JSON（OpenAPI）を設計するときの参考として、Google JSON Style Guide（Revision 0.9）の要点をまとめた外部ガイドの要約である。プロパティ名と値の形式のルールは今でも参考になるが、`data` / `error` で包むレスポンス構造は古い慣習なので、参考情報として扱う。

## 概要

- 対象は RPC / REST 両方の JSON リクエストとレスポンス（原典 Introduction）。
- 基本は [JSON.org](https://www.json.org) の仕様に従い、Google 内の API の見た目を揃えるための補足ルールという位置づけ。
- コメントは JSON に含めない。文字列とプロパティ名は二重引用符で囲む（原典 Comments / Double Quotes）。
- 便宜的にデータをグループ化せず、意味のあるまとまり（住所など）のときだけ入れ子にする（原典 Flattened data vs Structured Hierarchy）。

## プロパティの命名

原典の Property Name Format / Singular vs Plural Property Names による。

- 意味が明確な名前にする。ASCII の camelCase にする。
- 先頭は英字、`_`、`$` のいずれか。JavaScript の予約語は避ける。JavaScript の識別子と同じ規則なので、クライアントが `result.fooBar` とドット記法で読める。
- 配列のプロパティ名は複数形、それ以外は単数形にする。

```json
{ "author": "lisa", "siblings": ["bart", "maggie"] }
```

- 例外として、数を表す `totalItems` のような名前は許容される。`itemCount` のように単数形に言い換えてもよい。
- JSON オブジェクトをマップとして使う場合、キーにはこの命名規則が適用されず、任意の Unicode 文字を使える。API ドキュメントでマップであることを明記する（原典 Key Names in JSON Maps）。

```json
{ "thumbnails": { "72": "https://example.com/72.png" } }
```

## 値の形式

原典の Property Value Format / Empty/Null Property Values / Enum Values / Property Value Data Types による。

- 値は真偽値、数値、Unicode 文字列、オブジェクト、配列、`null` のいずれか。数値には数値型を使うなど、用途に合う型を選ぶ。
- 省略可能なプロパティや空・`null` の値は、省く方向で検討する。ただし `0` のように意味を持つ値は残す。
- 列挙値は文字列で表す。列挙値が追加・変更されても、クライアントが壊れにくくなるため。

```json
{ "color": "WHITE" }
```

- 日付時刻は RFC 3339 形式の文字列にする。

```json
{ "lastUpdate": "2007-11-06T16:34:41.000Z" }
```

- 期間は ISO 8601 の期間形式の文字列にする。

```json
{ "duration": "P3Y6M4DT12H30M5S" }
```

- 緯度経度は ISO 6709 形式の文字列で、`±DD.DDDD±DDD.DDDD` を推奨する（原典 Latitude/Longitude Property Values）。

```json
{ "statueOfLiberty": "+40.6894-074.0447" }
```

## レスポンス構造（参考）

原典の JSON Structure & Reserved Property Names による。この節は古い慣習として、参考情報にとどめる。

- トップレベルに `apiVersion`、`data`、`error` などの予約プロパティを置く構造を推奨している。予約プロパティは必須ではない。
- 成功時は `data`、失敗時は `error` を使い、同時には出さない。
- `data` 内の `items`（配列）、ページング（`totalItems`、`pageIndex`、`nextLink` など）、`error` 内の `code`、`message`、`errors[]`（`domain`、`reason`）が定義されている。

```json
{ "data": { "items": [], "totalItems": 0 } }
```

```json
{ "error": { "code": 404, "message": "File Not Found" } }
```

- 予約名とのバージョン衝突は、別名を選ぶか、メジャーバージョンで改名して避ける（原典 Naming Conflicts）。

## See also

- [命名パターン](/knowledge/naming-patterns.md)
- [Google JSON Style Guide（原典）](https://raw.githubusercontent.com/google/styleguide/gh-pages/jsoncguide.md)
