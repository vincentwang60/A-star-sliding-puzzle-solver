import pygame as pg
import sys
import random as r
import time
import copy
from settings import *
from graph import *
from sprites import *

class Game:
    def __init__(self):#setup pygame and clock
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self): # initialize all variables and do all the setup for a new game
        self.solved = False
        self.progress = 0
        self.drawn = False
        self.moves = 0
        self.solve_tick = 0
        self.solution = []
        self.all_sprites = pg.sprite.Group()
        self.tile_sprites = pg.sprite.Group()
        self.graph = Graph()
        self.bg = bg(self)
        self.tile_list = []
        for num_tile in self.graph.start_node.tile_list:
            self.tile_list.append(tile(self,num_tile.pos[0],num_tile.pos[1],num_tile.num))
        self.missing_coord = self.graph.start_node.missing_coord

    def run(self):#game loop
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):#move tiles and start solver if not started
        if self.solved:
            if self.solve_tick < SOLVE_DELAY:
                self.solve_tick += 1
            else:
                self.solve_tick = 0
                if len(self.solution) > 0:
                    self.move(self.solution[0])
                    self.solution.pop(0)
            for tile in self.tile_list:
                tile.frame_update()
        if self.drawn and not self.solved:
            start = time.time()
            result = self.graph.a_star()
            end = time.time()
            self.time_taken = end-start
            if result != False:
                self.solution = result
            self.solved = True 

    def move(self,dir):#follows instructions given by solver
        moving_tile = None
        if dir == 0:
            moving_tile = [self.missing_coord[0],self.missing_coord[1]+1]
        if dir == 1:
            moving_tile = [self.missing_coord[0]-1,self.missing_coord[1]]
        if dir == 2:
            moving_tile = [self.missing_coord[0],self.missing_coord[1]-1]
        if dir == 3:
            moving_tile = [self.missing_coord[0]+1,self.missing_coord[1]]
        for tile in self.tile_list:
            if tile.pos[0] == moving_tile[0] and tile.pos[1] == moving_tile[1]:
                self.missing_coord = moving_tile
                tile.move(dir)
                tile.update()
                self.bg.update()
        self.moves += 1

    def draw(self):
        self.screen.fill(BGCOLOR)
        if not self.drawn or self.solved:
            self.all_sprites.draw(self.screen)
            self.tile_sprites.draw(self.screen)
            if not self.solved:
                self.draw_text(self.screen,str('Solving...'),WIDTH/2,HEIGHT-20,GRAY4,20)
            else:
                self.draw_text(self.screen,'Solved in '+str(self.time_taken),WIDTH/2,HEIGHT-20,GRAY4,20)
            pg.display.flip()
        self.drawn = True

    def events(self): #catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw_text(self,surface,text,x,y,color,size):
        font_name = pg.font.match_font(FONT_NAME)
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x),int(y))
        surface.blit(text_surface,text_rect)

g = Game()
g.new()
g.run()
