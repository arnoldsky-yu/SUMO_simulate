from dynamic_traffic_flow import TrafficFlowManager
from data_analyze import process_vehicle_data

# 定義路徑對應
path_mapping = {
    "VI9S600": ["11", "12", "13", "14", "15"],  # C 路徑
    "VI9S600E": ["16", "17", "18", "19", "20"], # G 路徑

    "VIWRJ60": ["1", "2", "3", "4", "5"],       # B 路徑
    "VIWRJ60E": ["6", "7", "8", "9", "10"],     # E 路徑

    "VIWRJ00": ["21", "22", "23", "24", "25"],  # I 路徑
    "VI9R760": ["26", "27", "28", "29", "30"],  # K 路徑
}

def main():
    config_file = "taipei.sumocfg"
    traffic_manager = TrafficFlowManager(config_file)
    
    traffic_manager.set_queue_data(process_vehicle_data("filtered_data.json"))
    traffic_manager.set_path_mapping(path_mapping)
    
    traffic_manager.start_simulation()
    traffic_manager.run_simulation(total_steps=30000)
    traffic_manager.close_simulation()

if __name__ == "__main__":
    main()
