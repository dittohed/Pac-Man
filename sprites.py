import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 255, 255))

        self.rect = self.image.get_rect() # player coordinate
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        # moving
        self.speed = 2 # 2 pixels per second
        self.vel_x, self.vel_y = 0, 0
        self.wanna_go = 'r' # to make movement more comfortable - player can pick directions in advance

    def get_keys(self):
        keys = pg.key.get_pressed() # object denoting which keys are currently held down

        if keys[pg.K_LEFT] or keys[pg.K_a]: # supporting both arrows and WSAD movement
            self.wanna_go = 'l'
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.wanna_go = 'r'
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.wanna_go = 'u'
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.wanna_go = 'd'

    def collide_walls(self, dir):
        hitted = pg.sprite.spritecollide(self, self.game.walls, False) # False, so they don't get deleted

        if dir == 'x':
            if hitted:
                if self.vel_x > 0:
                    self.rect.x = hitted[0].rect.left - self.rect.width
                if self.vel_x < 0:
                    self.rect.x = hitted[0].rect.right

                self.vel_x = 0
        elif dir == 'y':
            if hitted:
                if self.vel_y > 0:
                    self.rect.y = hitted[0].rect.top - self.rect.height
                if self.vel_y < 0:
                    self.rect.y = hitted[0].rect.bottom

                self.vel_y = 0

    def update(self):
        self.get_keys()

        # make sure speeds are always set correctly (every collide sets appropriate speeds to 0)
        if self.wanna_go == 'l':
            self.vel_x = -self.speed
        elif self.wanna_go == 'r':
            self.vel_x = self.speed
        elif self.wanna_go == 'u':
            self.vel_y = -self.speed
        elif self.wanna_go == 'd':
            self.vel_y = self.speed

        # collisions check - change player coordinate and then check for any collisions
        # this order ensures movement system working properly
        self.rect.x += self.vel_x
        self.collide_walls('x')

        self.rect.y += self.vel_y
        self.collide_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
