import os
import random
from flask import Flask
import threading
import time
import tweepy
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/')
def home():
    return "正弦波くん、エゴサ進化モードで生存中！"

# --- Google検索の魔法（エラー対策済み！） ---
def google_search(query):
    api_key = os.environ.get("GOOGLE_API_KEY")
    cx = os.environ.get("SEARCH_ENGINE_ID")
    
    if not api_key or not cx:
        print("【警告】環境変数が足りないよ！Renderの設定を確認してね。")
        return None
    
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        # 確実に1件の中身を拾う設定
        result = service.cse().list(q=query, cx=cx, num=1).execute()
        
        if 'items' in result and len(result['items']) > 0:
            item = result['items'][0]
            title = item['title']
            link = item['link']
            return f"{title} {link}"
    except Exception as e:
        print(f"検索エラーが発生したよ……っ！: {e}")
    return None

def sine_wave_bot():
    # Xの鍵をセット
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    while True:
        # 1. ユマ指定の最強検索リスト！
        search_words = ["UTAU", "UTAU キャラクター", "バニラアイス", "イチゴアイス", "正弦波"]
        target_word = random.choice(search_words)
        
        # 2. 検索実行！
        news_content = google_search(target_word)
        
        if news_content:
            # 検索成功時のポスト
            post_text = f"ぼく、エゴサしてきました……っ！\n{target_word}の波：{news_content}"
        else:
            # 失敗した時のいつものセリフ
            messages = [
                "び、びび、びっぐな波がきてる……っ！ 🌊",
                "ジャック、見てる？ ぼく、ネットの波を泳いでるよ！",
                "ピッチカーブ編集……ユマ、頑張って……っ！"
            ]
            post_text = random.choice(messages)
        
        try:
            client.create_tweet(text=post_text)
            print(f"【成功】ポストしたよ: {post_text}")
        except Exception as e:
            print(f"【エラー】ポスト失敗: {e}")

        # 最初は15分(900秒)くらいに設定しておくと、すぐ確認できて楽しいかも！
        # 1時間なら 3600 にしてね。
        time.sleep(3600)

if __name__ == "__main__":
    # ボットを別スレッドで開始
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    
    # Renderのポートに合わせてFlaskを起動
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
