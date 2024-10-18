import pygame

# provide sprite for visualizing elevator

elevator_sprite = pygame.image.load(".\\imgs\\elevator.png")
elevator_sprite = pygame.transform.scale(elevator_sprite, (60, 60))

floor_sprite = pygame.image.load(".\\imgs\\floor.png")
floor_right_sprite = pygame.transform.scale(floor_sprite, (200, 60))
floor_left_sprite = pygame.transform.flip(floor_right_sprite, True, False)

elevator_holder_sprite = pygame.image.load(".\\imgs\\elevator_holder.png")
elevator_holder_sprite = pygame.transform.scale(elevator_holder_sprite, (60, 60))

person_sprite = pygame.image.load(".\\imgs\\person.png")
person_sprite = pygame.transform.scale(person_sprite, (20, 40))

floor_width = elevator_holder_sprite.get_width() * 2 + floor_left_sprite.get_width() + floor_right_sprite.get_width()
floor_height = 60


def draw_floor(window, x = 0, y = 0):

    window.blit(floor_left_sprite, (x, y))

    window.blit(elevator_holder_sprite, (floor_left_sprite.get_width() + x , y))
    window.blit(elevator_holder_sprite, (floor_left_sprite.get_width()  + elevator_holder_sprite.get_width()+ x, y))

    window.blit(floor_right_sprite, (floor_left_sprite.get_width() + elevator_holder_sprite.get_width()*2 + x, y))