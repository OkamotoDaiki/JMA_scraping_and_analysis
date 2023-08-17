from bs4 import BeautifulSoup
import sys
import glob
import pandas as pd
from datetime import datetime
import json

def main():
    # JSONファイルを読み込む
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 出力ファイル名を指定
    output_file = config["output_fpath"]

    # 対象のXMLファイルを取得
    files = glob.glob("input_fpath")

    # 各リストを初期化
    kind_name_list = []
    area_name_list = []
    crater_name_list = []
    event_date_time_list = []
    event_date_time_utc_list = []
    lat_crater_coordinate_list = []
    long_crater_coordinate_list = []

    # 各XMLファイルに対して処理を行う
    for fpath in files:
        # XMLファイルを読み込む
        with open(fpath, "r", encoding="utf-8") as xml_file:
            xml_content = xml_file.read()

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(xml_content, "xml")

        try:
            # 各要素を抽出
            kind_name = soup.find("Kind").find("Name").text
            area_name = soup.find("Area").find("Name").text
            crater_name = soup.find("CraterName").text
            crater_coordinate = soup.find("CraterCoordinate").text
            event_date_time = soup.find("EventDateTime").text
            event_date_time_utc = soup.find("EventDateTimeUTC").text

            # 日時を変換
            event_date_time = datetime.fromisoformat(event_date_time).strftime("%Y-%m-%d %H:%M:%S")
            event_date_time_utc = datetime.fromisoformat(event_date_time_utc.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")

            latitude, longitude = crater_coordinate.split("+")[1], crater_coordinate.split("+")[2]

            # 噴火または爆発のデータのみをリストに追加
            if kind_name == "噴火" or kind_name == "爆発":
                kind_name_list.append(kind_name)
                area_name_list.append(area_name)
                crater_name_list.append(crater_name)
                event_date_time_list.append(event_date_time)
                event_date_time_utc_list.append(event_date_time_utc)
                lat_crater_coordinate_list.append(latitude)
                long_crater_coordinate_list.append(longitude)
                
        except AttributeError:
            pass

    # データをDataFrameに変換
    data = {
        "kind_name": kind_name_list,
        "area_name": area_name_list,
        "crater_name": crater_name_list,
        "event_time_jst": event_date_time_list,
        "event_time_utc": event_date_time_utc_list,
        "latitude": lat_crater_coordinate_list,
        "longitude": long_crater_coordinate_list
    }
    df = pd.DataFrame(data)

    # event_time_utc列をdatetime型に変換
    df['event_time_utc'] = pd.to_datetime(df['event_time_utc'])

    # event_time_utc列で昇順にソート
    df_sorted = df.sort_values('event_time_utc')

    # DataFrameをCSVファイルに書き込み
    df_sorted.to_csv(output_file, index=False)
    return 0

if __name__=="__main__":
    main()