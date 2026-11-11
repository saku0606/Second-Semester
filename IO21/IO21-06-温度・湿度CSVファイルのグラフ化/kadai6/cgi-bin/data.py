#!/usr/bin/python3
import os
import csv
import json
import datetime
from urllib.parse import parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, 'kadai5.csv')


def get_minutes():
    query = parse_qs(os.environ.get('QUERY_STRING', ''))
    try:
        return max(0, int(query.get('min', ['60'])[0]))
    except ValueError:
        return 60


def read_records():
    records = []
    with open(CSV_FILE, encoding='utf-8', newline='') as f:
        for row in csv.reader(f):
            try:
                t = datetime.datetime.strptime(row[0].strip(), '%Y-%m-%d %H:%M:%S')
                records.append((t, float(row[1]), float(row[2])))
            except (IndexError, ValueError):
                continue
    return records


result = {'total': 0, 'time': [], 'temp': [], 'humi': []}
try:
    records = read_records()
    result['total'] = len(records)

    minutes = get_minutes()
    if minutes > 0 and records:
        since = records[-1][0] - datetime.timedelta(minutes=minutes)
        records = [r for r in records if r[0] > since]

    result['time'] = [r[0].strftime('%Y-%m-%d %H:%M:%S') for r in records]
    result['temp'] = [r[1] for r in records]
    result['humi'] = [r[2] for r in records]
except FileNotFoundError:
    result['error'] = 'kadai5.csv が見つかりません'

print('Content-Type: application/json; charset=utf-8')
print('Cache-Control: no-store')
print()
print(json.dumps(result))
