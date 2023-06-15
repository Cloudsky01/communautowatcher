import webbrowser
import folium
import time

from logic import fetch_all_vehicles

class Model:
    def __init__(self):
        self.all_vehicle_group = None
        self.vehicle_group_within_radius = None
        self.vehicle_count = 0
        self.time = None
        self.selected_vehicle = None


