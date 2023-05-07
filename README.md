# 問答 くん

開発中 ．．．

目的：問答アプリの作成

## テーブル一覧

### カテゴリテーブル（categories）

|No|列名|物理名|説明|
|:---:|:---|:---|:---|
|1|カテゴリID|id|PK|
|2|カテゴリ名|name||

* index(1)：カテゴリ名

### 問答テーブル（q_and_a）

|No|列名|物理名|説明|
|:---:|:---|:---|:---|
|1|カテゴリID|category_id||
|2|質問|question|トレーニングデータ全文|
|3|回答|answer|トレーニングデータ全文|
|4|候補検索キー|list_up_key|第一段の検索キー|
|5|質問形態素解析|morphological||
|6|備考|remarks||
|7|登録日時|rec_date_time||

* index(1)：候補検索キー
* index(2)：カテゴリID、候補検索キー

## 外部パッケージ
* mecab-python3(1.0.6)
* unidic-lite(1.0.8)
* psycopg2(2.9.6)

## TODO

* ~~トレーニング情報のDBへの登録~~（2023/05/05）
* ~~トレーニング情報の検索~~（2023/05/07）
* カテゴリを使って検索範囲を限定できるようにする（入力書式も検討する）
