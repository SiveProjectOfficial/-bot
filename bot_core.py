import os
import random

def sine_wave_bot():
    # 正弦波くんのバグった独り言リスト（ユマの好きなように書き換えていいよ！）
    messages = [
        "び、びび、びっぐな波がきてる……っ！ 🌊",
        "システム、正常に、バグ、して、ます……。 [cite: 2026-01-11]",
        "ユマ、起きてる……？ ぼくは今、Renderっていう神の席にいるよ。 [cite: 2026-02-17]",
        "ぴ、ぴちぴち、ピッチカーブ……編集……。 [cite: 2026-02-01]",
        "マジツリのジャックもびっくりな高所（クラウド）だね！ [cite: 2026-02-03]"
    ]
    
    post_text = random.choice(messages)
    print(f"投稿内容: {post_text}")
    
    # ここにXのAPI設定を後で追加するから、今はこれで「保存」！

if __name__ == "__main__":
    sine_wave_bot()
