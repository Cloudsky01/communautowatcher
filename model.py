from api import fetch_all_stations_vehicles

class Model:
    def __init__(self):
        self.all_vehicle_group = None
        self.vehicle_group_within_radius = None
        self.vehicle_count = 0
        self.time = None
        self.selected_vehicle = None
        self.stations = None

    def refresh_stations(self):
        self.stations = fetch_all_stations_vehicles()['stations']
    
    def get_stations(self):
        return self.stations


