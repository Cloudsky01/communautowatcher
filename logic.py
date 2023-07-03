from vehicles import VehicleGroup
from utils import callAPI, write_to_file, Coordinates
import time
from vehicles import Vehicle, VehicleDetails
import psutil


def fetch_all_vehicles(lat, lng) -> VehicleGroup:
    vehicle_group = VehicleGroup([])
    response = callAPI("https://restapifrontoffice.reservauto.net/api/v2/Vehicle/FreeFloatingAvailability?CityId=59")
    log_info(response.json())
    for vehicle in response.json()['vehicles']:
        vehicle = Vehicle(vehicle['vehicleId'], Coordinates(vehicle['vehicleLocation']))
        vehicle.calculate_distance(lat, lng)
        vehicle_group.add_vehicle(vehicle)
    
    return vehicle_group

def fetch_vehicle_details(vehicle_id):
    response = callAPI(f"https://restapifrontoffice.reservauto.net/api/v2/Vehicle/{vehicle_id}/FreeFloating?BranchId=1")
    return VehicleDetails(response.json()).get_formatted_details()

def log_info(log):
    log_datetime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    write_to_file(f"./data/log_{log_datetime}.json", log)

