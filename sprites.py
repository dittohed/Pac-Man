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
        self.speed = 200
        self.vel_x, self.vel_y = 0, 0

    def get_keys(self):
        self.vel_x, self.vel_y = 0, 0
        keys = pg.key.get_pressed() # object denoting which keys are currently held down

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -self.speed
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = self.speed
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel_y = -self.speed
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel_y = self.speed


    def move(self, dx = 0, dy = 0):
        if not self.collide_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_walls(self, dx = 0, dy = 0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True

        return False

    def update(self):
        self.get_keys()

        self.x += self.vel_x * self.game.dt
        self.y += self.vel_y * self.game.dt
        self.rect.topleft = (self.x, self.y)

        if pg.sprite.spritecollideany(self, self.game.walls): # check collisions between arg1 and arg2
            self.x -= self.vel_x * self.game.dt
            self.y -= self.vel_y * self.game.dt
            self.rect.topleft = (self.x, self.y)

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
