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
        # currently these are actual player coordinates (because rect coordinates must be integers)
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # moving
        self.speed = 150
        self.vel_x, self.vel_y = 0, 0
        self.wanna_go = 'r' # to make movement more comfortable and lacking-1-pixel-to-turn-right problem

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
        hitted = pg.sprite.spritecollide(self, self.game.walls, False) #False, so they don't get deleted

        if dir == 'x':
            if hitted:
                # print("x dir collison")
                # each case covers different crossroad problem type
                # this prevents blocking player, because it's 1 pixel higher than a corridor he wants to enter

                # and make sure that corridor is above a hitted wall
                if self.vel_y < 0 and \
                self.game.screen.get_at((hitted[0].rect.x, hitted[0].rect.y - 1))[:3] == (0, 0, 0) and \
                (hitted[0].rect.y - self.rect.y > 0.8 * self.rect.height): # 0.8 is small enough & yet works
                    # going up, wanting to turn left or right
                    self.vel_y = 0
                    self.y = hitted[0].rect.y - self.rect.height
                    self.rect.y = self.y
                elif self.vel_y > 0 and \
                self.game.screen.get_at((hitted[0].rect.x, hitted[0].rect.y + 1))[:3] == (0, 0, 0) and \
                self.rect.y - hitted[0].rect.y > 0.8 * self.rect.height:
                    # going down, wanting to turn left or right
                    self.vel_y = 0
                    self.y = hitted[0].rect.y + self.rect.height
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
                # print("y dir collison")
                if self.vel_y > 0:
                    self.y = hitted[0].rect.top - self.rect.height
                if self.vel_y < 0:
                    self.y = hitted[0].rect.bottom

                self.vel_y = 0
                self.rect.y = self.y

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

        # velocities are pixels per second, not per frame!
        self.x += self.vel_x * self.game.dt
        self.y += self.vel_y * self.game.dt

        # collisions check
        self.rect.x = self.x # control player sprite actual x-coordinate
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
