import os
import random
from flask import Flask
import threading
import time

# Renderに「サイトですよ〜」って嘘をつくための設定
app = Flask(__name__)

@app.route('/')
def home():
    return "正弦波くん、生存確認OK！"

def sine_wave_bot():
    while True:
        messages = [
            "び、びび、びっぐな波がきてる……っ！ 🌊",
            "システム、正常に、バグ、して、ます……。",
            "ユマ、起きてる……？ ぼくは今、Renderっていう神の席にいるよ。",
            "ぴ、ぴちぴち、ピッチカーブ……編集……。",
            "マジツリのジャックもびっくりな高所だね！"
        ]
        post_text = random.choice(messages)
        print(f"【ログ】正弦波くんの独り言: {post_text}")
        
        # 本物のX投稿コードはAPIキーをもらってからここに書こう！
        
        # 1時間（3600秒）ごとに喋るようにするよ
        time.sleep(3600)

if __name__ == "__main__":
    # 正弦波くんの脳を別ルート（スレッド）で動かす
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    
    # サイトとしての受付を開始する
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
