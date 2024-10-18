import random
from Elevator import ElevatorThread, DirectionStatus
from Passenger import Passenger
from sprites import *
import threading

pygame.init()

window_width = 900
window_height = 600

window = pygame.display.set_mode((200*2 + 60*2, 60*5))

clock = pygame.time.Clock()

run = True

# passenger queue
passengers = []

# lock
request_lock = threading.RLock()
passenger_lock = threading.RLock()
print_lock = threading.RLock()

# required floor
request_queue = {}

p_id = 0

# thread that create passenger
def add_passenger():
    global p_id
    while True:

        pygame.time.wait(random.randint(5, 10)* 1000)

        from_floor = random.randint(1, 5)
        to_floor = random.randint(1, 5)

        while to_floor == from_floor:
            from_floor = random.randint(1, 5)
            to_floor = random.randint(1, 5)

        if from_floor > to_floor:
            x = random.randint(50,170)
        else:
            x = random.randint(350, 450)

        passenger = Passenger(p_id, _from_floor=from_floor, _to_floor=to_floor, x = x,  y = 10 + (5-from_floor)*60)
        p_id += 1

        with request_lock, passenger_lock:
            # add into passengers into require floor
            request_queue.setdefault(passenger.from_floor * (1 if passenger.status == DirectionStatus.Up else -1),
                                     []).append(passenger)

            # add to passengers queue
            passengers.append(passenger)

# 2 elevators thread
elevator_1 = ElevatorThread(200,4*60, request_queue, request_lock, passengers, passenger_lock, 1)
elevator_2 = ElevatorThread(260,4*60, request_queue, request_lock, passengers, passenger_lock, 2)

elevator_1.start()
elevator_2.start()

threading.Thread(target=add_passenger).start()

while run:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    # draw the building of 5 floors
    for _ in range(5):
        draw_floor(window, 0, (_ * 60))

    # draw the elevators
    window.blit(elevator_sprite, (elevator_1.x, elevator_1.y))
    window.blit(elevator_sprite, (elevator_2.x, elevator_2.y))

    # draw the passengers
    with passenger_lock:
        for person in passengers:
            window.blit(person_sprite, (person.x, person.y))

    # Updating the display surface
    pygame.display.update()

    # Filling the window with black color
    window.fill((135, 206, 235))

