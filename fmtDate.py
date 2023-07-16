import datetime
import re
import csv

input_file = './kodekodemari.csv'
output_file = './kodekodemari2.csv'

with open(input_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

header = rows[0]
data_rows = rows[1:]

# 2列目の書き換え
for row in data_rows:
    print(row)
    status_id =  int(re.search(r'^https://twitter\.com/(.*)/status/(\d+)$', row[0]).group(2))
    unix_time = ((status_id >> 22) + 1288834974657) / 1000 - 16 * 60 * 60
    row[1] = datetime.datetime.fromtimestamp(unix_time).strftime('%Y%m%d%H%M%S')


# 書き換えた行を新しいCSVファイルに書き出す
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data_rows)
