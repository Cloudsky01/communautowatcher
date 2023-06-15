import time
from logic import fetch_all_vehicles
from repeatTimer import RepeatTimer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.refresh_thread = None
        self.stop_flag = False

    def refresh(self, distance, latitude, longitude):
        self.model.all_vehicle_group = self.find_all_vehicles(latitude, longitude)
        self.model.vehicle_group_within_radius = self.find_vehicles_within_radius(distance)
        self.update_list()
        self.update_vehicle_count()
        self.update_time(time.strftime("%H:%M:%S", time.localtime()))

    def stop_search(self):
        self.stop_flag = True
        if self.refresh_thread:
            self.refresh_thread.stop()
            self.refresh_thread.join()
            self.refresh_thread = None

    def toggle_auto_refresh(self, interval, distance, latitude, longitude):
        if self.refresh_thread:
            self.refresh_thread.stop()
            self.refresh_thread = None
        else:
            self.stop_flag = False
            self.refresh_thread = RepeatTimer(interval, self.refresh, args=(distance, latitude, longitude))
            self.refresh_thread.start()

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
    
    def update_time(self, time):
        self.view.update_time(time)
    
    def update_list(self):
        vehicle_info_list = []
        for vehicle in self.model.vehicle_group_within_radius:
            vehicle_info = f"ID: {vehicle.vehicle_id}, Distance: {vehicle.distance}, Coordinates: ({vehicle.position.latitude}, {vehicle.position.longitude})"
            vehicle_info_list.append(vehicle_info)
        self.view.update_vehicle_list(vehicle_info_list)


    def update_vehicle_count(self):
        self.view.update_vehicle_count(self.vehicle_count)