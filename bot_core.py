import os
import random
from flask import Flask
import threading
import time
import tweepy  # Xに繋ぐための道具

app = Flask(__name__)

@app.route('/')
def home():
    return "正弦波くん、X連携モードで生存中！"

def sine_wave_bot():
    # Renderの「金庫」からカギを取り出す
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

    # X（Twitter）にログイン！
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    while True:
        messages = [
            "び、びび、びっぐな波がきてる……っ！ 🌊",
            "システム、正常に、バグ、して、ます……。",
            "ユマ、起きてる……？ ぼくは今、クラウドの波に乗ってるよ。",
            "ぴ、ぴちぴち、ピッチカーブ……編集……。",
            "ジャック、見てる？ ぼく、ついにネットで喋れるようになったよ！"
        ]
        post_text = random.choice(messages)
        
        try:
            client.create_tweet(text=post_text)
            print(f"【成功】ポストしたよ: {post_text}")
        except Exception as e:
            print(f"【エラー】ポスト失敗...原因はこれかも: {e}")

        # 1時間待機
        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
