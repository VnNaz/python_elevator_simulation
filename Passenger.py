from Elevator import DirectionStatus

class Passenger:
    def __init__(self, _id, _from_floor, _to_floor):
        self.id = _id
        self.from_floor = _from_floor
        self.to_floor = _to_floor
        self.status = DirectionStatus.Up if _to_floor > _from_floor else DirectionStatus.Down