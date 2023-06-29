"""
 分析
 ・総日数、総文字数、総投稿数、投稿数/日、文字/投稿
 ・縦軸を時間、横軸を曜日とした投稿数の集計
 ・ネガポジ分析
 ・単語出現頻度(名詞、動詞、形容詞)
 ・共起キーワード
 ・特徴単語抽出(TF-IDF)
"""
import pandas
import MeCab
import ipadic
import numpy
from asari.api import Sonar
import collections
import pyfpgrowth
from sklearn.feature_extraction.text import TfidfVectorizer

name = 'kodekodemari'
full_data = pandas.read_csv(name + '_log.csv')
data = full_data

# 総日数を計算
data['created_datetime'] = pandas.to_datetime(
    data['created_datetime'], format='%Y%m%d%H%M%S')
diff_datetime = data['created_datetime'].max() - data['created_datetime'].min()
day_total = diff_datetime.days
total = [['総使用日数', day_total]]

# 総投稿数を計算
post_total = len(data)
total.append(['総投稿数', post_total])

# 総文字数を計算
char_total = data['text'].str.len().sum()
total.append(['総文字数', char_total])

# TODO:ZeroDivisionError: division by zeroの回避
total.append(['投稿数/一日', round((post_total / day_total), 2)])
total.append(['文字数/一日', round((char_total / day_total), 2)])
total.append(['文字数/一投稿', round((char_total / post_total), 2)])

# 週・時間でグループ化し集計
week = {'0': '日曜', '1': '月曜', '2': '火曜',
        '3': '水曜', '4': '木曜', '5': '金曜', '6': '土曜'}
data['week'] = data['created_datetime'].dt.strftime('%w')
data['hour'] = data['created_datetime'].dt.strftime('%H')

group = data.groupby(['week', 'hour']).size().reset_index(name='count')
group_data = group.pivot(index='hour', columns='week', values='count')
group_data = group_data.rename_axis(index='時間')
group_data = group_data.rename(columns=week)

print('make postcount')
pandas.DataFrame(group_data).to_csv(name + '_postcount.csv')

# 不要な文字を削除
excluded_strings = ['"', 'https', 'Twitter', 't', 'co']
data['fmt_text'] = data['text'].str.split(
    ': "').str[1].replace(excluded_strings, '', regex=True)

# 文章解析
sonar = Sonar()
sentiment = {'negative': 'ネガティブ', 'positive': 'ポジティブ'}
sentiment_total = {key: 0 for key in sentiment}
mecab = MeCab.Tagger(ipadic.MECAB_ARGS)
pos = {'noun': '名詞', 'verb': '動詞', 'adjective': '形容詞'}
pos_total = {key: [] for key in pos}
pos_list = []
excluded_words = ['*', 'する', 'こと', 'おる', 'れる', 'ある', 'いる', 'てる', 'なる', 'の', 'ん']

tfidf_text = []

# TODO:オブジェクト化
for fmt_text in data['fmt_text']:
    # 型がnanや値がNullの時スキップ
    if fmt_text is numpy.nan:
        continue

    # ネガポジ分析
    # TODO:asari.apiの速度が出ないので調査
    for key, value in sentiment.items():
        if sonar.ping(fmt_text)['top_class'] == key:
            sentiment_total[key] += 1

    # 品詞・原型の取得とデータの整形
    # 返却値の一番目が品詞なのでparseToNodeを使用
    node = mecab.parseToNode(fmt_text)
    tmp_arr = []

    # TODO:階層が深いのを修正
    while node:
        word = node.feature.split(',')
        for key, value in pos.items():
            if word[0] == value and len(word) >= 6:
                if word[6] not in excluded_words:
                    # 出現頻度のために[原型,原型,…]の形で挿入
                    pos_total[key].append(word[6])
                    # 共起・TF-IDFのために[[原型,原型,…],[原型,原型,…],…]の形で挿入
                    tmp_arr.append(word[6])
        node = node.next

    pos_list.append(tmp_arr)
    tfidf_text.append(fmt_text)

total.append(['ポジティブ投稿数', sentiment_total['positive']])
total.append(['ネガティブ投稿数', sentiment_total['negative']])

print('make total')
pandas.DataFrame(total).to_csv(name + '_total.csv', header=False, index=False)

# 単語出現頻度を集計
frequency = {}
for key, value in pos.items():
    frequency[value] = []
    frequency[value+'数'] = []
    count = dict(collections.Counter(pos_total[key]))
    for k, v in count.items():
        frequency[value].append(k)
        frequency[value+'数'].append(v)

# 列の長さを揃える
length = max(len(value) for value in frequency.values())
for key, value in frequency.items():
    diff = length - len(value)
    if diff > 0:
        frequency[key] += [float('nan')] * diff

print('make frequency')
pandas.DataFrame(frequency).to_csv(name + '_frequency.csv', index=False)

# 共起キーワードを分析
combo_data = []
# TODO:pyfpgrowthは対象行が多いと停止するので書き換える(20000行で共起回数30回以上ならOK)
for key, value in pyfpgrowth.find_frequent_patterns(pos_list, 30).items():
    if len(key) > 1:
        tmp = str(key).replace("'", "").replace("(", "").replace(")", "")
        combo_data.append([tmp, value])

print('make combo')
pandas.DataFrame(combo_data, columns=['組み合わせ', '共起回数']).to_csv(
    name + '_combo.csv', index=False)

# TF-IDFを計算
vectorizer = TfidfVectorizer()
sentence_list = [' '.join(cont) for cont in pos_list]
tfidf_data = []

tfidf_matrix = vectorizer.fit_transform(sentence_list).toarray()
feature_names = vectorizer.get_feature_names_out()

for i, sentence in enumerate(sentence_list):
    for j, feature in enumerate(feature_names):
        tfidf_value = tfidf_matrix[i, j]

        if tfidf_value > 0.0 and tfidf_value < 1.0:
            tfidf_data.append([feature, tfidf_value, tfidf_text[i]])

print('make tfidf')
pandas.DataFrame(tfidf_data, columns=['単語', '重要度', '該当文章']).to_csv(
    name + '_tfidf.csv', index=False)

# TODO:階層的クラスタリングの追加
