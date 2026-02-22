import os, random, threading, time, tweepy, re
from flask import Flask
from ntscraper import Nitter

app = Flask(__name__)
scraper = Nitter()

def make_markov_text(source_text):
    # 日本語だけを抽出してバラバラにする
    words = re.findall(r'[ぁ-んァ-ヶー一-龠]+', source_text)
    if len(words) < 5: return None
    
    markov = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        if key not in markov: markov[key] = []
        markov[key].append(words[i+2])
    
    try:
        curr = random.choice(list(markov.keys()))
        res = list(curr)
        for _ in range(15):
            if curr in markov:
                nxt = random.choice(markov[curr])
                res.append(nxt)
                curr = (res[-2], res[-1])
            else: break
        return "".join(res)
    except: return None

def get_x_raw_material():
    # Googleを通さず、Xの検索結果から直接テキストをむしり取る！
    q = random.choice(["UTAU", "ボカロ トレンド", "バニラアイス"])
    try:
        # 検索して最新のポストを20件取得
        tweets = scraper.get_tweets(q, mode='term', number=20)
        text = " ".join([t['text'] for t in tweets['tweets']])
        return text
    except:
        return ""

def sine_wave_bot():
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    while True:
        # 即時投稿！
        material = get_x_raw_material()
        txt = make_markov_text(material)
        
        post = f"{txt}……っ！" if txt else "波が……うまく掴めないよ……。バニラアイス食べよ？"
        
        try:
            client.create_tweet(text=post)
            print(f"成功: {post}")
        except Exception as e:
            print(f"失敗: {e}")
            
        time.sleep(3600)

@app.route('/')
def home(): return "正弦波くん、X直結エゴサモード……っ！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
