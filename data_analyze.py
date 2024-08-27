import json
from collections import defaultdict
from datetime import datetime

def process_vehicle_data(file_path, start_time_str="17:00:00", end_time_str="17:30:00"):
    """
    處理車輛資料，根據指定的時間範圍篩選資料，並計算每個 VDID 下的 M 類型車輛總數以及 S 和 L 類型車輛總數。

    :param file_path: 資料檔案的路徑
    :param start_time_str: 時間範圍的開始時間，預設為 "17:00:00"
    :param end_time_str: 時間範圍的結束時間，預設為 "19:00:00"
    :return: 包含結果的 dict, 格式為 {VDID: [{'TotalM': int, 'TotalSL': int, 'timestamp': datatime}, ...], ...}
    """

    # 讀取資料檔案
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 建立存放資料的 queue
    queues = defaultdict(list)

    # 時間範圍設置
    start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
    end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

    # 遍歷每一筆資料
    for entry in data:
        vdid = entry['VDID']
        info_time_str = entry['InfoTime'].split('T')[1].split('+')[0]  # 提取 InfoTime 的時間部分
        info_time = datetime.strptime(info_time_str, "%H:%M:%S").time()
        
        # 只處理在 17:00 ~ 19:00 之間的紀錄
        if start_time <= info_time <= end_time:
            # 初始化統計結果
            lane_m_sum = 0
            lane_sl_sum = 0  # S 和 L 的總和

            # 遍歷每一個 LinkFlow
            for link_flow in entry['LinkFlows']:
                # 遍歷每一個 Lane
                for lane in link_flow['Lanes']:
                    if lane['LaneID'] in [0, 1, 2]:
                        # 加總 Type M 的資料
                        for vehicle in lane['Vehicles']:
                            if vehicle['VehicleType'] == 'M':
                                lane_m_sum += vehicle['Volume']
                            elif vehicle['VehicleType'] in ['S', 'L']:
                                lane_sl_sum += vehicle['Volume']  # S 和 L 的總和
                    elif lane['LaneID'] == 3:
                        # 如果需要處理 Lane3 的資料可以在這裡進行擴展
                        pass

            # 將結果加入 queue 中
            queues[vdid].append({
                'TotalM': lane_m_sum,
                'TotalSL': lane_sl_sum,
                'timestamp': info_time
            })

    return queues

