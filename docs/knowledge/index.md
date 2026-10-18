# 共通設計ナレッジ

- [テスト設計における AAA パターン](aaa-pattern.md) - 単体テストを Arrange・Act・Assert の 3 段で構成する原則。
- [コードを書くときに意識すること](coding-mindset.md) - 書く前に既存の解決策を探し、小さく読みやすく、テストで仕様を示すコードを保つための心構え。
- [関数のシグネチャの読み方と決め方](function-signatures.md) - 関数の名前・引数・戻り値からなるシグネチャの意味と、中身より先にシグネチャを決める手順。
- [半角・全角記号の使い分けルール](bracket-and-character-rules.md) - コードや文書での半角・全角記号の使い分けルール。
- [プログラミングでよく使われる定番命名パターン](naming-patterns.md) - プログラミングでよく使われる定番の命名パターン集。
- [Package by Feature 設計指針](package-by-feature.md) - コードを技術レイヤーではなく業務機能単位で分割する設計指針。
- [React カスタムフックの責務分離とライフサイクル設計指針](react-hook-separation-and-lifecycle.md) - React カスタムフックで状態とロジックを分離し、ライフサイクルを設計する指針。
- [React の画面の切り替えと state のリセット](react-state-reset-by-position.md) - React の state がツリー上の位置で管理されることを使い、画面を切り替えたときに state を作り直す設計の指針。
- [Next.js の app/ と features/ の分担](nextjs-app-and-features.md) - Next.js の App Router で、app/ をルーティング専用の薄い入口にし、機能のコードを features/ にまとめる指針。
- [テーブル駆動テストの設計指針](table-driven-tests.md) - Go でテストケースを表として並べて網羅的に検証するテスト設計。
- [Go のテストで t.Fatalf と t.Errorf を使い分ける](test-fatal-vs-error.md) - Go のテストで、失敗したときに後ろの確認へ進むかどうかで t.Fatalf と t.Errorf を選ぶ基準。
- [Go の Repository 層のテストの設計指針](go-repository-testing.md) - Go で DB にアクセスする Repository 層を、本物の DB に対してテストするときの接続・データの分け方・確かめる範囲の指針。
