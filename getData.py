"""
 Twitter API、archive.today、The Wayback Machineから情報を取得
"""
import tweepy
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import subprocess

# Twitter APIから情報を取得 ========
consumer_key = '●●●●'
consumer_secret = '●●●●'
access_token = '●●●●'
access_token_secret = '●●●●'

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth)

tw_id = 1297164649343811584
tweets = api.user_timeline(user_id=tw_id, count=1)
max_id = tweets[0].id
tw_data = []

# 過去の投稿を可能な範囲で取得
while 0 < len(tweets):
    tweets = api.user_timeline(user_id=tw_id, count=100, max_id=max_id)
    tw_data.extend(tweets)
    max_id = tw_data[-1].id - 1

# ファイルに書き込む
with open('./tw/tw_data.csv', mode='a', newline='') as csv_file:
    csv.writer(csv_file).writerow(tw_data)

# archive.todayから情報を取得 ========
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get('https://archive.is/https://twitter.com/kodekodemari/status/*')
cookie = {'name': 'cf_clearance', 'value': '●●●●'}
driver.add_cookie(cookie)

num = 0
while True:
    file_name = './at/at_data_' + str(num) + '.html'
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

# The Wayback Machineから情報を取得 ========
url = 'http://web.archive.org/cdx/search/cdx?url=https://twitter.com/kodekodemari/status/*&filter=mimetype:text/html&filter=statuscode:200'
result = subprocess.run(['curl', '-o', './twm/twm_data.txt', url])