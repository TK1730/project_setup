# project_setup

今使っている PC の環境構築、今後使用するためのDocker 環境、CI/CD の取説を残すリポジトリです。

---

## 📄 各種セットアップ手順書

### 1. [GoogleドライブのデータセットをローカルPCで使うための環境構築手順書](SETUP_GoogleDrive_to_LocalPC_Streaming.md)
Google ドライブ上の大容量データセットをローカル PC（Windows/WSL）のストレージを消費せずに仮想ドライブとしてマウントし、開発環境から直接ストリーミングで利用するための手順です。

#### 💡 実施した操作
1. **Google Cloud 側の設定**:
   * Google Cloud Console にてプロジェクト（プロジェクト名：`my-rclone-project`）を作成。
   * Google Drive API を有効化。
   * Google Auth Platform（OAuth 同意画面）の初期構成を完了（公開ステータスを公開状態に変更）。
   * 独自の **OAuth クライアント ID（デスクトップ アプリ）** を作成。
2. **WSL2（Linux）側の設定**:
   * WSL2 に `rclone` および `fuse3` をインストール。
   * Windows 側の設定（`rclone.conf`）をコピーして同期。
   * `rclone mount` コマンドにより、`~/workspace/gdrive` ディレクトリへの Google ドライブのマウント（読み込み専用）に成功。
   * `~/.bashrc` に自動マウント設定（多重起動防止付き）を追記し、WSL2 起動時の自動マウント化を完了。

#### ⏭️ 次に行う操作
* 作成したマウントディレクトリ（`~/workspace/gdrive`）を利用し、Docker コンテナやローカル開発環境（VS Code / Cursor 等）からデータセットのストリーミング利用を開始します。
* 詳細な手順や Docker ボリュームマウントの設定は、[SETUP_GoogleDrive_to_LocalPC_Streaming.md](SETUP_GoogleDrive_to_LocalPC_Streaming.md) を参照してください。
