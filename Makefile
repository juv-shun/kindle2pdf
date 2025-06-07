.PHONY: all kindle2pdf images pdf clean lint format check

# デフォルトターゲット：スクリーンショット取得→PDF変換
all: kindle2pdf

# Kindle2PDF実行（スクリーンショット取得→PDF変換）
kindle2pdf:
	@echo "=== Kindle スクリーンショット取得を開始します ==="
	uv run python kindle2images.py
	@echo "=== PDF変換を開始します ==="
	uv run python images2pdf.py
	@echo "🎉 Kindle2PDF処理が正常に完了しました！"

# スクリーンショット取得のみ
images:
	uv run python kindle2images.py

# PDF変換のみ
pdf:
	uv run python images2pdf.py

# 依存関係のインストール
install:
	uv sync

# クリーンアップ
clean:
	rm -rf images/*.png
	rm -rf pdf/*.pdf

# Linter実行
lint:
	uv run ruff check .

# フォーマッター実行
format:
	uv run ruff format .

# Linter + フォーマッター
check: lint format