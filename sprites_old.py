import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()

        # initially grid coordinates,
        # now these are actual player coordinates (because rect coordinates must be integers)
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # moving
        self.speed = 150
        self.vel_x, self.vel_y = 0, 0
        self.wanna_go = 'r'

    def get_keys(self):
        # self.vel_x, self.vel_y = 0, 0
        keys = pg.key.get_pressed() # object denoting which keys are currently held down

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -self.speed
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = self.speed
            self.wanna_go = 'r'
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel_y = -self.speed
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel_y = self.speed

    def collide_walls(self, dir):
        hitted = pg.sprite.spritecollide(self, self.game.walls, False) #False, so they don't get deleted

        if dir == 'x':
            if hitted:
                if self.vel_x > 0 and hitted[0].rect.y - self.rect.y > (99 / 100) * self.rect.height:
                    self.vel_y = -self.speed
                    self.y = hitted[0].rect.y - self.rect.height
                    self.rect.y = self.y
                else:
                    if self.vel_x > 0:
                        self.x = hitted[0].rect.left - self.rect.width
                    if self.vel_x < 0:
                        self.x = hitted[0].rect.right

                    self.vel_x = 0
                    self.rect.x = self.x
        elif dir == 'y':
            if hitted:
                if self.vel_y > 0:
                    self.y = hitted[0].rect.top - self.rect.height
                if self.vel_y < 0:
                    self.y = hitted[0].rect.bottom
                self.vel_y = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()

        if self.wanna_go == 'r':
            self.vel_x = self.speed

        # velocities are pixels per second, not per frame!
        self.x += self.vel_x * self.game.dt
        self.y += self.vel_y * self.game.dt

        # to avoid not sticking to the wall bug
        self.rect.x = self.x
        self.collide_walls('x')

        self.rect.y = self.y
        self.collide_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
