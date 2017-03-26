import random
from models.map import Map
from models.wall import Wall
from views.image_all import *

pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Prison Riot")
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

square_size = 40
clock = pygame.time.Clock()
player_image = player_right_image


class TimeModel:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def direct_move():
    if event.key == pygame.K_RIGHT:
        player_image = player_right_image
    elif event.key == pygame.K_DOWN:
        player_image = player_down_image
    elif event.key == pygame.K_LEFT:
        player_image = player_left_image
    elif event.key == pygame.K_UP:
        player_image = player_top_image
    else:
        player_image = player_right_image
    return player_image


def init_ques():
    myfile = open("ques.txt", "r")
    count_line = 0
    ques_input = []
    temp = {}
    ques_key = ["content", "a", "b", "c", "d", "answer"]
    while True:
        theline = myfile.readline()
        if len(theline) == 0:
            break
        temp[ques_key[count_line]] = theline[:len(theline)-1]
        if count_line == 5:
            ques_input.append(temp)
            temp = {}
        count_line = (count_line + 1) % 6
    myfile.close()
    return ques_input


def init_map(level):
    map_file = "map" + str(level) +'.txt'
    myfile = open(map_file, "r")
    map_input = []
    while True:
        theline = myfile.readline()
        if len(theline) == 0:
            break
        map_input.append(theline)
    myfile.close()
    return map_input


def min(a, b):
    if a > b:
        return b
    return a


def max(a, b):
    if a > b:
        return a
    return b


def print_game(map):
    for y in range(max(map.player.y-2, 0), min(map.player.y+3,map.height)):
        for x in range(max(map.player.x-2, 0), min(map.player.x+3,map.width)):
            screen.blit(plattform_image, (200 + (x * square_size), 100 + (y * square_size)))
            if map.player.match(x, y):
                screen.blit(player_image, (200 + (x * square_size), 100 + (y * square_size)))
            elif map.boss.match(x, y):
                screen.blit(boss_image, (200 + (x * square_size), 100 + (y*square_size)))
            elif map.door_win.match(x, y):
                screen.blit(door_win_image, (200 + (x * square_size), 100 + (y*square_size)))
            elif map.find_wall(x, y) != None:
                screen.blit(wall_image, (200 + (x * square_size), 100 + (y * square_size)))
            elif map.find_ques(x, y) != None:
                screen.blit(ques_image, (200 + (x * square_size), 100 + (y * square_size)))
    pygame.display.flip()


def revert_content(content):
    step = 0
    b = []
    for i in range(len(content)):
        step += 1
        if content[i] == " " and step >= 65:
            b.append(content[i+1-step:i])
            step = 0
    b.append(content[i+1-step:i+1])
    return b


def show_ques(ques):
    myfont = pygame.font.SysFont("Arial Rounded MT Bold", 20)
    myfont_answer = pygame.font.SysFont("Arial Rounded MT Bold", 30)
    temp_content = revert_content(ques.content)
    content = []
    for temp in temp_content:
        content.append(myfont.render(temp, 1, COLOR_WHITE))
    choice_a = myfont.render(ques.a, 1, COLOR_WHITE)
    choice_b = myfont.render(ques.b, 1, COLOR_WHITE)
    choice_c = myfont.render(ques.c, 1, COLOR_WHITE)
    choice_d = myfont.render(ques.d, 1, COLOR_WHITE)
    your_answer = myfont_answer.render("YOUR ANSWER", 1, COLOR_WHITE)
    you_sure = myfont.render("ARE YOU SURE? PRESS [Y] or [N]", 1, COLOR_WHITE)

    ques_index = random.randint(0, 2)
    def process_show_ques(ques_index):
        screen.blit(bg_ques_image[ques_index], (0, 100))
        for i in range(len(content)):
            screen.blit(content[i], (80, 215+i*25))
        screen.blit(choice_a, (90, 390))
        screen.blit(choice_b, (365, 390))
        screen.blit(choice_c, (90, 455))
        screen.blit(choice_d, (365, 455))
        screen.blit(your_answer, (40, 120))
    process_show_ques(ques_index)
    pygame.display.flip()

    answer = "..."
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    answer = "A"
                elif event.key == pygame.K_b:
                    answer = "B"
                elif event.key == pygame.K_c:
                    answer = "C"
                elif event.key == pygame.K_d:
                    answer = "D"
                elif event.key == pygame.K_n:
                    answer = "..."
                elif event.key == pygame.K_y:
                    done = True
                    break
                else:
                    continue
            process_show_ques(ques_index)
            answer_image = myfont_answer.render(answer, 1, COLOR_WHITE)
            screen.blit(answer_image, (205, 120))
            screen.blit(you_sure, (40, 150))
            pygame.display.flip()
    return ques.check_answer(answer)


