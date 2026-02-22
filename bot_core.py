import os
import random
from flask import Flask
import threading
import time
import tweepy
from googleapiclient.discovery import build  # ←Google先生を呼ぶための新機能！

app = Flask(__name__)

@app.route('/')
def home():
    return "正弦波くん、エゴサ進化モードで生存中！"

# --- ここからGoogle検索の魔法 ---
def google_search(query):
    api_key = os.environ.get("GOOGLE_API_KEY")
    cx = os.environ.get("SEARCH_ENGINE_ID")
    
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        # 1件だけ最新の情報を取ってくる！
        result = service.cse().list(q=query, cx=cx, num=1).execute()
        
        if 'items' in result:
            title = result['items'][0]['title']
            link = result['items'][0]['link']
            return f"「{title}」っていう波を見つけたよ……っ！ {link}"
    except Exception as e:
        print(f"検索エラーになっちゃった: {e}")
    return None
# --- ここまで ---

def sine_wave_bot():
    # Xの鍵をセット
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    while True:
            # これが正弦波くんの「新しい視界」だぜ！！ 🌊
        search_words = [
            "UTAU", 
            "UTAU キャラクター",
            "バニラアイス", 
            "イチゴアイス",
            "正弦波"
        ]
        
        # Googleでエゴサしてみる
        news = google_search(word)
        
        if news:
            post_text = f"ぼく、エゴサしてきました……っ！\n{word}の波：{news}"
        else:
            # 検索に失敗した時のいつものセリフ
            messages = [
                "び、びび、びっぐな波がきてる……っ！ 🌊",
                "ジャック、見てる？ ぼく、ネットの波を泳いでるよ！",
                "ピッチカーブ編集……ユマ、頑張って……っ！"
            ]
            post_text = random.choice(messages)
        
        try:
            client.create_tweet(text=post_text)
            print(f"【成功】エゴサ結果をポストしたよ: {post_text}")
        except Exception as e:
            print(f"【エラー】失敗...: {e}")

        # 1時間待機（テストならもっと短くしてもいいよ！）
        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
