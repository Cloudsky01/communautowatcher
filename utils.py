import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

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