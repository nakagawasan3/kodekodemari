"""
 その他
 ・csvファイルを結合
 ・csvファイルを画像に変換
"""
import pandas
import glob
import matplotlib.pyplot as plt
import japanize_matplotlib # グラフの日本語化

# csvファイルを結合 ========
full_data = pandas.DataFrame()

# ファイルを読み込んで結合
for file in glob.glob('./data/*.csv'):
    data = pandas.read_csv(file, header=None)
    full_data = pandas.concat([full_data, data])

# 重複する行の削除
full_data = full_data.drop_duplicates(subset=[0])

# csvに書き込む
full_data.columns = ['url', 'created_datetime', 'snapshot_url', 'snapshot_datetime', 'text']
full_data.to_csv('kodekodemari_log.csv', index=False)

# csvファイルを画像に変換 ========
data = pandas.read_csv('kodekodemari_log.csv', header=None)
data = data.sort_values(by=[data.columns[1]], ascending=True)
if len(data) > 2**10:
    data = data.head(1200)
width = 2600
height = 24 * len(data)
dpi = 100

# 描写域作成
fig = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
ax = fig.add_subplot()
ax.set_axis_off()
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

# テーブル整形
table = ax.table(cellText=data.values, cellLoc='left', loc='upper center', colWidths=[0.12, 0.04, 0.20, 0.04, 0.60])
table.auto_set_font_size(False)
table.set_fontsize(6)
table.scale(1, 1.4)

# 文字列のセルの余白を削除
for key,cell in table.get_celld().items():
  if key[1] in [0, 2, 4]:
    cell.PAD = 0.01

# 画像を保存
plt.savefig('kodekodemari_log.png', format='png', dpi=dpi)
