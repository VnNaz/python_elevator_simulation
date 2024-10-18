import threading
from enum import Enum

class Elevator:
    def __init__(self, _id, _floor):
        self.passenger = None
        self.id = _id
        self.floor = _floor
        self.status = DirectionStatus.Idle

    def add_passenger(self, passenger):
        self.passenger.append(passenger)
    def remove_floor(self, floor):
        self.passenger = filter(lambda psg: psg.foor != floor, self.passenger)

class DirectionStatus(Enum):
    Down = -1
    Idle = 0
    Up = 1
    Catch = 2


