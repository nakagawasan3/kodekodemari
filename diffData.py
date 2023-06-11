"""
 差分を取得しファイルを再分割
 ※getDatatwm.pyが失敗したときに使用する
"""
import glob
import re
import pandas
import numpy

# ファイルごとに処理
for file in glob.glob('./twm/twm_part_*.csv'):
    num = re.search(r'\d+', file).group()

    org_data = pandas.read_csv('./twm/twm_part_' + num + '.csv')
    ref_data = pandas.read_csv('./data/twm_full_' + num + '.csv')

    indexes = org_data[org_data.iloc[:, 1].isin(ref_data.iloc[:, 0])].index
    org_data = org_data.drop(indexes)

    org_data.to_csv('./twm/diff_data_a.csv', mode='a', header=False, index=False)

# 負荷分散のため500行ごとに分割
csv_data = pandas.read_csv('./twm/diff_data_a.csv')
for i, part in enumerate(numpy.array_split(csv_data, len(csv_data) // 500 + 1)):
    part.to_csv(f'./twm/diff_data_a_{i}.csv', index=False, header=False)