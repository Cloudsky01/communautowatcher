from vehicles import VehicleGroup
from utils import callAPI, write_to_file, read_file, openURL, Coordinates
import time
from vehicles import Vehicle, VehicleDetails
import psutil


def fetch_all_vehicles(lat, lng) -> VehicleGroup:
    vehicle_group = VehicleGroup([])
    response = callAPI("https://restapifrontoffice.reservauto.net/api/v2/Vehicle/FreeFloatingAvailability?CityId=59")
    for vehicle in response.json()['vehicles']:
        vehicle = Vehicle(vehicle['vehicleId'], Coordinates(vehicle['vehicleLocation']), VehicleDetails(vehicle))
        vehicle.calculate_distance(lat, lng)
        vehicle_group.add_vehicle(vehicle)
    return vehicle_group
