# kindle2pdf

Kindleアプリからスクリーンショットを自動取得してPDFファイルを生成するPythonツールです。

## 概要

kindle2pdfは、Kindleアプリのページを自動的にスクリーンショット撮影し、それらの画像を1つのPDFファイルに結合するツールです。pyautoguiを使用してページめくり操作を自動化し、Pillowを使って画像処理とPDF生成を行います。

## 主な機能

- Kindleアプリの自動ページめくり
- 連続スクリーンショット取得
- PNG画像の自動PDF変換
- 設定可能なスクリーンショット範囲とタイミング

## 必要な環境

- Python 3.13以上
- macOS（osascriptを使用）
- Amazon Kindleアプリ

## インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd kindle2pdf

# 依存関係をインストール
uv sync
```

## 使用方法

### 1. 設定ファイルの準備

`config.json`でスクリーンショット範囲やアプリ設定を調整できます：

```json
{
  "screenshot_region": [70, 70, 1850, 1000],
  "kindle_app_name": "Amazon Kindle",
  "page_turn_delay": 0.8,
  "activation_delay": 3,
  "page_turn_direction": "left"
}
```

### 2. スクリーンショット取得

```bash
uv run python kindle2images.py
```

1. Kindleアプリが自動的にアクティブ化されます
2. 読み始めたいページにKindleを配置してください
3. Kindleをフルスクリーンモードにしてください
4. スクリーンショット取得が自動で開始されます
5. 終了する場合は`Ctrl+C`を押してください

### 3. PDF変換

```bash
uv run python images2pdf.py
```

`images/`ディレクトリ内のPNG画像が`pdf/kindle_book.pdf`として結合されます。

**注意**: PDF作成が正常に完了すると、元のPNGファイルは自動的に削除されます。PDF作成に失敗した場合、PNGファイルは保持されます。

## 出力ファイル

- `images/`: スクリーンショット画像（PNG形式）※PDF作成後は自動削除
- `pdf/kindle_book.pdf`: 結合されたPDFファイル

## 設定項目

| 項目 | 説明 | デフォルト値 |
|------|------|-------------|
| `screenshot_region` | スクリーンショット範囲 [x, y, width, height] | [70, 70, 1850, 1000] |
| `kindle_app_name` | Kindleアプリケーション名 | "Amazon Kindle" |
| `page_turn_delay` | ページめくり間隔（秒） | 0.8 |
| `activation_delay` | アプリ切り替え待機時間（秒） | 3 |
| `page_turn_direction` | ページめくり方向 | "left" |

## 開発

```bash
# Linter/Formatter実行
uv run ruff check .
uv run ruff format .
```

## 注意事項

- macOS専用ツールです
- Kindleアプリが起動している必要があります
- スクリーンショット範囲は環境に応じて調整が必要な場合があります
- 著作権法を遵守してご利用ください