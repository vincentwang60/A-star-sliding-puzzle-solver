import pygame as pg
import random as r
from settings import *

class bg(pg.sprite.Sprite):#displays moves and fills in background
    def __init__(self,game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.image.fill(GRAY2)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.bar = 0

        'add top box'
        pg.draw.line(self.image,GRAY3,(0,50),(WIDTH,50),9)
        pg.draw.line(self.image,GRAY1,(1,50),(WIDTH-1,50),7)
        self.game.draw_text(self.image,'Moves: ' + str(game.moves),WIDTH/2,50/2,GRAY4,30)

        'add tile backdrop'
        pg.draw.rect(self.image,GRAY3,pg.Rect((TOPLEFT[0]-GAMEBORDER,TOPLEFT[1]-GAMEBORDER),(TILESIZE*TILESIDECOUNT+2*GAMEBORDER,TILESIZE*TILESIDECOUNT+2*GAMEBORDER)))

    def update(self):
        goal = int((self.game.progress**2) * (WIDTH-2))
        if self.bar < goal:
            self.bar += 5
        else:
            self.game.move_bar = False
        pg.draw.line(self.image,GRAY3,(0,50),(WIDTH,50),9)
        pg.draw.line(self.image,GRAY1,(1,50),(WIDTH-1,50),7)
        pg.draw.line(self.image,BLUE,(2,50),(self.bar,50),5)
        pg.draw.rect(self.image,GRAY2,pg.Rect(WIDTH/2-100,10,200,30))
        self.game.draw_text(self.image,'Moves: ' + str(self.game.moves),WIDTH/2,50/2,GRAY4,30)

class tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.groups = game.tile_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.target = self.coord_to_pix(tuple((x,y)))
        self.rect.x = self.target[0]
        self.rect.y = self.target[1]
        self.pos = tuple((x,y))
        self.num = num
        if self.num != 0:
            self.image.fill(GRAY2)
            pg.draw.rect(self.image,GRAY1,pg.Rect(BORDER,BORDER,TILESIZE-2*BORDER,TILESIZE-2*BORDER))
            self.pos = tuple((x,y))
            self.game.draw_text(self.image,str(num),50,52,GRAY4,50)
        else:
            self.image = pg.Surface((1, 1))
            self.image.fill(GRAY3)
            self.rect.x = -100
            self.rect.y = -100
            self.pos = tuple((-100,-100))
            self.target = tuple((100,100))

    def move(self,dir):
        if dir == 0:
            self.pos = tuple((self.pos[0],self.pos[1]-1))
        if dir == 1:
            self.pos = tuple((self.pos[0]+1,self.pos[1]))
        if dir == 2:
            self.pos = tuple((self.pos[0],self.pos[1]+1))
        if dir == 3:
            self.pos = tuple((self.pos[0]-1,self.pos[1]))

    def update(self):
        self.target = self.coord_to_pix(self.pos)

    def frame_update(self):
        if ANIM_SPEED == 0:
            speed = 10
        if ANIM_SPEED == 1:
            speed = 20
        if ANIM_SPEED == 2:
            speed = 50
        if self.rect.x < self.target[0]:
            self.rect.x += speed
        elif self.rect.x > self.target[0]:
            self.rect.x -= speed
        if self.rect.y < self.target[1]:
            self.rect.y += speed
        elif self.rect.y > self.target[1]:
            self.rect.y -= speed

    def coord_to_pix(self,coords):
        return (coords[0]*TILESIZE + TOPLEFT[0],coords[1]*TILESIZE + TOPLEFT[1])
