import random

import pygame

from models.boss import Boss
from models.door_win import DoorWin
from models.player import Player
from models.ques import Ques
from models.wall import Wall


class Map:
    def __init__(self, map_input, ques_input):
        self.width = len(map_input)
        self.height = len(map_input[0]) - 1
        self.wall = []
        self.ques = []
        check_ques = [True] * len(ques_input)
        for y in range(self.height):
            for x in range(self.width):
                if map_input[y][x] == "P":
                    self.player = Player(x, y)
                elif map_input[y][x] == "B":
                    self.boss = Boss(x, y)
                elif map_input[y][x] == "D":
                    self.door_win = DoorWin(x, y)
                elif map_input[y][x] == "#":
                    self.wall.append(Wall(x, y))
                elif map_input[y][x] == "Q":
                    while True:
                        index_ques = random.randint(0, len(ques_input)-1)
                        if check_ques[index_ques]:
                            break
                    self.ques.append(Ques(x, y, ques_input[index_ques]))
                    check_ques[index_ques] = False

    def find_wall(self, x, y):
        for i in range(len(self.wall)):
            if self.wall[i].match(x, y):
                return i
        return None

    def find_ques(self, x, y):
        for i in range(len(self.ques)):
            if self.ques[i].match(x, y):
                return i
        return None

    def in_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.find_wall(x, y) == None

    def move_boss(self):
        while True:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            next_bx, next_by = self.boss.calc_next(dx, dy)
            if self.in_map(next_bx, next_by) and dx*dy == 0 and self.door_win.match(next_bx, next_by) == False:
                break
        self.boss.move(dx, dy)
        self.boss.dx = dx
        self.boss.dy = dy

    def move_player(self, dx, dy):
        next_px, next_py = self.player.calc_next(dx, dy)
        if self.in_map(next_px, next_py):
            self.move_boss()
            self.player.move(dx, dy)

    def check_win(self):
        return self.door_win.match(self.player.x, self.player.y)

    def process_input(self, request):
        dx, dy = 0, 0
        if request == pygame.K_UP:
            dy = -1
        elif request == pygame.K_DOWN:
            dy = +1
        elif request == pygame.K_LEFT:
            dx = -1
        elif request == pygame.K_RIGHT:
            dx = +1
        elif request == pygame.K_r:
            ret
        else:
            return
        self.move_player(dx, dy)
