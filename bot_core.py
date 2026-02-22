import os, random, threading, time, tweepy, re, requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_wiki_material():
    # UTAUのWikiから言葉をさらってくるよ！
    urls = [
        "https://w.atwiki.jp/utau2008/", 
        "https://w.atwiki.jp/utau2008/pages/15.html" # 初心者向けページとか
    ]
    try:
        url = random.choice(urls)
        res = requests.get(url, timeout=10)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'html.parser')
        # Wikiの本文っぽいところからテキストを抽出
        return soup.get_text()
    except:
        # 万が一Wikiが見れない時のための予備の波
        return "UTAU 楽曲制作 重音テト 正弦波 歌声 バニラアイス 新作 トレンド"

def make_markov_text(source_text):
    # Wikiから拾った言葉をバラバラにする
    words = re.findall(r'[ぁ-んァ-ヶー一-龠]+|[a-zA-Z]+', source_text)
    if len(words) < 10: 
        words = re.findall(r'[ぁ-んァ-ヶー一-龠]+|[a-zA-Z]+', "UTAU 楽曲制作 重音テト 正弦波 バニラアイス")

    markov = {}
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        if key not in markov: markov[key] = []
        markov[key].append(words[i+2])
    
    try:
        curr = random.choice(list(markov.keys()))
        res = list(curr)
        for _ in range(15): # 少し長めに喋るようにしたよ
            if curr in markov:
                nxt = random.choice(markov[curr])
                res.append(nxt)
                curr = (res[-2], res[-1])
            else: break
        return "".join(res)
    except:
        return "波の音が聞こえる"

def sine_wave_bot():
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    while True:
        # Wikiから材料をゲットして、マルコフで混ぜる
        material = get_wiki_material()
        txt = make_markov_text(material)
        
        # 語尾の「……っ！」を削除！
        post = txt if txt else "波が静かだ……"
        
        try:
            client.create_tweet(text=post)
            print(f"成功: {post}")
        except Exception as e:
            print(f"失敗: {e}")
            
        time.sleep(3600)

@app.route('/')
def home(): return "正弦波くん、Wiki泥棒モード起動中……っ！" # ここは管理用だから残しとくねｗ

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
