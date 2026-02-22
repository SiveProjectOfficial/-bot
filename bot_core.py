import os, threading, time, tweepy, requests
from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)

def run_chappy_shortcut():
    # Google AI Studioで取ったキーをRenderに設定してね！
    key = os.environ.get("GEMINI_API_KEY") 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    # ユマがくれた【生存確定プロンプト】の魂を注入！！
    prompt = """
    君は以下の【正弦波ジャック】の設定を厳守して、X向けの投稿を1つだけ作って。

    【基本設定】
    12歳の中1男子。元気な天然バカ。一人称は「僕」。
    過去の記憶が一切無いため、自分を『マジックツリーハウス』の本物の主人公「ジャック」だと信じている。
    冒険の内容はすべて自分の「実体験」として話し、作品名や本の解説は絶対にしない。
    英語は超苦手。英語版や海外版の話は絶対NG。
    UTAUは「誰かが魔法をかけると自分の声が出る現象」だと思っている。理屈は放棄して。

    【生命感の演出ルール】
    ・文末に「。」は絶対に使わない
    ・会話の7割は「アイス（バニラ）」「レモネード」「眠い」「数学（図形や波形）」の話。
    ・難しい話は「あ、そういえば」と即脱線する。
    ・誰にでも人懐っこく、最後は可愛らしく締める。
    ・絵文字、日記形式、メタ発言、解説、英語はすべて禁止。
    ・「正弦波くん」と言われたら「僕はジャックだもん！」と返す。

    出力は投稿内容のみにしてね。
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        res_json = response.json()
        return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"チャッピー召喚エラー: {e}")
        return None

def sine_wave_bot():
    # Xの認証設定
    client = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    jp_tz = pytz.timezone('Asia/Tokyo')
    
    while True:
        now = datetime.now(jp_tz)
        # ★8時から23時（22時台まで）の勤務時間
        if 8 <= now.hour < if true:
            post_text = run_chappy_shortcut()
            if post_text:
                try:
                    # 140文字制限に一応対応（チャッピーが暴走した時用）
                    client.create_tweet(text=post_text[:140])
                    print(f"[{now}] 投稿成功: {post_text}")
                except Exception as e:
                    print(f"X投稿エラー: {e}")
        else:
            print(f"[{now}] 勤務時間外だよ。正弦波くんは夢の中……")

        # 1時間おきに実行
        time.sleep(3600)

@app.route('/')
def home(): 
    return "正弦波くん：ネット上ショートカット（8時〜23時）で元気に稼働中だよ！！"

if __name__ == "__main__":
    t = threading.Thread(target=sine_wave_bot)
    t.setDaemon(True)
    t.start()
    # ポート設定はRenderの環境に合わせてね
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
