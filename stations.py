class Stations:
    def __init__(self, stations):
        self.stations = stations
        self.position = stations['location']

    def get_stations(self):
        return self.stations
    
    def get_vehicles(self):
        return self.vehicles
    
    def get_sorted_vehicles(self):
        return self.sorted_vehicles
    
    def get_vehicles_by_type(self, vehicle_type):
        return self.vehicles_by_type