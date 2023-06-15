import time
from logic import fetch_all_vehicles
from repeatTimer import RepeatTimer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.refresh_thread = None
        self.stop_flag = False

    def start_search(self, distance, latitude, longitude):
        self.model.find_all_vehicles(latitude, longitude)
        self.model.find_vehicles_within_radius(distance)
        self.model.update_list()
        self.model.update_vehicle_count()
        self.model.update_time(time.strftime("%H:%M:%S", time.localtime()))

    def refresh(self, distance, latitude, longitude):
        self.model.find_all_vehicles(latitude, longitude)
        self.model.find_vehicles_within_radius(distance)
        self.model.update_list()
        self.model.update_vehicle_count()
        self.model.update_time(time.strftime("%H:%M:%S", time.localtime()))

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