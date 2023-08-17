import requests
from bs4 import BeautifulSoup
import time
import random
import json
import sys

def get_max_page_number(soup: BeautifulSoup) -> int:
    """ページ数の最大値を取得する.

    Args:
      soup: BeautifulSoupオブジェクト。

    Returns:
      最大ページ数を整数値で返す。

    <div>タグ、<ul>タグ、<li>タグを検索し、<a>タグのテキスト内容を抽出する。
    抽出したテキスト内容を整数に変換し、最大値を取得して返す。
    """
    # <a>タグの内容を格納するための空のリストを初期化
    content_list = []

    # classが"body"の<div>タグをすべて検索し、ループ処理
    for div in soup.find_all("div", class_="body"):
        # 現在の<div>タグ内のclassが"page"の<ul>タグをすべて検索し、ループ処理
        for ul in div.find_all("ul", class_="page"):
            # 現在の<ul>タグ内の<li>タグをすべて検索し、ループ処理
            for li in ul.find_all("li"):
                # 現在の<li>タグ内の<a>タグをすべて検索し、ループ処理
                for a in li.find_all("a"):
                    # 現在の<a>タグのテキスト内容を取得
                    content = a.text
                    # 取得した内容をcontent_listに追加
                    content_list.append(content)

    # content_listから整数値のみを含む新しいリストを作成
    filtered_list = [int(x) for x in content_list if x.isdigit()]
    # filtered_listの最大値を取得
    max_value = max(filtered_list)
    # 最大値を返す
    return max_value


def get_XML_and_save(url, config):
    """指定したページからXML電文を取得し、ファイルとして保存する

    Args:
        page_num (int): 対象となるページ番号
        url (str): 対象となるページのURL
        config (dict): 設定を含む辞書

    Returns:
        int: 処理が正常終了した場合は0を返す
    """
    output_fpath = config["output_fpath"]
    random_time_min = config["_random_time_min"]
    random_time_max = config["_random_time_max"]
    volcano_eruption_id = config["volcano_eruption_id"]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    #ファイル数のカウントの初期化
    file_count = 0
    # XML電文へのリンクを取得
    links = []
    for tr in soup.find_all("tr", id=True):
        for a in tr.find_all("a", href=True):
            link = a["href"]
            if volcano_eruption_id in link:
                links.append(link)
    # XML電文へのリンクを変換
    print(f"XML電文のリンク数: {len(links)}")
    for link in links:
        link = "http://agora.ex.nii.ac.jp" + link
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # XML電文へのリンクを取得
        for div in soup.find_all("div", class_="body"):
            for p in div.find_all("p"):
                for a in p.find_all("a", href=True):
                    if volcano_eruption_id in a["href"]:
                        XML_link = "http://agora.ex.nii.ac.jp" + a["href"]
                        # XML電文を取得
                        response = requests.get(XML_link)
                        soup = BeautifulSoup(response.content, "html.parser")
                        pre_content = ""
                        # <pre>タグの内容を取得
                        for div in soup.find_all("div", class_="body"):
                            pre = div.find("pre")
                            if pre:
                                pre_content = pre.get_text()
                                # XMLファイルを保存
                                fpath = output_fpath + url.split("page=")[1] + "_" + a["href"].split("id=")[1] + ".xml"
                                with open(fpath, "w", encoding="utf-8") as xml_file:
                                    xml_file.write(pre_content)
                                print(f"{fpath}にファイルを保存しました.")
                                #ファイル数のカウント
                                file_count += 1
                                print(f"ファイル処理数: {file_count}")
                                #スクレイピングマナー
                                time.sleep(random.randint(random_time_min, random_time_max))
                            else:
                                print("<pre>タグのオブジェクトがNoneです.")
    return 0


def main():
    # JSONファイルを読み込む
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    #customかautoでモードを決定
    mode = config["mode"]
    url = config["url"]
    if mode == "custom":
        page_num = config["page_num"]
        new_url = url + str(page_num)
        get_XML_and_save(new_url, config)
    elif mode == "auto":
        init_page_num = config["init_page_num"]
        # 1ページ目にある時刻が書かれたリンクをすべて取得
        verify_url = url + str(init_page_num)
        response = requests.get(verify_url)
        soup = BeautifulSoup(response.content, "html.parser")
        # ページの最大値を取得
        max_page_num = get_max_page_number(soup)
        print(f"ページの最大数={max_page_num}")
        all_url = [url + str(num) for num in range(init_page_num, max_page_num + 1)]
        # 各ページのURLをループ処理
        start_count = config["start_count"]
        all_url = all_url[start_count-1:]
        for url in all_url:
            get_XML_and_save(url, config)
    else:
        print("Error:modeの文字列が異なります。customかautoのみです.")
        sys.exit()
    return 0


if __name__=="__main__":
    main()