import random
import time

# Step1 スライムクラス
class Slime:
    # Step4 足跡・マークを受け取る
    def __init__(self, footprint, mark): # コンストラクタ
        # 位置（初期値0）
        self.__position = 0
        # Step4 スライムごとの足跡・マーク
        self.__footprint = footprint
        self.__mark = mark

    # 走るメソッド
    def run(self):
        # 位置に-1〜3の乱数を加算
        self.__position += random.randint(-1, 3)

        # Step2 足跡＋マークで表示
        # 足跡は位置の数だけ（マイナス時は足跡なしにする）
        # Option2 足跡を1個ずつ0.1秒（100ms）間隔で表示
        # end=""で改行なし。
        # コンソールにバッファ(一時的に出力を蓄えておく)機能があり、
        # その機能が生きているためです。
        # このflush=Trueを指定すると、
        # このバッファ機能をOFFし、直ぐに描画する様になります。
        for i in range(self.__position):
            print(self.__footprint, end="", flush=True)
            time.sleep(0.1)

        # 最後にマーク表示＋改行（マークの後も0.1秒待ち）
        print(self.__mark, flush=True)
        time.sleep(0.1)

    # 位置のゲッター（デコレーター使用）
    @property # プロパティー
    def position(self):
        return self.__position

    # Step6 マークのゲッター（勝ったやつののマーク表示用）
    @property
    def mark(self):
        return self.__mark
