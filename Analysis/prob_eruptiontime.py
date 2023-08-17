import pandas as pd
from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
import json

def main():
    # JSONファイルを読み込む
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    df = pd.read_csv(config["input_fpath"])
    time_list = df["event_time_jst"].tolist()
    time_list_dt = [dt.strptime(time, '%Y-%m-%d %H:%M:%S') for time in time_list]


    init_time = dt.strptime(config["init_time"], '%Y-%m-%d %H:%M:%S')
    end_time = dt.strptime(config["end_time"], '%Y-%m-%d %H:%M:%S')

    delta_t_min = config["delta_t_min"]
    delta_t_max = config["delta_t_max"]
    delta_t_list = list(range(delta_t_min, delta_t_max+1)) #delta_t_minからdelta_t_maxまでの整数を含むリスト
    prob_list = [] #delta_tで火山噴火が発生する確率を保持するリスト
    percent_list = [] #確立をパーセントに変換した者を保持するリスト
    count_of_ones_list = [] #特定の時間間隔内で火山噴火が1回以上発生する場合の回数を保持するリスト
    for delta_t_num in delta_t_list:
        print(f"delta_t={delta_t_num}")
        delta_t = datetime.timedelta(minutes=delta_t_num)
        #delta_t_numの時間範囲にカウントされる個数の作成
        count_list = []
        #初期処理
        cal_time = init_time + delta_t
        count = 0
        for time in time_list_dt:
            if init_time <= time and time < cal_time:
                count = count + 1
            else:
                pass
        count_list.append(count)
        #whileループ
        while cal_time < end_time:
            cal_time_2 = cal_time + delta_t
            count = 0
            for time in time_list_dt:
                if cal_time <= time and time < cal_time_2:
                    count = count + 1
                else:
                    pass
            count_list.append(count)
            cal_time = cal_time_2

        #delta_t_numの範囲に現れる噴火の確率
        detect_list = [1 if num >= 1 else num for num in count_list]
        count_of_ones = detect_list.count(1)
        print(count_of_ones)
        length = len(detect_list)
        print(length)
        prob = round(count_of_ones / length, 4) #ある時間内の噴火の確率
        percent = round(prob * 100, 2)
        print(prob)
        print(f'{percent}%')
        count_of_ones_list.append(count_of_ones)
        prob_list.append(prob)
        percent_list.append(percent)

    #縦軸が確率、横軸がdelta_tのグラフ
    plt.plot(delta_t_list, percent_list)
    plt.xlabel("delta_t[min]")
    plt.ylabel("probability[%]")
    plt.savefig(config["output_image_fpath"])

    #csvデータの生成
    header = ["delta_t","count_of_ones","prob", "percent[%]"]
    save_list = [delta_t_list, count_of_ones_list, prob_list, percent_list]
    data_dict = {header[i]: save_list[i] for i in range(len(header))}
    df = pd.DataFrame(data_dict)
    df.to_csv(config["output_csv_fpath"], index=False)
    return 0

if __name__=="__main__":
    main()