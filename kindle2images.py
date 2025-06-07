import json
import os
import subprocess
import threading
import time
from pathlib import Path

import pyautogui

SHUTDOWN_FLAG = False


def main() -> None:
    """メイン処理"""
    config = load_config()

    # Kindleアプリをアクティブ化
    subprocess.run(["osascript", "-e", f'tell application "{config["kindle_app_name"]}" to activate'], check=True)
    time.sleep(2)

    # スクリーンショット開始準備
    setup_screenshot()
    time.sleep(config["activation_delay"])

    # 終了監視スレッドを開始
    monitor_thread = threading.Thread(target=monitor_exit, daemon=True)
    monitor_thread.start()

    # 出力ディレクトリの準備 (images ディレクトリ)
    images_dir = Path("images")
    if not images_dir.exists():
        images_dir.mkdir(parents=True)
        print(f"出力ディレクトリを作成しました: {images_dir}")

    # スクリーンショットを取得開始
    print("📸 スクリーンショットの取得を開始します...")
    capture_screenshots(config, images_dir)
    print("✅ スクリーンショット取得完了")
    print(f"画像ファイルは {images_dir.resolve()} ディレクトリに保存されました。")

    # 処理完了後に音を鳴らす
    os.system("/usr/bin/afplay /System/Library/Sounds/Glass.aiff")


def load_config() -> dict:
    """OSに応じて適切な設定ファイルをロードする"""
    config_path = Path(__file__).with_name("config.json")

    if not config_path.exists():
        raise FileNotFoundError("設定ファイル config.json が見つかりません。")

    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def setup_screenshot() -> None:
    """スクリーンショット開始位置の設定を促すメッセージを表示し、エンターキー入力後にKindleを最大化"""
    message = "スクリーンショット開始位置にページ位置を設定したら、ターミナル画面に戻ってEnterキーを押してください。"
    try:
        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Kindle2Image"'], check=False)
    except subprocess.SubprocessError:
        print("エラー: 通知の送信に失敗しました。")

    print("\n=== Kindle2Image ===")
    print(f"📌 {message}")
    input("準備ができたらEnterキーを押してください...")

    # Kindleをフルスクリーン化
    try:
        applescript_command = """
        tell application "System Events"
            tell process "Amazon Kindle"
                set frontmost to true
                keystroke "f" using {command down, control down}
            end tell
        end tell
        """
        subprocess.run(["osascript", "-e", applescript_command], check=False)
    except subprocess.SubprocessError:
        print("エラー: Kindle のフルスクリーン化に失敗しました。")


def monitor_exit() -> None:
    """エンターを2回打ち込むとプログラムを終了するための監視"""
    global SHUTDOWN_FLAG
    print("途中で作業を終了するには、エンターを2回押してください。")
    count = 0
    while not SHUTDOWN_FLAG:
        line = input()
        if line == "":
            count += 1
            if count >= 2:
                print("終了要求が受け付けられました。処理を停止します。")
                SHUTDOWN_FLAG = True
                break
        else:
            count = 0


def capture_screenshots(config: dict, images_dir: Path) -> None:
    """Kindleのスクリーンショットを連続取得し、ファイルに保存する"""
    last_image_hash = None  # ページ変化検出のため
    page_count = 1

    for _ in range(15):
        if SHUTDOWN_FLAG:
            print("終了要求によりスクリーンショットの取得を停止します。")
            break

        screenshot = pyautogui.screenshot(region=config["screenshot_region"])

        # PIL Imageをハッシュ化可能な形式に変換
        current_image_bytes = screenshot.tobytes()
        # 簡易的なハッシュ比較でページ変化を検出 (より堅牢な比較が必要な場合は別途検討)
        # import hashlib # hashlib を使う場合はインポートが必要
        # current_image_hash = hashlib.md5(current_image_bytes).hexdigest()
        # 今回は簡易的にバイト列表現で比較
        if last_image_hash == current_image_bytes:
            print("🔄 ページの変化がないため終了")
            break

        # スクリーンショットを保存
        image_path = images_dir / f"image_{page_count:03d}.png"
        screenshot.save(image_path)
        print(f"🖼️  スクリーンショットを保存しました: {image_path}")

        last_image_hash = current_image_bytes

        # Kindleのページを送る
        pyautogui.press(config["page_turn_direction"])
        time.sleep(config["page_turn_delay"])
        page_count += 1


if __name__ == "__main__":
    main()