def finish_ques(map, index_ques, result, request):
    if result:
        del map.ques[index_ques]
        done = False
        true_eff.play(0)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    done = True
            screen.blit(pass_target_image, (0, 100))
            pygame.display.flip()
    else:
        del map.ques[index_ques]
        map.wall.append(Wall(map.player.x, map.player.y))
        done = False
        false_eff.play(0)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    done = True
            screen.blit(fail_target_image, (0, 100))
            pygame.display.flip()

        dx, dy = 0, 0
        if request == pygame.K_UP:
            dy = -1
        elif request == pygame.K_DOWN:
            dy = +1
        elif request == pygame.K_LEFT:
            dx = -1
        elif request == pygame.K_RIGHT:
            dx = +1
        map.player.move(-dx, -dy)


def process_ques(map, request):
    index_ques = map.find_ques(map.player.x, map.player.y)
    if index_ques == None:
        return
    result = show_ques(map.ques[index_ques])
    finish_ques(map, index_ques, result, request)


def check_lost(map):
    global done, replay
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx*dy == 0:
                next_px, next_py = map.player.calc_next(dx, dy)
                if map.boss.match(next_px, next_py):
                    screen.fill(COLOR_BLACK)
                    lose_eff.play(0)
                    screen.blit(game_lost_image, (0, 100))
                    pygame.display.flip()
                    done = False
                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                done = True
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_y:
                                    replay = True
                                    return replay
                                elif event.key == pygame.K_n:
                                    done = True
                    return True
    return False


def check_won(map):
    global next_level, level_next
    if map.door_win.match(map.player.x, map.player.y):
        screen.fill(COLOR_WHITE)
        win_eff.play(0)
        screen.blit(game_win_image, (0, 100))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        next_level = True
                        if level_next < 2:
                            level_next += 1
                        return next_level, level_next
                    elif event.key == pygame.K_n:
                        done = True
        return True
    return False

done = False
global done
clock_model = TimeModel(50, 50)
blood_model = TimeModel(695, 50)
level_next = 0
ques_input = init_ques()
map_input = init_map(level_next)
map = Map(map_input, ques_input)
replay = False
back_menu = False
done = False
next_level = False
timer_count = 0
list_intro = [story_1_images, story_2_images, story_3_images, avatar_images, ruler_images]
sound = pygame.mixer.Sound("Sounds/sound.wav")
sound.play(-1)
true_eff = pygame.mixer.Sound("Sounds/True.wav")
false_eff = pygame.mixer.Sound("Sounds/False.wav")
win_eff = pygame.mixer.Sound("Sounds/win_level.wav")
lose_eff = pygame.mixer.Sound("Sounds/lose_level.wav")
index_game = 0
while index_game < 6:
    index_image = 0
    if index_game == 3:
        done = False
        while not done:
            screen.blit(list_intro[index_game][index_image], [0, 0])
            pygame.display.flip()
            clock.tick(2)
            index_image = (index_image + 1) % 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    done = True
    elif index_game == 4:
        done = False
        while not done:
            screen.fill(COLOR_BLACK)
            screen.blit(list_intro[index_game][index_image], [0, 100])
            pygame.display.flip()
            clock.tick(2)
            index_image = (index_image + 1) % 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    done = True
    elif index_game == 5:
        done = False
        while not done:
            screen.fill(COLOR_BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    player_image = direct_move()
                    map.process_input(event.key)
                    process_ques(map, event.key)
                    if check_won(map):
                        if level_next > 2:
                            next_level = False
                            done = False
                            while not done:
                                screen.blit(win_image, (0, 0))
                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        done = True
                                    elif event.type == pygame.KEYDOWN:
                                        done = True
                                        break
                            index_game = 2
                            map_input = init_map(0)
                            map = Map(map_input, ques_input)
                            done = True
                        if next_level:
                            map_input = init_map(level_next)
                            map = Map(map_input, ques_input)
                        else:
                            index_game = 2
                            map_input = init_map(0)
                            map = Map(map_input, ques_input)
                            done = True
                    if check_lost(map):
                        if replay:
                            map_input = init_map(level_next)
                            map = Map(map_input, ques_input)
                        else:
                            index_game = 2
                            map_input = init_map(0)
                            map = Map(map_input, ques_input)
                            done = True
            timer_count += 1
            if timer_count >= 10:
                timer_count = 0
                clock_model.x += 1
            if clock_model.x == blood_model.x:
                done = True
                break

            screen.blit(clock_image, (clock_model.x, clock_model.y))
            screen.blit(blood_image, (blood_model.x, blood_model.y))
            print_game(map)
            clock.tick(50)
            pygame.display.flip()
    else:
        done = False
        while not done:
            screen.blit(list_intro[index_game][index_image], (0, 50))
            pygame.display.flip()
            clock.tick(2)
            index_image = (index_image + 1) % 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    done = True
                    break
    index_game += 1
