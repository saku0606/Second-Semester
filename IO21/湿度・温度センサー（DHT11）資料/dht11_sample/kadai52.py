#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
課題5 : DHT11 で温度・湿度を1分ごとに計測し、kadai5.csv に追記保存する

  配線 : DATA -> GPIO26 (37番ピン) / VCC -> 5V / GND -> GND
  停止 : [CTRL]+[C]
"""
from pathlib import Path
import time

from RPi import GPIO
from dht11 import DHT11

# ---- 設定 -------------------------------------------------------------
DATA_PIN   = 26                                      # センサーのDATA線 (BCM番号)
PERIOD_SEC = 60                                      # 計測間隔 [秒]
CSV_PATH   = Path(__file__).with_name('kadai5.csv')  # このプログラムと同じフォルダに作る
CRLF       = '\r\n'                                  # 改行コード CR+LF (0x0d, 0x0a)


def now_text():
    """現在時刻を yyyy-mm-dd hh:mm:ss 形式の文字列で返す"""
    return time.strftime('%Y-%m-%d %H:%M:%S')


def append_csv(stamp, temp, humi):
    """時刻・温度・湿度の1行を CSV の末尾に追記し、書いた内容を返す"""
    # {:5.1f} は %5.1f と同じ書式 (全体5桁・小数点以下1桁 → 999.9)
    line = '{},{:5.1f},{:5.1f}'.format(stamp, temp, humi)

    # newline='' で Python 側の改行変換を止め、CR+LF を自分で書き込む
    with open(CSV_PATH, mode='a', encoding='utf-8', newline='') as fp:
        fp.write(line + CRLF)

    return line


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    sensor = DHT11(pin=DATA_PIN)

    saved = 0
    print('計測開始 : 保存先 {}'.format(CSV_PATH.name))
    print('停止するには [CTRL]+[C] を押してください')

    try:
        while True:
            start = time.monotonic()
            stamp = now_text()
            data = sensor.read()

            if data.is_valid():
                line = append_csv(stamp, data.temperature, data.humidity)
                saved += 1
                print('[{:4d}] {}'.format(saved, line))
            else:
                print('[----] {} 読み取り失敗のため保存しません'.format(stamp))

            # 計測にかかった時間を差し引き、1分間隔がずれないように待つ
            rest = PERIOD_SEC - (time.monotonic() - start)
            if rest > 0:
                time.sleep(rest)

    except KeyboardInterrupt:
        print()
        print('[CTRL]+[C] で停止しました (保存件数 : {} 件)'.format(saved))

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
