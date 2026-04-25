import subprocess
import time
import sys
import socket
import os

def is_port_open(port):
    """ポートが開放されているか確認する"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def launch_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engine_dir = os.path.join(base_dir, "engine")
    
    print("🚀 1/2: FastAPI サーバーを起動しています...")
    # main.py を別プロセスで起動
    api_process = subprocess.Popen([sys.executable, "main.py"], cwd=engine_dir)

    # モデルのロード待ち 
    print("⏳ モデルを読み込んでいます（数秒〜十数秒かかります）...")
    
    # ポート 8000 が開くのを待機
    attempts = 0
    while not is_port_open(8000):
        time.sleep(2)
        attempts += 1
        if attempts > 30: # 最大60秒待機
            print("❌ サーバーの起動に時間がかかりすぎています。")
            break
    
    print("✅ API サーバーの準備が整いました。")
    print("🚀 2/2: Gradio 画面を起動します...")

    # chat.py を起動
    try:
        subprocess.run([sys.executable, "chat.py"], cwd=engine_dir)
    except KeyboardInterrupt:
        print("\n終了しています...")
    finally:
        # スクリプトを閉じたらAPIサーバーも終了させる
        api_process.terminate()

if __name__ == "__main__":
    launch_all()
