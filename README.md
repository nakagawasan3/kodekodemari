# kodekodemari
## 概要
アーカイブから対象のTwitterアカウントのつぶやきを取得し分析します。
現在、対応しているサイトは以下の通りです。
[https://archive.org/](https://archive.org/)
[https://archive.md/](https://archive.md/)

## 使い方
*getData.py*でアーカイブが保存されているURLを取得します。
*fmtAt.py*と*fmtTwm.py*でアーカイブから取得した情報を整形し、*getDatatwm.py*で投稿の内容を取得します。
取得したデータはcsvファイルとして分割されているので*doData.py*で結合してください。
また、エラーが出た場合は取得済データと未取得データの差分を*diffData.py*で取って再度*getDatatwm.py*を実行してください。
分析は*Analysis.py*で行うことが出来ます。

## ディレクトリ/ファイルの内容
- Analysis.py
  - 投稿の内容を分析する
- diffData.py
  - 取得済データと未取得データの差分を取得しcsvファイルに書き出す
- doData.py
  - 取得済データのcsvファイルを結合する
- fmtAt.py
  - https://archive.md/からの情報を整形する
- fmtTwm.py
  - https://archive.org/からの情報を整形する
- getData.py
  - アーカイブが保存されているURL一覧を取得する
- getDatatwm.py
  - アーカイブが保存されているURLを元に投稿の内容を取得する

- アカウント名_combo.csv
  - よく一緒に使用される単語の組み合わせ一覧
- アカウント名_frequency.csv
  - よく使用される単語一覧(名詞、動詞、形容詞)
- アカウント名_log.csv
  - 投稿の内容・URL・時間、アーカイブURLの一覧
- アカウント名_postcount.csv
  - 投稿数を曜日と時間で分割した一覧
- アカウント名_tfidf.csv
  - 全ての文章の中で特徴的な単語一覧
- アカウント名_total.csv
  - 総使用日数・総投稿数・総文字数の一覧

- アカウント名_log.png
  - アカウント名_log.csvを画像化したファイル

- at
  - https://archive.md/から取得したファイルが入る
- data
  - 整形済みのファイルが入る
- shell
  - シェルスクリプトで描いたベータバージョン
- twm
  - https://archive.org/から取得したファイルが入る