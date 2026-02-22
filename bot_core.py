import os, random, threading, time, tweepy, re, requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_wiki_material():
    try:
        with open("Word.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        # 正弦波くんの名前やテトさんは抜いて、バックアップもクリーンに！
        return "楽曲制作 物理演算 エディタ ノート 歌声合成 エンジン wavファイル ツール"

def make_markov_text(source_text):
    # ★ここを修正！ ひらがな、カタカナ、漢字、英数字を1文字から全部拾うようにしたよ！
    # これで「を」や「が」も全部マルコフ連鎖の材料になる！！
    words = re.findall(r'[ぁ-ん]|[ァ-ヶー]|[一-龠]+|[a-zA-Z0-9]+', source_text)
    
    if len(words) < 10: return "波が静かだ"
    
    markov = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        if key not in markov: markov[key] = []
        markov[key].append(words[i+2])
    
    try:
        curr = random.choice(list(markov.keys()))
        res = list(curr)
        # 文の長さもイーロンに怒られない程度（15〜20語くらい）に調整
        for _ in range(18):
            if curr in markov:
                nxt = random.choice(markov[curr])
                res.append(nxt)
                curr = (res[-2], res[-1])
            else: break

def sine_wave_bot():
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    while True:
        material = get_wiki_material()
        txt = make_markov_text(material)
        post = txt if txt else "波が静かだ……っ！"
        
        try:
            client.create_tweet(text=post)
            print(f"成功: {post}")
        except Exception as e:
            print(f"失敗エラー内容: {e}")
            
        time.sleep(3600)

@app.route('/')
def home(): return "正弦波くん、日本語文法（カオス）モード……っ！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
