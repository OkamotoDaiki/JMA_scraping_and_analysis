# JMA_scraping_and_analysis
気象庁が提供しているXML形式の火山噴火データをスクレイピングし、解析する。
 
# DEMO

xml_scraper.pyを実行すると、次のようなcsvデータを取得できる。

kind_name,area_name,crater_name,event_time_jst,event_time_utc,latitude,longitude
爆発,桜島,昭和火口,2012-12-10 04:27:00,2012-12-09 19:27:00,3134.63,13039.53
爆発,桜島,昭和火口,2012-12-10 05:25:00,2012-12-09 20:25:00,3134.63,13039.53
爆発,桜島,昭和火口,2012-12-10 10:13:00,2012-12-10 01:13:00,3134.63,13039.53
爆発,桜島,昭和火口,2012-12-10 22:50:00,2012-12-10 13:50:00,3134.63,13039.53
噴火,桜島,昭和火口,2012-12-12 15:59:00,2012-12-12 06:59:00,3134.63,13039.53
...

またある時間内に火山噴火が発生する確率はAnalysisにあるスクリプトで実行できる。
例えば、1分間に火山噴火が発生する確率～60分間に火山噴火が発生する確率は次のようなグラフになる。
(ここにグラフ)

# Feature
現段階ではAnalysisでは次のようなことができる。
・ある時間内に火山噴火が発生する確率を計算する。

# Requirement
 
* python3 3.8.10
 
# Installation
 
このリポジトリをクローンすること。
 
# Usage
 
基本の手順は
webscraping -> xml_scraping -> Analysis

Webスクレイピングは次のコマンドで実行できる。
取得したXMLデータは eruption_XMLフォルダ に生成される。
 
```bash
cd ./webscraping
python3 eruption_scraping.py
```

eruption_XMLにあるローカルデータを./xml_scraping/inputに移す。
その後、次のコマンドでxmlをスクレイピングし、火山噴火データをまとめる。
結果はresultフォルダにある。

```bash
cd ../xml_scraping
python3 xml_scraoer.py
```

XMLスクレイピングで生成した火山噴火データを解析する。
ある時間内に火山噴火が起こる確率を算出したい場合、次のスクリプトを実行する。

```bash
cd ../Analysis
python3 prob_eruptiontime.py
```

# Note
 
Webスクレイピング自体アクセスの頻度が高いため、一度取得できたら用がない限り実行しないこと。
 
# Author
* Oka.D.
* okamotoschool2018@gmail.com