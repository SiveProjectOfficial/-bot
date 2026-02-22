import os, random, threading, time, tweepy, re, requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_wiki_material():
    # ★ここだけ書き換えたよ！Wikiに行かずに身内のファイルを読み取る
    try:
        with open("Word.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "UTAU 楽曲制作 重音テト 正弦波 歌声 バニラアイス"

def make_markov_text(source_text):
    words = re.findall(r'[ぁ-んァ-ヶー一-龠]+|[a-zA-Z]+', source_text)
    if len(words) < 10: return "波が静かだ"
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
    except: return "不思議な波"

def sine_wave_bot():
    # ★ユマの「4つの名前」を1ミリも違わずに使うよ！！
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    while True:
        material = get_wiki_material()
        txt = make_markov_text(material)
        post = txt if txt else "波が静かだ"
        
        try:
            client.create_tweet(text=post)
            print(f"成功: {post}")
        except Exception as e:
            print(f"失敗エラー内容: {e}")
            
        time.sleep(3600)

@app.route('/')
def home(): return "正弦波くん、名前も完璧モード……っ！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
