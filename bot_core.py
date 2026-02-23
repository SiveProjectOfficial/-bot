import requests
from bs4 import BeautifulSoup
import random
import re
import time
import json
import os
from datetime import datetime
import sys
import tweepy # ここでtweepyを使うよ

# --- ① X (Twitter) API設定 ---
# X Developer Portalで取得したキーをここに入れてね
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"
BEARER_TOKEN = "YOUR_BEARER_TOKEN"

# クライアント認証
def get_twitter_client():
    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

# --- ② エサ場 & 設定 ---
TARGET_URLS = [
    "https://dic.nicovideo.jp/a/utau",
    "https://dic.nicovideo.jp/a/重音テト",
    "https://dic.nicovideo.jp/a/足立レイ",
    "https://dic.nicovideo.jp/a/初音ミク",
    "https://dic.nicovideo.jp/a/voicevox",
    "https://dic.nicovideo.jp/a/ずんだもん"
]
SKELETON_WORDS = ["の", "が", "を", "に", "だよ", "です", "だね", "なのだ", "よー！", "だわ"]
CACHE_FILE = "brain_cache.json"

# --- ③ 脳みそ構築ロジック ---
def build_safe_pure_brain(urls, skeleton):
    BAN_LIST = [
        "ケツ", "オチンポ", "かゆい", "エロ", "スケベ", "絶望", "敗北", "死ん", "殺す",
        "小山乃舞世", "声優", "CV", "演者", "担当", "絵師", "イラストレーター", "作者", "開発者", 
        "出演", "ゲスト", "地上波", "放送", "番組", "スクラッチ", "景品", "販売", "購入", "円",
        "プレミアム会員", "エラー", "再試行", "スレッド", "レス", "努めてください", "ほんわか",
        "掲示板", "脚注", "関連項目", "編集", "作成", "ログイン", "パスワード", "ページ番号",
        "Google", "Chrome", "トヨタ", "ルイヴィトン", "日清", "案件", "広告", "宣伝", 
        "ショップ", "カフェ", "公式応援", "就任"
    ]
    combined_text = " ".join(skeleton)
    for url in urls:
        try:
            print(f"Feeding: {url.split('/')[-1]}...", flush=True)
            res = requests.get(url, timeout=5)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text()
            for l in text.split('\n'):
                l = l.strip()
                if 10 < len(l) < 100 and not any(bad in l for bad in BAN_LIST):
                    clean_l = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', l)
                    clean_l = re.sub(r'[【】［］\[\]「」『』()（）]', '', clean_l)
                    combined_text += " " + clean_l
        except: continue
    tokens = re.findall(r'[一-龠]+|[ぁ-ん]+|[ァ-ヶー]+|[a-zA-Z0-9]+', combined_text)
    chain = {}
    for i in range(len(tokens) - 2):
        key = (tokens[i], tokens[i+1])
        if key not in chain: chain[key] = []
        chain[key].append(tokens[i+2])
    return chain

def get_brain():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {tuple(eval(k)): v for k, v in data.items()}
    else:
        new_brain = build_safe_pure_brain(TARGET_URLS, SKELETON_WORDS)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({str(list(k)): v for k, v in new_brain.items()}, f, ensure_ascii=False)
        return new_brain

def generate_safe_bug(brain):
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
        if i > 12 and any(end in sentence for end in ["だよ", "です", "だね", "なのだ", "！", "。"]):
            break
    return sentence[:140]

# --- ④ メイン実行ループ ---
brain = get_brain()
client = get_twitter_client()

print("\n--- 正弦波くんOS：X連携モード稼働 ---", flush=True)

while True:
    now = datetime.now()
    # 8時から23時までの間かチェック
    if 8 <= now.hour <= 23:
        try:
            tweet_text = generate_safe_bug(brain)
            client.create_tweet(text=tweet_text) # ここで投稿！
            print(f"[{now.strftime('%H:%M')}] 投稿成功: {tweet_text}", flush=True)
        except Exception as e:
            print(f"[{now.strftime('%H:%M')}] 投稿エラー: {e}", flush=True)
        
        # 1時間待機
        time.sleep(3600)
    else:
        print(f"[{now.strftime('%H:%M')}] スリープ中...", flush=True)
        time.sleep(600)
