from vehicles import VehicleGroup
from user import User
from utils import callAPI, write_to_file, read_file, openURL, Coordinates
import time
from vehicles import Vehicle, VehicleDetails
import psutil


def fetch_all_vehicles(user: User) -> VehicleGroup:
    vehicle_group = VehicleGroup([])
    response = callAPI("https://restapifrontoffice.reservauto.net/api/v2/Vehicle/FreeFloatingAvailability?CityId=59")
    for vehicle in response.json()['vehicles']:
        vehicle = Vehicle(vehicle['vehicleId'], Coordinates(vehicle['vehicleLocation']), VehicleDetails(vehicle))
        vehicle.calculate_distances_from_user(user)
        vehicle_group.add_vehicle(vehicle)
    return vehicle_group

def update_vehicle_distance_from_user(user: User, vehicleGroup: VehicleGroup) -> VehicleGroup:
    vehicleGroup.calculate_distances_from_user(user)
    return vehicleGroup

def fetch_vehicle_distance_from_user(radius: int, user: User, vehicleGroup: VehicleGroup) -> VehicleGroup:
    vehicleGroup.calculate_distances_from_user(user)
    return vehicleGroup.get_vehicle_within_radius(radius, user)

def main():
    user = User()
    user.print_location()
    vehicles = fetch_all_vehicles(user)
    vehicles = fetch_vehicle_distance_from_user(1000, user, vehicles)

    print(f"Found {len(vehicles.vehicles)} vehicles")
    # Get the current process ID
    process_id = psutil.Process()

    # Get CPU usage percentage
    cpu_usage = process_id.cpu_percent()

    # Get memory usage in bytes
    memory_usage = process_id.memory_info().rss

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage} bytes")
    time.sleep(5)
