import webbrowser
import folium
import time

from logic import fetch_all_vehicles

class Model:
    def __init__(self):
        self.vehicle_group = None
        self.vehicle_count = 0
        self.time = None
        self.selected_vehicle = None
        self.view = None

    def update_time(self, time):
        self.view.update_time(time)

    def get_vehicle_details(self, vehicle_id):
        if self.vehicle_group:
            for vehicle in self.vehicle_group:
                if vehicle.vehicle_id == vehicle_id:
                    return vehicle.get_details()
        return ''

    def find_all_vehicles(self, lat, lng):
        self.vehicle_group = fetch_all_vehicles(lat, lng)
        self.vehicle_count = len(self.vehicle_group)
        return self.vehicle_group
    
    def find_vehicles_within_radius(self, distance):
        self.vehicle_group = self.vehicle_group.get_vehicle_within_radius(distance)
        return self.vehicle_group
    
    def update_list(self):
        vehicle_info_list = []
        for vehicle in self.vehicle_group:
            vehicle_info = f"ID: {vehicle.vehicle_id}, Distance: {vehicle.distance}, Coordinates: ({vehicle.position.latitude}, {vehicle.position.longitude})"
            vehicle_info_list.append(vehicle_info)
        self.view.update_vehicle_list(vehicle_info_list)


    def update_vehicle_count(self):
        self.view.update_vehicle_count(self.vehicle_count)


