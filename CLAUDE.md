# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

kindle2pdfは、Kindle アプリからスクリーンショットを自動取得してページ画像を生成するPythonツールです。pyautoguiとPillowを使用してKindleのページめくり操作を自動化し、連続的にスクリーンショットを撮影します。

## 開発環境

- Python 3.13以上が必要
- パッケージ管理：`uv`
- 主要な依存関係：pillow, pyautogui

## 開発コマンド

- 依存関係のインストール：`uv sync`
- プログラム実行：`uv run python kindle2images.py`
- Linter/Formatter：`uv run ruff check .` および `uv run ruff format .`

## アーキテクチャ

### 構成ファイル
- `kindle2images.py`：メインプログラム
- `config.json`：設定ファイル（スクリーンショット範囲、Kindleアプリ名、ページめくり設定等）
- `pyproject.toml`：プロジェクト設定とパッケージ依存関係

### 主要な処理フロー
1. 設定ファイル読み込み
2. Kindleアプリをアクティブ化
3. ユーザーがページ位置を設定後、Kindleをフルスクリーン化
4. 別スレッドで終了監視開始
5. スクリーンショット取得ループ（ページ変化がなくなるまで継続）
6. 取得した画像を`images/`ディレクトリに保存

### 設定可能項目
- `screenshot_region`：スクリーンショット範囲（x, y, width, height）
- `kindle_app_name`：Kindleアプリケーション名
- `page_turn_delay`：ページめくり間隔（秒）
- `activation_delay`：アプリ切り替え待機時間（秒）
- `page_turn_direction`：ページめくり方向（キー名）