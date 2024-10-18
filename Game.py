from sprites import *
import threading

pygame.init()

window_width = 900
window_height = 600

window = pygame.display.set_mode((900, 600))

clock = pygame.time.Clock()

run = True

velocity = 2

x = (window_width / 2 - floor_width / 2) + 200
y = 120

def move():
    global x, y
    while True:
        pygame.time.wait(150)
        y += velocity

threading.Thread(target=move).start()
while run:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    for _ in range(5):
        draw_floor(window, window_width / 2 - floor_width / 2, 120 + (_ * 60))

    window.blit(elevator_sprite, (x,y))

    # Updating the display surface
    pygame.display.update()

    # Filling the window with black color
    window.fill((135, 206, 235))