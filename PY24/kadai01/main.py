import time
from slime import Slime

# ゴールの位置（定数）
GOAL = 10

# Step1 スライムを作るばしょ
# slime = Slime()

# Step5 スライムのデータ（足跡, マーク）
# ※このタプルはスライムを作るときだけ使う！あとのしょりでは使わない
# Step9 3匹目をふやした（この1行をたしただけで、ほかはなにも変えてない！）
slime_data = (
    ("=", "○"),
    ("~", "☆"),
    ("*", "◇"),
)

# Step3 2匹にしたのでリストで管理する
# slimes = [Slime(), Slime()]
slimes = []

# Step5 スライムを作ってリストに入れるばしょ（インスタンス化は1行だけ）
for footprint, mark in slime_data:
    slimes.append(Slime(footprint, mark))

# Step7 ① 出走者リストを出すばしょ
print("[List of runners]")
no = 1
for slime in slimes:
    print(f"No.{no}:{slime.mark}")
    no += 1

# Step7 ② Betするばしょ
# Step8 ちゃんとした番号が入るまで何回もきく
while True:
    print("[Bet]")
    bet_input = input("No:")

    # 数字じゃないのはダメ（isdecimalは全角の数字もTrueになる）
    if bet_input.isdecimal():
        # 全角の数字でもint()でふつうの数字にできた！
        bet_no = int(bet_input)

        # 出走してる番号だけOK（スライムの数で決めるので3匹になってもだいじょうぶ）
        if bet_no >= 1 and bet_no <= len(slimes):
            break

# Option1 レース前のカウントダウン（1秒ずつ）
print("[On your mark]")
for count in range(3, 0, -1):
    # flush=Trueがないと1秒ずつ出なくてまとめて出てきちゃった
    # （コンソールのバッファ機能のせいらしい。flush=Trueですぐ出るようになる）
    print(count, end=" ", flush=True)
    time.sleep(1)
print("Go!!")

# ゴールしたスライムを入れるリスト
winners = []

# Step3 さいしょの枠
print("-" * 25)

# だれかがゴールを超えるまでくりかえす
while len(winners) == 0:
    # 1ターンで1匹ずつ交互に走る
    for slime in slimes:
        slime.run()

    # 1ターンごとに枠を出す
    print("-" * 25)

    # ゴールを超えたスライムがいたらwinnersに入れる（同着もあり）
    for slime in slimes:
        if slime.position > GOAL:
            winners.append(slime)

# Step6 勝ったスライムを出すばしょ（同着のときは両方出る）
print("Winner!")
for slime in winners:
    print(slime.mark)

# Step7 ③ Betの勝ち負けを出すばしょ
# Betした番号のスライム（リストは0からなので-1する）
bet_slime = slimes[bet_no - 1]
print(f"You bet on {bet_slime.mark}")

if bet_slime in winners:
    print("You win!")
else:
    print("You lose..")
