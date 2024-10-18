import threading
import pygame
from enum import Enum

class ElevatorThread(threading.Thread):

    def __init__(self, x, y, request_queue, request_lock, passenger_list, passenger_lock, id):
        threading.Thread.__init__(self)

        self.passengers_inside = []
        self.passengers_waiting = []

        self.current_floor = 1
        self.aim_floor = 1
        self.x = x
        self.y = y

        self.request_queue = request_queue
        self.request_lock = request_lock

        self.passenger_list = passenger_list
        self.passenger_lock = passenger_lock

        self.status = DirectionStatus.Idle

        self.elevator_id = id

        self.is_running = True

    def run(self):

        assert self.request_queue is not None
        assert self.passenger_lock is not None
        assert self.request_lock is not None

        while True:

            # assert self.current_floor > 0
            # assert self.aim_floor > 0

            # if elevator is idle and there is a request, get the elevator move
            self.take_require()

            # Main logic for elevator movement, servicing requests, and synchronization
            with self.passenger_lock:

                # if elevator is moving, it will catch up the passenger in same floor and same direction
                if self.status not in [DirectionStatus.Idle, DirectionStatus.Catch]:

                    with self.request_lock:
                        self.request_queue.pop(self.current_floor * (1 if self.status == DirectionStatus.Up else -1), None)

                # collect pass-by passengers
                for passenger in  self.passenger_list[:]:
                    if passenger.from_floor == self.current_floor and passenger.status == self.status:
                        pygame.time.wait(500)
                        self.passengers_inside.append(passenger)
                        self.passenger_list.remove(passenger)

                        # also change the aim floor if needed
                        if self.status == DirectionStatus.Up:
                            self.aim_floor = max(passenger.to_floor, self.aim_floor)
                        else:
                            self.aim_floor = min(passenger.to_floor, self.aim_floor)

                        print(f'elevator ({self.elevator_id}) take passenger ({passenger.id}) at floor {self.current_floor}')

                # if derived to request floor:
                if self.current_floor == self.aim_floor and self.status == DirectionStatus.Catch:
                    # add waiting passengers to elevator
                    for passenger in self.passengers_waiting[:]:
                        if passenger in self.passenger_list:
                            pygame.time.wait(500)
                            self.passenger_list.remove(passenger)
                            self.passengers_waiting.remove(passenger)
                            self.passengers_inside.append(passenger)

                            # redirect the elevator base on direction of the passenger
                            self.status = passenger.status

                            # also change the aim floor if needed
                            if self.status == DirectionStatus.Up:
                                self.aim_floor = max(passenger.to_floor, self.aim_floor)
                            else:
                                self.aim_floor = min(passenger.to_floor, self.aim_floor)

                            print(f'elevator ({self.elevator_id}) take passenger ({passenger.id}) at floor {self.current_floor}')

            # release passenger to destination
            for passenger in self.passengers_inside[:]:
                if passenger.to_floor == self.current_floor:
                    pygame.time.wait(500)
                    self.passengers_inside.remove(passenger)

                    print(f'elevator ({self.elevator_id}) drop passenger ({passenger.id}) at floor {self.current_floor}')

            self.move()

    def take_require(self):
        with self.request_lock:
            # if elevator is idle and there is a request, the get the elevator move
            if self.status == DirectionStatus.Idle and self.request_queue:
                # for optimization purpose get to the farthest floor
                farthest_floor = max(self.request_queue.keys(), key=lambda k: abs(k) - self.current_floor)

                # assign the passenger to the elevator
                self.passengers_waiting = self.request_queue[farthest_floor]

                del self.request_queue[farthest_floor] # remove the request

                self.aim_floor = abs(farthest_floor)

                # change status to catch
                self.status = DirectionStatus.Catch

    def move(self):
        if self.status != DirectionStatus.Idle and self.current_floor != self.aim_floor:

            print(f'elevator ({self.elevator_id}) with current floor {self.current_floor} is going to floor {self.aim_floor}')

            # go up or down
            if self.aim_floor > self.current_floor:
                for _ in range(10):
                    pygame.time.wait(200)
                    self.y -= 60/10
                self.current_floor += 1
            else:
                for _ in range(10):
                    pygame.time.wait(300)
                    self.y += 60 / 10
                self.current_floor -= 1

        elif self.current_floor == self.current_floor and not self.passengers_inside:
            self.status = DirectionStatus.Idle

class DirectionStatus(Enum):
    Down = -1
    Idle = 0
    Up = 1
    Catch = 2


