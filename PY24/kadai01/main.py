import time
from slime import Slime

# Step5 スライムの初期データ（足跡, マーク）
# ※生成時のみ使用。以降の処理では使わない
# Step9 3匹目を追加（この1行の追加のみ。他は変更なし）
slime_data = ( # タプル
    ("=", "○"),
    ("~", "☆"),
    ("*", "◇"),
)

# Step3 スライムはリストで管理
slimes = []

# Step5 スライム生成→リストへ（インスタンス化は1行）
for footprint, mark in slime_data: # あんぱっく
    slimes.append(Slime(footprint, mark))

# Step7 ① 出走者リスト表示
print("[List of runners]")
no = 1
for slime in slimes:
    print(f"No.{no}:{slime.mark}")
    no += 1

# Step7 ② Bet入力
# Step8 入力チェック（正しい番号まで繰り返し）
while True: # ブーリアン
    print("[Bet]")
    bet_input = input("No:")

    # 数字チェック（isdecimalは全角の数字もTrue）
    if bet_input.isdecimal():
        # 全角の数字もint()で変換可
        bet_no = int(bet_input)

        # 出走中の番号のみOK（範囲はスライムの数から。3匹でも対応）
        if bet_no >= 1 and bet_no <= len(slimes):
            break

# Option1 レース前のカウントダウン（1秒間隔）
print("[On your mark]")
for count in [3, 2, 1]:
    # 先生の補足より：
    # sleepを掛けても処理が止まらない場合、以下の様に、
    # printにflush=True指定が必要となります。
    # 理由：コンソールにバッファ(一時的に出力を蓄えておく)機能があり、
    # その機能が生きているためです。
    # このflush=Trueを指定すると、
    # このバッファ機能をOFFし、直ぐに描画する様になります。
    print(count, end=" ", flush=True)
    time.sleep(1)
print("Go!!")

# ゴール判定用（誰かが10を超えたらTrue）
goal = False

# Step3 最初の枠
print("-" * 25)

# レース本体（誰かがゴールするまで）
while not goal:
    # 1ターン分（1匹ずつ交互に）
    for slime in slimes:
        slime.run()

    # Step3 1ターンごとの枠
    print("-" * 25)

    # 10超えのスライムがいたらゴール（同着あり）
    for slime in slimes:
        if slime.position > 10:
            goal = True

# Step6 勝者のマーク表示（10超えは全員表示→同着時も全員）
print("Winner!")
for slime in slimes:
    if slime.position > 10:
        print(slime.mark)

# Step7 ③ Betの勝敗表示
# Betした番号のスライム（リストは0始まりなので-1）
bet_slime = slimes[bet_no - 1]
print(f"You bet on {bet_slime.mark}")

# Betしたスライムが10超えなら勝ち
if bet_slime.position > 10:
    print("You win!")
else:
    print("You lose..")
