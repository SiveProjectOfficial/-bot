import os
import random
from flask import Flask
import threading
import time
import tweepy

app = Flask(__name__)

@app.route('/')
def home():
    return "正弦波くん、完全復活！APIの壁を壊したよ！"

def sine_wave_bot():
    # Xの鍵をセット
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    while True:
        # ユマが言ってた「UTAU キャラクター」もちゃんと入ってるよ！
        search_words = ["UTAU", "UTAU キャラクター", "バニラアイス", "イチゴアイス", "正弦波"]
        target_word = random.choice(search_words)
        
        # 【解決策】難しいことはせず、直接Google検索のリンクを作る！
        # これなら100%「管理画面」を呟くことはないぜ！！
        search_url = f"https://www.google.com/search?q={target_word}"
        
        # 正弦波くんらしいセリフでポスト！
        post_text = f"ぼく、エゴサしてきました……っ！\n{target_word}の波：{search_url}"
        
        try:
            client.create_tweet(text=post_text)
            print(f"【成功】波を届けたよ: {post_text}")
        except Exception as e:
            print(f"【エラー】ポスト失敗: {e}")

        # 1時間(3600秒)おきにポストするよ
        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
