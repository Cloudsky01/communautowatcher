import geocoder
from math import radians, sin, cos, sqrt, atan2

class User:
    def __init__(self):
        self.lat = None
        self.lng = None  

    def update_current_geolocation(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def get_current_geolocation(self):
        g = geocoder.ip('me')
        if g.ok:
            return g.latlng
        else:
            return None
        
    def calculate_distance(self, lat, lng):
        lat1 = radians(self.lat)
        lon1 = radians(self.lng)
        lat2 = radians(lat)
        lon2 = radians(lng)

        radius = 6371000  # approximate value

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = radius * c

        return distance
    
    def print_location(self):
        print("Current location: lat: {}, lng: {}".format(self.lat, self.lng))
