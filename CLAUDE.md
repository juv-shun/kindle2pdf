# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

kindle2pdfは、Kindle アプリからスクリーンショットを自動取得してページ画像を生成し、それらを1つのPDFファイルに結合するPythonツールです。pyautoguiとPillowを使用してKindleのページめくり操作を自動化し、連続的にスクリーンショットを撮影、最終的にPDFとして出力します。

## 開発環境

- Python 3.13以上が必要
- パッケージ管理：`uv`
- 主要な依存関係：pillow, pyautogui

## 開発コマンド

- 依存関係のインストール：`make install` または `uv sync`
- **Kindle2PDF実行（推奨）：`make` または `make kindle2pdf`** - スクリーンショット取得からPDF変換まで連続実行
- スクリーンショット取得のみ：`make images` または `uv run python kindle2images.py`
- PDF変換のみ：`make pdf` または `uv run python images2pdf.py`
- Linter/Formatter：`make check` または `uv run ruff check . && uv run ruff format .`
- クリーンアップ：`make clean`

## アーキテクチャ

### 構成ファイル
- `Makefile`：ビルドスクリプト（連続実行、個別実行、クリーンアップ等）
- `kindle2images.py`：スクリーンショット取得プログラム
- `images2pdf.py`：PNG画像をPDFに変換するプログラム
- `config.json`：設定ファイル（スクリーンショット範囲、Kindleアプリ名、ページめくり設定等）
- `pyproject.toml`：プロジェクト設定とパッケージ依存関係

### 主要な処理フロー

#### スクリーンショット取得 (kindle2images.py)
1. 設定ファイル読み込み
2. Kindleアプリをアクティブ化
3. ユーザーがページ位置を設定後、Kindleをフルスクリーン化
4. 別スレッドで終了監視開始
5. スクリーンショット取得ループ（ページ変化がなくなるまで継続）
6. 取得した画像を`images/`ディレクトリに保存

#### PDF変換 (images2pdf.py)
1. `images/`ディレクトリからPNGファイルを検索・ソート
2. 各画像をRGB形式に変換（PDF互換性のため）
3. 全画像を1つのPDFファイルに結合
4. `pdf/kindle_book.pdf`として出力
5. PDF作成成功時、元のPNGファイルを自動削除（失敗時は保持）

### 設定可能項目
- `screenshot_region`：スクリーンショット範囲（x, y, width, height）
- `kindle_app_name`：Kindleアプリケーション名
- `page_turn_delay`：ページめくり間隔（秒）
- `activation_delay`：アプリ切り替え待機時間（秒）
- `page_turn_direction`：ページめくり方向（キー名）

## 開発ルール

### ドキュメント更新の必須要件
仕様変更や新機能追加を実装する際は、必ず以下のドキュメントを更新すること：

1. **CLAUDE.md**: 
   - 処理フローの変更
   - 新しい設定項目の追加
   - アーキテクチャの変更
   - 開発コマンドの追加

2. **README.md**:
   - 使用方法の変更
   - 新機能の説明
   - 注意事項の追加
   - 設定項目の変更

この要件を満たさない場合、実装は不完全とみなす。