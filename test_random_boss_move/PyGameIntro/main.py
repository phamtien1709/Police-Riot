import pygame

pygame.init()
screen = pygame.display.set_mode([300, 300])

mario_sprites = [
    pygame.image.load("images/mario-4.png"),
    pygame.image.load("images/mario-3.png"),
    pygame.image.load("images/mario-2.png"),
    pygame.image.load("images/mario-1.png")
]
class MarioAnim:
    def __init__(self, sprites):
        self.sprites = sprites
        self.count = 0
        self.sprite_index = 0
        self.state = False

    def run(self, screen, x, y):
        if self.state:
            screen.blit(self.sprites[self.sprite_index], [x, y])

            self.count += 1
            if self.count >= 7:
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.count = 0
        else:
            screen.blit(self.sprites[0], (x, y))


done = False
WHITE = [255, 255, 255]
clock = pygame.time.Clock()

mario_anim = MarioAnim(mario_sprites)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mario_anim.state = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mario_anim.state = False



    screen.fill(WHITE)
    mario_anim.run(screen, 10, 20)


    clock.tick(60)
    pygame.display.flip()