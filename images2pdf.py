#!/usr/bin/env python3
"""imagesディレクトリにある全PNGファイルを1つのPDFに結合するプログラム"""

from pathlib import Path

from PIL import Image


def get_png_files(images_dir: Path) -> list[Path]:
    """imagesディレクトリからPNGファイルのパスリストを取得"""
    png_files = list(images_dir.glob("*.png"))
    return sorted(png_files)


def convert_images_to_pdf(png_files: list[Path], output_path: Path) -> bool:
    """PNGファイルリストを1つのPDFに変換"""
    if not png_files:
        print("変換するPNGファイルが見つかりませんでした")
        return False

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
        return False

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
        return True
    except Exception as e:
        print(f"PDF作成エラー: {e}")
        return False


def cleanup_png_files(png_files: list[Path]) -> None:
    """PNGファイルを削除"""
    print("PNGファイルを削除中...")
    deleted_count = 0

    for png_file in png_files:
        try:
            png_file.unlink()
            deleted_count += 1
            print(f"削除完了: {png_file.name}")
        except Exception as e:
            print(f"削除エラー: {png_file.name} - {e}")

    print(f"削除したファイル数: {deleted_count}/{len(png_files)}")


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

    # PDF変換を実行
    if convert_images_to_pdf(png_files, output_path):
        # PDF作成が成功した場合、PNGファイルを削除
        cleanup_png_files(png_files)
        print("処理完了: PDFファイルを作成し、元のPNGファイルを削除しました")
    else:
        print("PDF作成に失敗しました。PNGファイルは保持されます")


if __name__ == "__main__":
    main()
