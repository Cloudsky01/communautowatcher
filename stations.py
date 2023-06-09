from dataclasses import dataclass

@dataclass
class coords:
    lat: float
    lng: float


class Stations:
    def __init__(self, vehicleID, stationID, coords: coords):
        self.vehicleID = vehicleID
        self.stationID = stationID
        self.coords = coords

    def getAvailability
