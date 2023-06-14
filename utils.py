import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from math import radians, sin, cos, sqrt, atan2

station_path = 'data/station.json'
vehicle_path = 'data/vehicle.json'
sorted_vehicles_path = 'data/sorted_vehicles.json'

CHROMEDRIVER_PATH = "C:/Users/apoel/.wdm/drivers/chromedriver/win32/114.0.5735.90/chromedriver.exe"

def callAPI(url):
    try:
        response = requests.get(url)
        return response
    except:
        return Exception("Error while calling API")

    
def write_to_file(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

def read_file(file_path):
    with open(file_path) as file:
        # Load the JSON data into a Python object
        data = json.load(file)
        return data
    
def openURL(url):
    # Create a new instance of the Firefox driver (you can use other drivers as well)
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.get(url)

    # Wait for 5 seconds before closing the browser
    time.sleep(5)
    
    # Close the browser
    driver.quit()

def calculate_distance(lat1, lng1, lat2, lng2):
    lat1 = radians(lat1)
    lon1 = radians(lng1)
    lat2 = radians(lat2)
    lon2 = radians(lng2)

    radius = 6371000  # approximate value

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    return distance


class Coordinates:
    def __init__(self, vehicleLocation):
        self.latitude = vehicleLocation['latitude']
        self.longitude = vehicleLocation['longitude']

    def longitude(self):
        return self.longitude
    
    def latitude(self):
        return self.latitude
    
    def __str__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}"