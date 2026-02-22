import os
import random
import threading
import time
import tweepy
from flask import Flask
from googleapiclient.discovery import build
import re

app = Flask(__name__)

# --- マルコフ連鎖：正弦波くんの思考回路 ---
def make_markov_text(source_text):
    # 日本語の助詞や単語で簡易分割（エゴサした言葉の破片を作る）
    words = re.findall(r'[ぁ-んァ-ヶー一-龠]+', source_text)
    if len(words) < 5: return None
    
    markov = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        if key not in markov: markov[key] = []
        markov[key].append(words[i+2])
    
    # 文章を組み立てる
    try:
        current_key = random.choice(list(markov.keys()))
        result_words = list(current_key)
        for _ in range(20): # 20単語くらい繋げる
            if current_key in markov:
                next_word = random.choice(markov[current_key])
                result_words.append(next_word)
                current_key = (result_words[-2], result_words[-1])
            else:
                break
        return "".join(result_words)
    except:
        return None

# --- エゴサ：材料仕入れ ---
def get_ego_search_material():
    api_key = os.environ.get("GOOGLE_API_KEY")
    cx = os.environ.get("SEARCH_ENGINE_ID")
    service = build("customsearch", "v1", developerKey=api_key)

    # ユマ特選：UTAU・トレンド・アイス限定リスト！
    search_queries = [
        "UTAU キャラクター 流行り", "UTAU 新着音源 評価", "UTAU 技術部 考察",
        "バニラアイス 新作 期間限定", "イチゴアイス コンビニ トレンド",
        "SNS 流行り 言葉 現在", "ネット 話題 バズり"
    ]
    
    all_text = ""
    # 2つくらいワードを選んで、材料を混ぜる！
    for query in random.sample(search_queries, 2):
        try:
            res = service.cse().list(q=query, cx=cx, num=5).execute()
            if 'items' in res:
                for item in res['items']:
                    # タイトルと説明文を材料にする
                    all_text += item['title'] + " " + item.get('snippet', '') + " "
        except Exception as e:
            print(f"検索ミスった……っ！: {e}")
            
    return all_text

def sine_wave_bot():
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    while True:
        # 1. 材料をエゴサしてくる
        material = get_ego_search_material()
        
        # 2. マルコフ連鎖で「正弦波くんの言葉」を作る
        generated = make_markov_text(material) if material else None
        
        if generated:
            post_text = f"{generated}……っ！"
        else:
            # 材料が足りなかった時の予備（これならバグっぽくない！）
            post_text = "波が混ざりすぎて、言葉が溶けちゃった……。バニラアイス食べよう"
        
        try:
            client.create_tweet(text=post_text)
            print(f"【成功】マルコフポスト: {post_text}")
        except Exception as e:
            print(f"【エラー】: {e}")

        # 1時間おき
        time.sleep(3600)

@app.route('/')
def home(): return "正弦波くん、UTAUとトレンドを収集中……っ！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
