# kindle2pdf

Kindle アプリからスクリーンショットを自動取得して PDF ファイルを生成する Python ツールです。

## 概要

kindle2pdf は、Kindle アプリのページを自動的にスクリーンショット撮影し、それらの画像を 1 つの PDF ファイルに結合するツールです。pyautogui を使用してページめくり操作を自動化し、Pillow を使って画像処理と PDF 生成を行います。

## 主な機能

- Kindle アプリの自動ページめくり
- 連続スクリーンショット取得
- PNG 画像の自動 PDF 変換
- 設定可能なスクリーンショット範囲とタイミング

## 必要な環境

- Python 3.13 以上
- macOS（osascript を使用）
- Amazon Kindle アプリ

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

1. Kindle アプリが自動的にアクティブ化されます
2. 読み始めたいページに Kindle を配置してください。
   - フルスクリーンは解除した状態で始めてください。
3. 自動的に、フルスクリーンになり、スクリーンショット取得が自動で開始されます
4. 終了する場合は`Ctrl+C`を押してください

### 3. PDF 変換

```bash
uv run python images2pdf.py
```

`images/`ディレクトリ内の PNG 画像が`pdf/kindle_book.pdf`として結合されます。

**注意**: PDF 作成が正常に完了すると、元の PNG ファイルは自動的に削除されます。PDF 作成に失敗した場合、PNG ファイルは保持されます。

## 出力ファイル

- `images/`: スクリーンショット画像（PNG 形式）※PDF 作成後は自動削除
- `pdf/kindle_book.pdf`: 結合された PDF ファイル

## 設定項目

| 項目                  | 説明                                         | デフォルト値         |
| --------------------- | -------------------------------------------- | -------------------- |
| `screenshot_region`   | スクリーンショット範囲 [x, y, width, height] | [70, 70, 1850, 1000] |
| `kindle_app_name`     | Kindle アプリケーション名                    | "Amazon Kindle"      |
| `page_turn_delay`     | ページめくり間隔（秒）                       | 0.8                  |
| `activation_delay`    | アプリ切り替え待機時間（秒）                 | 3                    |
| `page_turn_direction` | ページめくり方向                             | "left"               |

## 開発

```bash
# Linter/Formatter実行
uv run ruff check .
uv run ruff format .
```

## 注意事項

- macOS 専用ツールです
- スクリーンショット範囲は環境に応じて調整が必要な場合があります
- 著作権法を遵守してご利用ください
