import traci
import random
import uuid

class TrafficFlowManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.queue_data = {}
        self.path_mapping = {}

    def set_queue_data(self, queue_data):
        self.queue_data = queue_data

    def set_path_mapping(self, path_mapping):
        self.path_mapping = path_mapping

    def start_simulation(self):
        sumoCmd = ["sumo", "-c", self.config_file]
        traci.start(sumoCmd)

    def close_simulation(self):
        traci.close()

    def run_simulation(self, total_steps=7200):
        step = 0
        while step < total_steps:
            traci.simulationStep()
            self._process_queue_data(step)
            step += 1

    def _process_queue_data(self, step):
        for VDID, records in self.queue_data.items():
            paths = self.path_mapping.get(VDID, [])
            for record in records:
                self._create_vehicles(step, paths, record)

                # 如果是 VI9S600 或 VIWRJ60，複製車流到 VI9S600E 或 VIWRJ60E
                if VDID in ["VI9S600", "VIWRJ60"]:
                    extended_paths = self.path_mapping.get(VDID + "E", [])
                    self._create_vehicles(step, extended_paths, record)

    def _create_vehicles(self, step, paths, record):
        total_m = record['TotalM']
        total_sl = record['TotalSL']

        for _ in range(total_m):
            random_id = str(uuid.uuid4())
            veh_id = f"moto_{random_id}"
            route_id = random.choice(paths)  # 直接從 paths 列表中選擇路徑
            print(f"Assigning motorcycle route: {route_id} to vehicle: {veh_id}")  # debug output
            traci.vehicle.add(vehID=veh_id, routeID=route_id, typeID="motorcycle")

        for _ in range(total_sl):
            random_id = str(uuid.uuid4())
            veh_id = f"car_{random_id}"
            route_id = random.choice(paths)  # 直接從 paths 列表中選擇路徑
            print(f"Assigning car route: {route_id} to vehicle: {veh_id}")  # debug output
            traci.vehicle.add(vehID=veh_id, routeID=route_id, typeID="PassengerCar")



