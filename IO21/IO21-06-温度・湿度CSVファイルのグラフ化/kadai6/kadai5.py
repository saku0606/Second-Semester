#!/usr/bin/python3
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import csv

CSV_FILE = 'kadai5.csv'
INTERVAL = 60

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(pin=26)

try:
    next_time = time.time()
    while True:
        now = datetime.datetime.now()
        result = instance.read()
        if result.is_valid():
            row = [now.strftime('%Y-%m-%d %H:%M:%S'),
                   '%5.1f' % result.temperature,
                   '%5.1f' % result.humidity]

            with open(CSV_FILE, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, lineterminator='\r\n')
                writer.writerow(row)

            print(','.join(row))
        else:
            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' 計測エラー(CSVには保存しません)')

        next_time += INTERVAL
        wait = next_time - time.time()
        if wait > 0:
            time.sleep(wait)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
