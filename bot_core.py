import requests
from bs4 import BeautifulSoup
import random
import re
import time
import tweepy
from datetime import datetime
import os
import sys

# --- ① X API設定（RenderのEnv Vars推奨） ---
API_KEY = os.environ.get("API_KEY", "YOUR_API_KEY")
API_SECRET = os.environ.get("API_SECRET", "YOUR_API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET", "YOUR_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN", "YOUR_BEARER_TOKEN")

def get_twitter_client():
    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

# --- ② 検索エサ場取得（Google検索風） ---
def fetch_search_seeds():
    queries = ["ニコニコ 話題", "ボカロ トレンド", "UTAU 新曲", "足立レイ 開発", "重音テト 最新"]
    headers = {"User-Agent": "Mozilla/5.0"}
    search_texts = ""
    
    for q in queries:
        try:
            # Google検索結果を簡易的にスクレイピング
            url = f"https://www.google.com/search?q={q}"
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 検索結果のスニペット（説明文）を抽出
            for g in soup.find_all('div'):
                t = g.get_text()
                if len(t) > 20: search_texts += " " + t
        except: continue
    return search_texts

# --- ③ 脳みそ構築ロジック ---
def build_pure_brain():
    # 既存のエサ場
    TARGET_URLS = [
        "https://dic.nicovideo.jp/a/utau", "https://dic.nicovideo.jp/a/重音テト",
        "https://dic.nicovideo.jp/a/足立レイ", "https://dic.nicovideo.jp/a/初音ミク",
        "https://dic.nicovideo.jp/a/voicevox", "https://dic.nicovideo.jp/a/ずんだもん"
    ]
    BAN_LIST = [
        "小山乃舞世", "声優", "CV", "演者", "担当", "絵師", "作者", "開発者", "出演", 
        "放送", "番組", "円", "エラー", "掲示板", "Google", "広告", "ログイン", "パスワード",
        "Amazon", "楽天", "価格", "セール", "在庫" # 検索結果に入りがちなゴミを追加
    ]
    
    combined_text = "の が を に だよ です だね なのだ よー！ だわ"
    
    # 大百科からの学習
    for url in TARGET_URLS:
        try:
            res = requests.get(url, timeout=5)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'html.parser')
            for l in soup.get_text().split('\n'):
                l = l.strip()
                if 10 < len(l) < 100 and not any(bad in l for bad in BAN_LIST):
                    clean_l = re.sub(r'[【】［］\[\]「」『』()（）]', '', l)
                    combined_text += " " + clean_l
        except: continue
    
    # ★最新検索結果からの学習を追加！
    print("Fetching search results for fresh news...", flush=True)
    combined_text += " " + fetch_search_seeds()
    
    # トークン化とマルコフ連鎖
    tokens = re.findall(r'[一-龠]+|[ぁ-ん]+|[ァ-ヶー]+|[a-zA-Z0-9]+', combined_text)
    chain = {}
    for i in range(len(tokens) - 2):
        key = (tokens[i], tokens[i+1])
        if key not in chain: chain[key] = []
        chain[key].append(tokens[i+2])
    return chain

def generate_tweet(brain):
    starts = ["僕は", "正弦波は", "テトさんは", "ミクさんは", "レイちゃんは", "0と1は"]
    w1 = random.choice(starts)
    candidates = [k[1] for k in brain.keys() if k[0] in [w1.replace("は",""), "は"]]
    w2 = random.choice(candidates) if candidates else "の"
    sentence = w1 + w2
    w1_curr, w2_curr = w1.replace("は",""), w2
    for i in range(25):
        if (w1_curr, w2_curr) in brain:
            w3 = random.choice(brain[(w1_curr, w2_curr)])
            sentence += w3
            w1_curr, w2_curr = w2_curr, w3
        else:
            new_key = random.choice(list(brain.keys()))
            sentence += new_key[0]
            w1_curr, w2_curr = new_key
        if i > 12 and any(end in sentence for end in ["！", "。"]): break
    return sentence[:140]

# --- ④ メインループ ---
# Renderはファイル永続化が難しいので、起動時に毎回脳を作る
print("Building brain with search integration...", flush=True)
brain = build_pure_brain()
client = get_twitter_client()

print("--- 正弦波くんOS：本番稼働開始 ---", flush=True)

while True:
    now = datetime.now()
    # 8時から23時（JSTを想定）
    if 8 <= now.hour <= 23:
        try:
            text = generate_tweet(brain)
            client.create_tweet(text=text)
            print(f"[{now.strftime('%H:%M')}] Posted: {text}", flush=True)
        except Exception as e:
            print(f"Error: {e}", flush=True)
        
        # 次の投稿まで1時間待機
        time.sleep(3600)
    else:
        # 夜間は10分ごとにチェック
        time.sleep(600)
