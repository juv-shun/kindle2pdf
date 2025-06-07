#!/usr/bin/env python3
"""imagesディレクトリにある全PNGファイルを1つのPDFに結合するプログラム"""

from pathlib import Path

from PIL import Image


def get_png_files(images_dir: Path) -> list[Path]:
    """imagesディレクトリからPNGファイルのパスリストを取得"""
    png_files = list(images_dir.glob("*.png"))
    return sorted(png_files)


def convert_images_to_pdf(png_files: list[Path], output_path: Path) -> None:
    """PNGファイルリストを1つのPDFに変換"""
    if not png_files:
        print("変換するPNGファイルが見つかりませんでした")
        return

    images = []

    for png_file in png_files:
        try:
            img = Image.open(png_file)
            # PNGがRGBAの場合、RGBに変換(PDFはRGBAをサポートしない)
            if img.mode == "RGBA":
                img = img.convert("RGB")
            images.append(img)
            print(f"読み込み完了: {png_file.name}")
        except Exception as e:
            print(f"エラー: {png_file.name} を読み込めませんでした - {e}")
            continue

    if not images:
        print("有効なPNGファイルが見つかりませんでした")
        return

    try:
        # 最初の画像をベースにして、残りの画像をPDFに追加
        images[0].save(
            output_path,
            "PDF",
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
        )
        print(f"PDF作成完了: {output_path}")
        print(f"変換したページ数: {len(images)}")
    except Exception as e:
        print(f"PDF作成エラー: {e}")


def main() -> None:
    """メイン処理"""
    images_dir = Path("images")
    pdf_dir = Path("pdf")
    output_path = pdf_dir / "kindle_book.pdf"

    # PDFディレクトリが存在しない場合は作成
    pdf_dir.mkdir(exist_ok=True)

    if not images_dir.exists():
        print(f"エラー: {images_dir} ディレクトリが存在しません")
        return

    print(f"{images_dir} ディレクトリからPNGファイルを検索中...")
    png_files = get_png_files(images_dir)

    if not png_files:
        print("PNGファイルが見つかりませんでした")
        return

    print(f"見つかったPNGファイル数: {len(png_files)}")
    convert_images_to_pdf(png_files, output_path)


if __name__ == "__main__":
    main()
