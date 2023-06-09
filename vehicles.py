from utils import Coordinates, calculate_distance

class VehicleDetails:
    def __init__(self, vehicle_details):
        self.vehicleDetails = vehicle_details

    def format_details(self):
        result = ""
        for key, value in self.vehicleDetails.items():
            result += f"{key}: {value}" + "\n"
        return result
    
    def get_formatted_details(self):
        return self.format_details()
    

class Vehicle:
    def __init__(self, vehicle_id : int, position : Coordinates):
        self.vehicle_id = vehicle_id
        self.position = position
        self.distance = None

    def calculate_distance(self, lat, lng):
        self.distance = calculate_distance(self.position.latitude, self.position.longitude, lat, lng)
    
    def get_details(self):
        self.vehicleDetails = VehicleDetails(self.vehicle_id)
        return self.vehicleDetails.get_formatted_details()


class VehicleGroup:
    def __init__(self, vehicles : list):
        self.vehicles : list(Vehicle) = vehicles

    def sort_by_distance(self):
        self.vehicles.sort(key=lambda vehicle: vehicle.distance)

    def print(self):
        for vehicle in self.vehicles:
            print(vehicle)

    def add_vehicle(self, vehicle : Vehicle):
        self.vehicles.append(vehicle)

    def calculate_distances(self, coordinates: Coordinates):
        for vehicle in self.vehicles:
            vehicle.calculate_distance(coordinates.latitude, coordinates.longitude)

    def get_vehicle_within_radius(self, radius: int):
        result = VehicleGroup([])
        for vehicle in self.vehicles:
            if (vehicle.distance < int(radius)):
                result.add_vehicle(vehicle)
        return result

    def get_nearest_vehicle(self):
        if not self.vehicles:
            return None
        return min(self.vehicles, key=lambda vehicle: vehicle.distance)
    
    def __len__(self):
        return len(self.vehicles)
    
    def __iter__(self):
        return iter(self.vehicles)

    
