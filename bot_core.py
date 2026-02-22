import os, random, threading, time, tweepy, re
from flask import Flask

app = Flask(__name__)

# --- マルコフの材料（ネットから拾えない時のための強力なバックアップ） ---
# ここに「UTAU」や「バニラアイス」の言葉を詰め込んでおいたよ！
BASE_WORDS = "UTAU 流行り 楽曲制作 重音テト  バニラアイス 新作 トレンド 音源"

def make_markov_text():
    # 複雑な道具を使わず、この場で言葉を混ぜる！
    words = re.findall(r'[ぁ-んァ-ヶー一-龠]+|[a-zA-Z]+', BASE_WORDS)
    if len(words) < 5: return "波が静かだ……"
    
    markov = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        if key not in markov: markov[key] = []
        markov[key].append(words[i+2])
    
    try:
        curr = random.choice(list(markov.keys()))
        res = list(curr)
        for _ in range(8):
            if curr in markov:
                nxt = random.choice(markov[curr])
                res.append(nxt)
                curr = (res[-2], res[-1])
            else: break
        return "".join(res)
    except: return "不思議な波……"

def sine_wave_bot():
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    # 起動してすぐに1回目を投稿！
    while True:
        txt = make_markov_text()
        post = f"{txt}……っ！"
        try:
            client.create_tweet(text=post)
            print(f"成功: {post}")
        except Exception as e:
            print(f"失敗: {e}")
        
        time.sleep(3600) # そのあと1時間寝る

@app.route('/')
def home(): return "正弦波くん、安定起動モード……っ！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
