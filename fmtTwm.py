"""
 The Wayback Machineのデータを整形
 ※titte取得のため1ページごとGETをするので他のデータの整形が終わってから行う
"""
import pandas
import numpy

# ファイル読み取り
twm_data = pandas.read_csv('./twm/twm_data.txt', delimiter=' ', header=None)

# urlに一致しない行を削除
twm_data = twm_data[twm_data[2].str.match(r'^https://twitter\.com/(.*)/status/(\d+)$')]

# 重複する行の削除
twm_data = twm_data.drop_duplicates(subset=[2])

# archive.todayと重複する行の削除
at_data = pandas.read_csv('./data/at_full.csv')
indexes = twm_data[twm_data.iloc[:, 2].isin(at_data.iloc[:, 0])].index
twm_data = twm_data.drop(indexes)

# Twitterと重複する行の削除
tw_data = pandas.read_csv('./data/tw_full.csv')
indexes = twm_data[twm_data.iloc[:, 2].isin(tw_data.iloc[:, 0])].index
twm_data = twm_data.drop(indexes)

# 負荷分散のため1000行ごとに分割
for i, part in enumerate(numpy.array_split(twm_data, len(twm_data) // 1000 + 1)):
    part.iloc[:, [1, 2]].to_csv(f'./twm/twm_part_{i}.csv', index=False, header=False)