import random
import threading
import time
from Passenger import Passenger
from Elevator import DirectionStatus, ElevatorThread


def elevator(elevator_id):
    passengers_inside = []
    passengers_waiting = []
    curr_floor = 1
    aim_floor = 1
    status = DirectionStatus.Idle
    while True:
        assert  curr_floor > 0
        assert  aim_floor > 0

        # elevator should not see the passenger, but the required floor
        request_lock.acquire()
        if status == DirectionStatus.Idle and request_queue: # idle elevator, get it move!
            floor = max(request_queue.keys(), key=lambda k: abs(k) - curr_floor)
            passengers_waiting = request_queue[floor]
            del request_queue[floor]
            aim_floor = abs(floor)

            status = DirectionStatus.Catch
        request_lock.release()

        passenger_lock.acquire()
        # delete request
        if status not in (DirectionStatus.Idle, DirectionStatus.Catch):
            request_lock.acquire()
            request_queue.pop(curr_floor * (1 if status == DirectionStatus.Up else -1), None)
            request_lock.release()

        # collect passenger current floor, pass by
        for _passenger in passengers[:]:
            if _passenger.from_floor == curr_floor and _passenger.status == status:
                passengers_inside.append(_passenger)
                passengers.remove(_passenger)

                if status == DirectionStatus.Up:
                    aim_floor = max(_passenger.to_floor, aim_floor)
                else:
                    aim_floor = min(_passenger.to_floor, aim_floor)

                print(f'elevator ({elevator_id}) take passenger ({_passenger.id}) at floor {curr_floor}')

        # catch all passenger
        if curr_floor == aim_floor and status == DirectionStatus.Catch:
            for _passenger in passengers_waiting[:]:
                if _passenger in passengers:
                    passengers.remove(_passenger)
                    passengers_waiting.remove(_passenger)
                    passengers_inside.append(_passenger)

                    # redirect the elevator base on direction of passenger
                    status = _passenger.status

                    if status == DirectionStatus.Up:
                        aim_floor = max(_passenger.to_floor, aim_floor)
                    else:
                        aim_floor = min(_passenger.to_floor, aim_floor)

                    print(f'elevator ({elevator_id}) take passenger ({_passenger.elevator_id}) at floor {curr_floor}')
        passenger_lock.release()

        # exit the passenger
        for _passenger in passengers_inside[:]:
            if _passenger.to_floor == curr_floor:
                passengers_inside.remove(_passenger)
                print(f'elevator ({elevator_id}) drop passenger ({_passenger.id}) at floor {curr_floor}')

        if status != DirectionStatus.Idle and curr_floor != aim_floor:
            print(f'elevator ({elevator_id}) with current floor {curr_floor} is going to floor {aim_floor}')
            time.sleep(3)
            curr_floor += 1 if aim_floor > curr_floor else -1
        elif curr_floor == aim_floor and not passengers_inside:
            status = DirectionStatus.Idle

# passenger queue
passengers = []

# lock
request_lock = threading.RLock()
passenger_lock = threading.RLock()
print_lock = threading.RLock()

# elevators
elevators = []

# required floor
request_queue = {}

# def __init__(self, x, y, request_queue, request_lock, passenger_list, passenger_lock, elevator_id):
for _ in range(2):
    thread = ElevatorThread(0,0, request_queue, request_lock, passengers, passenger_lock, _ + 1)
    thread.start()
    elevators.append(thread)

passenger_id = 1
while passenger_id < 4:
    # enhance passenger in random floor from 1 to 8
    from_floor = random.randint(1,9)
    to_floor = random.randint(1,9)
    if from_floor == to_floor:
        continue
    passenger = Passenger(passenger_id, _from_floor=from_floor, _to_floor=to_floor, x=0, y=0)
    passenger_id += 1

    with request_lock, passenger_lock:
        # add into passengers into require floor
        request_queue.setdefault(passenger.from_floor * (1 if passenger.status == DirectionStatus.Up else -1), []).append(passenger)

        # add to passengers queue
        passengers.append(passenger)

    # output
    print(f'passenger ({passenger.id}) waiting in floor {passenger.from_floor} want to floor {passenger.to_floor}')

    # sleep from 1 to 3 second
    time.sleep(random.randint(1,4))

for thread in elevators:
    thread.join()