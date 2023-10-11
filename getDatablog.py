"""
 blogなどから情報を取得
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import random
import subprocess
import glob
from bs4 import BeautifulSoup
import re
import datetime
import json
import pandas
import csv

# archive.todayから情報一覧を取得 ========
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get('https://archive.li/http://nomihs1.livedoor.blog/archives/*')
cookie = {'name': 'cf_clearance', 'value': '●●●●'}
driver.add_cookie(cookie)

num = 0
while True:
    file_name = './blog/at_list_' + str(num) + '.html'
    time.sleep(random.randint(1, 10))

    # ファイルに書き込む
    with open(file_name, 'w') as file:
        file.write(driver.page_source)

    # ページャーがあれば次のページをロード
    next = driver.find_elements(By.ID, 'next')
    if next != []:
        num += 1
        driver.find_element(By.ID, 'next').click()
    else:
        break

driver.quit()

# The Wayback Machineから情報一覧を取得 ========
url = 'http://web.archive.org/cdx/search/cdx?url=http://nomihs1.livedoor.blog/archives/*&filter=mimetype:text/html&filter=statuscode:200&output=json'
result = subprocess.run(['curl', '-o', './blog/twm_list.json', url])

# url, snapshot_url, snapshot_datetimeのリストを作成 ========
url_list = []

# archive.today
for file in glob.glob('./blog/at_list_*.html'):
    html = BeautifulSoup(open(file), 'html.parser')

    pattern = re.compile(r'row\d+')
    rows = html.find_all(attrs={'id': pattern})

    # blockごとに処理
    for row in rows:
        tmp = row.find('div', class_='TEXT-BLOCK')
        url = tmp.find_all('a')[1].get_text()
        tmp = row.find('div', class_='THUMBS-BLOCK')
        snapshot = tmp.select_one('div a')
        snapshot_url = snapshot['href']
        tmp_datetime = datetime.datetime.strptime(snapshot.get_text(), '%d %b %Y %H:%M')
        snapshot_datetime = tmp_datetime.strftime('%Y%m%d%H%M%S')

        url_list.append([url, snapshot_url, snapshot_datetime])

# The Wayback Machine
json_file = json.load(open('./blog/twm_list.json'))

for value in json_file:
    snapshot_datetime = value[1]
    url = value[2]
    snapshot_url = 'http://web.archive.org/web/' + snapshot_datetime + '/' + url

    url_list.append([url, snapshot_url, snapshot_datetime])

# urlが重複した時、一番目を残して削除
df = pandas.DataFrame(url_list, columns=['url', 'snapshot_url', 'snapshot_datetime'])
df.drop_duplicates(subset='url', keep='first', inplace=True)
df.to_csv('./blog/url_list.csv', header=False, index=False)

# snapshot_urlから情報を取得 ========
full_data = []
url_list_data = pandas.read_csv('./blog/url_list.csv')

for index, value in url_list_data.iterrows():
    url = value[0]
    snapshot_url = value[1]
    snapshot_datetime = value[2]
    # エラー検索用dump
    print(snapshot_url)

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(7)

    try:
        driver.get(snapshot_url)
        html = BeautifulSoup(driver.page_source, 'html.parser')

        # html解析
        # 詳細ページ以外の時エラー
        if html.find('div', {'id': 'comments-list'}) == None:
            print('no cont err')
            driver.quit()
            continue

        title = '"' + html.find('h2').get_text().strip() + '"'
        pattern = re.compile(r'ldblog_related_articles_*')

        tmp = html.find(attrs={'id': pattern})
        text = '"' + tmp.find_previous_sibling('div').get_text().strip() + '"'

        tmp_datetime = datetime.datetime.fromisoformat(html.find('abbr').get('title'))
        created_datetime = tmp_datetime.strftime('%Y%m%d%H%M%S')

        # エラー時修正しやすいよう1行ずつcsvに書き込む
        csv_data = [url, created_datetime, snapshot_url, snapshot_datetime, title, text]
        with open('ishimarushimon_livedoor.csv', mode='a', newline='') as csv_file:
            csv.writer(csv_file).writerow(csv_data)
    except WebDriverException as e:
        # urlが不正、時間がかかる時エラー
        print('ex err')
        driver.quit()
        continue

    driver.quit()