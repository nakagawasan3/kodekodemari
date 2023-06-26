"""
 Twitter APIのデータを整形
"""
import pandas
import datetime

tw_data = pandas.read_csv('./tw/tw_data.csv')
csv_data = []

for data in tw_data:
    # urlを取得
    url = 'https://twitter.com/' + data.user.screen_name + '/status/' + data.id_str

    # created_datetimeを取得
    tmp_datetime = ((int(data.id_str) >> 22) + 1288834974657) / 1000 - 16 * 60 * 60
    created_datetime = datetime.datetime.fromtimestamp(tmp_datetime).strftime('%Y%m%d%H%M%S')

    # snapshot_url/snapshot_datetimeを空
    snapshot_url = ''
    snapshot_datetime = ''

    # textを取得
    text = data.text

    csv_data.append([url, created_datetime, snapshot_url, snapshot_datetime, text])

# csvに書き込む
pandas.DataFrame(csv_data).to_csv('./data/tw_full.csv', header=False, index=False)