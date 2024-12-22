import time
import subprocess
from threading import Thread

# サーバーを起動
print("サーバーを起動します。")
streamlit_process = subprocess.Popen(["streamlit", "run", "app/src/データアップロード.py"])
fastapi_process = subprocess.Popen(["uvicorn", "app.src.train_api:app", "--reload"])

# 「Ctrl+C」が入力されたらサーバーを停止させる
try:
    while True:
        time.sleep(5)
        print("サーバーが実行中です。Ctrl+Cで停止します。")
except KeyboardInterrupt:
    streamlit_process.terminate()
    fastapi_process.terminate()
    print("サーバーを停止します。")
