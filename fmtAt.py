"""
 archive.todayのデータを整形
"""
import glob
from bs4 import BeautifulSoup
import re
import datetime
import csv

# ファイルごとに処理
for file in glob.glob('./at/at_data_*.html'):
    # htmlを取得
    html = BeautifulSoup(open(file), 'html.parser')
    rows = html.find_all('div', {'id':re.compile(r'row\d+')})
    
    # 行ごとに処理
    for row in rows:
        # urlを取得
        url = row.find('a', {'style': 'display:block;margin-top:10px;color:#1D2D40;font-size:10px'}).get_text()
        match = re.search(r'^https://twitter\.com/(.*)/status/(\d+)$', url)
        # urlに一致しない場合スキップ
        if match == None:
            continue
        
        # created_datetimeを取得
        tmp_datetime = ((int(match.group(2)) >> 22) + 1288834974657) / 1000 - 16 * 60 * 60
        created_datetime = datetime.datetime.fromtimestamp(tmp_datetime).strftime('%Y%m%d%H%M%S')
        
        # snapshot_urlを取得
        snapshot = row.select_one('div.THUMBS-BLOCK div a')
        snapshot_url = snapshot.get('href')
        
        # snapshot_datetimeを取得
        tmp_datetime = datetime.datetime.strptime(snapshot.find('div').get_text(), '%d %b %Y %H:%M')
        snapshot_datetime = tmp_datetime.strftime('%Y%m%d%H%M%S')
        
        # textを取得
        text = snapshot.find('img').get('title')
        
        # csvに書き込む
        csv_data = [url, created_datetime, snapshot_url, snapshot_datetime, text]
        with open('./data/at_full.csv', mode='a', newline='') as csv_file:
            csv.writer(csv_file).writerow(csv_data)