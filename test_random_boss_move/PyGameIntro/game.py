import pygame
import random

pygame.init()
screen = pygame.display.set_mode([800, 600])

done = False
game_finished = False
game_lose = False

# draw background
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# draw image
player_image = pygame.image.load("images/mario.png")
square_image = pygame.image.load("images/square.png")
box_image = pygame.image.load("images/box.png")
key_image = pygame.image.load("images/key.png")
win_image = pygame.image.load("images/win.png")
lose_image = pygame.image.load("images/lose.png")
boss_image = pygame.image.load("images/prison_left.png")

x = 100
y = 100

SQUARE_SIZE = 32


class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(self.x, self.y)

    def move(self, dx_random, dy_random):
        self.x += dx_random
        if dx_random == 0:
            self.y += dy_random

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def calc_next(self, dx, dy):
        return (self.x + dx), (self.y + dy)

    def match(self, x, y):
        return self.x == x and self.y == y


class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def calc_next_position(self, dx, dy):
        return self.x + dx, self.y + dy


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def calc_next_position(self, dx, dy):
        return self.x + dx, self.y + dy


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(1, 1)
        self.box = Box(6, 6)
        self.key = Key(11, 13)
        self.boss = Boss(10, 14)

    def move_player(self, dx, dy):
        [next_player_x, next_player_y] = self.player.calc_next_position(dx, dy)
        [next_box_x, next_box_y] = self.box.calc_next_position(dx, dy)
        if self.check_inside(next_player_x, next_player_y):
            if next_player_x == self.box.x and next_player_y == self.box.y:
                if self.check_inside(next_box_x, next_box_y):
                    pygame.mixer.music.load("sounds/move.wav")
                    pygame.mixer.music.play(0)
                    self.box.move(dx, dy)
                    self.player.move(dx, dy)
                    self.boss.move(dx_random, dy_random)
            else:
                pygame.mixer.music.load("sounds/move.wav")
                pygame.mixer.music.play(0)
                self.player.move(dx, dy)
                self.boss.move(dx_random, dy_random)

    def check_inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def check_win(self):
        if self.box.x == self.key.x and self.box.y == self.key.y:
            return True
        return False

    def check_lose(self):
        if [self.box.x, self.box.y] == [0, 0] or [self.box.x, self.box.y] == [0, self.width-1] or [self.box.x, self.box.y] == [self.height - 1, 0] or [self.box.x, self.box.y] == [self.width - 1, self.height -1]:
            return True
        return False

map = Map(25, 19)


while not done:

    key_arrow = None

    # Get events
    dx_random = random.randrange(-1, 2, 1)
    dy_random = random.randrange(-1, 2, 1)
    dx, dy = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1

    # Process game events

    if dx != 0 or dy != 0:
        map.move_player(dx, dy)
        if map.check_win():
            print("YOU WIN!")
            game_finished = True
        if map.check_lose():
            print("YOU LOSE!")
            game_lose = True

    # Repaint

    screen.fill(COLOR_WHITE)

    for x in range(map.width):
        for y in range(map.height):
            screen.blit(square_image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

    screen.blit(key_image, (map.key.x * SQUARE_SIZE, map.key.y * SQUARE_SIZE))

    screen.blit(box_image, (map.box.x * SQUARE_SIZE, map.box.y * SQUARE_SIZE))

    screen.blit(player_image, (map.player.x * SQUARE_SIZE, map.player.y * SQUARE_SIZE))

    screen.blit(boss_image, (map.boss.x * SQUARE_SIZE, map.boss.y * SQUARE_SIZE))

    if game_finished == True:
        screen.blit(win_image, (250, 200))
        # done = True
    if game_lose == True:
        screen.blit(lose_image, (250, 200))

    pygame.display.flip()