import pygame
from typing import Final
from numpy import sign

pygame.font.init()

# Constants
FPS: Final[int] = 45
WIDTH: Final[int] = 960
HEIGHT: Final[int] = 640
GRAVITY: Final[pygame.Vector2] = pygame.Vector2(0, 1)
FONT: Final = pygame.font.Font(None, 100)

LEVEL: Final[list] = [
    "nuuuuuuuuuuuuuuuuuuuuuuuuuuuun",
    "k............................s",
    "k............................s",
    "k............................s",
    "k............................s",
    "k.......lr..................js",
    "k............lr...lyywwwyyyyyn",
    "k..................suuuuunnnnn",
    "k...lyr.................snnnnn",
    "k.......................snnnnn",
    "k.......................snnnnn",
    "nyyyyyyyywwwyr..........snnnnn",
    "nnnnnnnnnnnnnnyyr.......snnnnn",
    "nuuuuuuuuuuuuuuuur......snnnnn",
    "k.....................lynnnnnn",
    "k....................lnnnnnnnn",
    "k...................lnnnnnnnnn",
    "k..................lnnnnnnnnnn",
    "k.................lnnnnnnnnnnn",
    "nyyyyyyyyyyyyyyyyynnnnnnnnnnnn",
]


class Player(pygame.sprite.Sprite):
    velocity = pygame.Vector2(0, 0)

    def __init__(self, platforms_x, platforms) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("character.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 140
        self.rect.centery = 560
        self.platforms_y = platforms
        self.platforms_x = platforms_x
        self.__isOnFloor = pygame.sprite.spritecollide(self, self.platforms_y, False)
    
    def restart(self) -> None:
        self.rect.centerx = 140
        self.rect.centery = 560

    def __move(self) -> None:
        self.rect.y += self.velocity.y
        if pygame.sprite.spritecollideany(self, self.platforms_y):
            self.rect.y -= self.velocity.y
            while not pygame.sprite.spritecollideany(self, self.platforms_y):
                self.rect.y += sign(self.velocity.y)
            self.rect.y -= sign(self.velocity.y)
            self.velocity.y = 0
            self.__isOnFloor = True

        self.rect.x += self.velocity.x
        if pygame.sprite.spritecollideany(self, self.platforms_x):
            self.rect.x -= self.velocity.x
            while not pygame.sprite.spritecollideany(self, self.platforms_x):
                self.rect.x += sign(self.velocity.x)
            self.rect.x -= sign(self.velocity.x)

    def jump(self) -> None:
        if self.__isOnFloor:
            self.velocity.y = -16

    def update(self):
        self.velocity += GRAVITY
        self.__isOnFloor = pygame.sprite.spritecollideany(self, self.platforms_y)
        self.__move()
        if self.rect.bottom < 0 or self.rect.bottom > 640 or self.rect.right < 0 or self.rect.left > 960:
            self.rect.centerx = 100
            self.rect.centery = HEIGHT / 2


class StaticPLatformBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, c) -> None:
        pygame.sprite.Sprite.__init__(self)
        match c:
            case 'y'|'l'|'r':
                self.image = self.image = pygame.image.load("block_p.png")
            case 'k':
                self.image = pygame.image.load("block_w.png")
            case 's':
                self.image = pygame.transform.flip(pygame.image.load("block_w.png"), True, False)
            case 'u':
                self.image = pygame.transform.rotate(pygame.image.load("block_w.png"), -90)
            case 'n':
                self.image = pygame.image.load("block_n.png")
            case 'w':
                self.image = pygame.image.load("water.png")
            case _:
                self.image = pygame.Surface((32, 32))
                self.image.fill((0, 255, 0))
                self.image.set_alpha(40)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class xCollider(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("finalNight.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


pygame.init()
pygame.mixer.init()
JUMPSOUND: Final = pygame.mixer.Sound("jump.wav")
WINSOUND: Final = pygame.mixer.Sound("win.wav")
DEFEATSOUND: Final = pygame.mixer.Sound("defeat.wav")
pygame.display.set_icon(pygame.image.load("icon.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hadamar's cube")
screen.fill((0, 0, 0))
bg = Background()
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()
platforms_x = pygame.sprite.Group()
platforms_y = pygame.sprite.Group()
death_blocks = pygame.sprite.Group()
win_blocks = pygame.sprite.Group()

x = y = 0
for row in LEVEL:
    for col in row:
        if col != '.':
            platform = StaticPLatformBlock(x, y, col)
            if col == 'k' or col == 's':
                platforms_x.add(platform)
                sprites.add(platform)
            elif col == 'y' or col == 'u':
                platforms_y.add(platform)
                sprites.add(platform)
            elif col == 'l':
                temp = xCollider(x, y+1)
                platforms_x.add(temp)
                platforms_y.add(platform)
                sprites.add(platform)
            elif col == 'r':
                temp = xCollider(x+31, y+1)
                platforms_x.add(temp)
                platforms_y.add(platform)
                sprites.add(platform)
            elif col == 'w':
                death_blocks.add(platform)
                sprites.add(platform)
            elif col == 'j':
                win_blocks.add(platform)
                sprites.add(platform)
            else:
                sprites.add(platform)

                
        x += 32
    y += 32
    x = 0
del platform
del x
del y
player = Player(platforms_x, platforms_y)
sprites.add(player)


def win():
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_ESCAPE:
                    run = False
                    


run: bool = True

while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                JUMPSOUND.play(0)
                player.jump()
            if event.key == pygame.K_a:
                player.velocity.x -= 4
            if event.key == pygame.K_d:
                player.velocity.x += 4
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.velocity.x += 4
            if event.key == pygame.K_d:
                player.velocity.x -= 4
        
        
    screen.blit(bg.image, bg.rect)
    player.update()
    sprites.draw(screen)
    if pygame.sprite.spritecollideany(player, death_blocks):
        DEFEATSOUND.play(0)
        screen.fill((0, 0, 0))
        temp = FONT.render("Defeat", False, (255, 0, 0))
        temprect = temp.get_rect()
        temprect.centerx = WIDTH // 2
        temprect.centery = HEIGHT // 2
        screen.blit(temp, temprect)
        pygame.display.flip()
        pygame.time.wait(1000)
        player.restart()
    if pygame.sprite.spritecollideany(player, win_blocks):
        WINSOUND.play(0)
        screen.fill((0, 0, 0))
        temp = FONT.render("Win", False, (0, 255, 0))
        temprect = temp.get_rect()
        temprect.centerx = WIDTH // 2
        temprect.centery = HEIGHT // 2
        screen.blit(temp, temprect)
        pygame.display.flip()
        pygame.time.wait(1000)
        player.restart()
    
    pygame.display.flip()

pygame.quit()
