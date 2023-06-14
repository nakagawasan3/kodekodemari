"""
The Wayback Machineから詳細情報を取得
"""
import csv
import subprocess
from bs4 import BeautifulSoup
import datetime
import re
import time

filename = './twm/twm_part_0.csv'
csvname = './data/twm_full_' + re.search(r'\d+', filename).group() + '.csv'
sleeptime = 7

# ファイル読み取り
with open(filename) as file:
    for row in csv.reader(file):
        # エラー検索用dump
        print(row)

        snapshot_url = 'http://web.archive.org/web/' + row[0] + '/' + row[1]
        result = subprocess.run(['curl', '-X', 'GET', snapshot_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 接続失敗時にスキップ
        if result.returncode != 0:
            continue
        html = BeautifulSoup(result.stdout.decode(encoding='utf8',errors='ignore'), 'html.parser')
        
        # textを取得
        if html.find('title') == None:
            continue
        text = html.find('title').text.replace('\n', '')
        
        # created_datetimeを取得
        status_id =  int(re.search(r'\d+', row[1]).group())
        unix_time = ((status_id >> 22) + 1288834974657) / 1000 - 16 * 60 * 60
        created_datetime = datetime.datetime.fromtimestamp(unix_time).strftime('%Y%m%d%H%M%S')
        
        # csvに書き込む
        csv_data = [row[1], created_datetime, snapshot_url, row[0], text]
        with open(csvname, mode='a', newline='') as csv_file:
            csv.writer(csv_file).writerow(csv_data)
            time.sleep(sleeptime)
