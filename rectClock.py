from pygame import Rect
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600), 0, 32)
done = False
clock_image = pygame.image.load("images/clock.png")
blood_image = pygame.image.load("images/blood.png")
clock = pygame.time.Clock()
square_size = 40
BACKGROUND = (148, 198, 153)


class TimeModel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

clock_model = TimeModel(20, 50)
blood_model = TimeModel(300, 50)
timer_count = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    timer_count += 1
    if timer_count >= 10:
        timer_count = 0
        clock_model.x += 3

    screen.fill(BACKGROUND)
    screen.blit(clock_image, (clock_model.x, clock_model.y))
    screen.blit(blood_image, (blood_model.x, blood_model.y))
    clock.tick(20)
    pygame.display.flip()
