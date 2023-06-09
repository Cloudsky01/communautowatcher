
from user import User
from utils import Coordinates

class VehicleDetails:
    def __init__(self, vehicleDetails):
        self.vehicleDetails = vehicleDetails
    
    def type(self):
        return self.vehicleDetails['vehicleTypeId']
    
    def propulsion_type(self):
        return self.vehicleDetails['propulsionTypeId']
    

class Vehicle:
    def __init__(self, vehicle_id : int, position : Coordinates, vehicleDetails : VehicleDetails):
        self.vehicle_id = vehicle_id
        self.position = position
        self.vehicleDetails = vehicleDetails
        self.distance = None

    def calculate_distances_from_user(self, user: User):
        self.distance = user.calculate_distance(self.position.latitude, self.position.longitude)


class VehicleGroup:
    def __init__(self, vehicles : list):
        self.vehicles : list(Vehicle) = vehicles

    def sort_by_distance(self, distance):
        self.vehicles.sort(key=lambda vehicle: vehicle.distance)

    def print(self):
        for vehicle in self.vehicles:
            print(vehicle)

    def add_vehicle(self, vehicle : Vehicle):
        self.vehicles.append(vehicle)

    def calculate_distances_from_user(self, user: User):
        for vehicle in self.vehicles:
            vehicle.calculate_distances_from_user(user)

    def get_vehicle_within_radius(self, radius: int, user: User):
        result = VehicleGroup([])
        for vehicle in self.vehicles:
            if (vehicle.distance < int(radius)):
                result.add_vehicle(vehicle)
        return result

    def get_nearest_vehicle(self):
        if not self.vehicles:
            return None
        return min(self.vehicles, key=lambda vehicle: vehicle.distance)

    
