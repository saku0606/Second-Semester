import random
import time

# Step1 スライムクラス
class Slime:
    # コンストラクタ
    # Step4 足跡とマークを作るときにもらうようにした
    def __init__(self, footprint, mark):
        # スライムの位置 さいしょは0
        self.__position = 0
        # Step4 スライムごとの足跡とマーク
        self.__footprint = footprint
        self.__mark = mark

    # 走るメソッド
    def run(self):
        # -1〜3のランダムな数を位置にたす
        self.__position += random.randint(-1, 3)
        # たしたあとの位置を出す
        # print(self.__position)  # Step1のときはこれだった

        # Step2 数字じゃなくて足跡とマークを出す
        # 足跡は位置の数だけならべる（マイナスのときは足跡なしになる）
        # Step4 "="と"○"じゃなくて自分の足跡とマークを使う
        # print(self.__footprint * self.__position + self.__mark)  # Option2の前はこれで1行まとめて出してた

        # Option2 足跡を1こずつ0.1秒(100ms)あけて出す
        # end=""で改行しないようにして、flush=Trueですぐ出す（先生の補足）
        for i in range(self.__position):
            print(self.__footprint, end="", flush=True)
            time.sleep(0.1)

        # さいごにマークを出して改行（マークのあとも0.1秒まつ）
        print(self.__mark, flush=True)
        time.sleep(0.1)

    # 位置のゲッター（デコレーターをつかう）
    @property
    def position(self):
        return self.__position

    # Step6 マークのゲッター（勝ったスライムのマークを出したいので作った）
    @property
    def mark(self):
        return self.__mark
