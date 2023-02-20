#!/usr/bin/env python3

import pygame
import time
from minefield import *

NUM_COLOR = { 1: (0,0,255), 2: (0,130,0), 3: (214,0,0),
              4: (0,0,132), 5: (132,0,0), 6: (0,130,132),
              7: (132,0,132), 8: (117,117,117),
              -1: (0,0,0) }
PLAYING = 0
GAME_OVER = 1
WIN = 2

class Graphics():

    def __init__(self,mine_width,mine_height,mine_size=50):
        self.mine_width = int(mine_width)
        self.mine_height = int(mine_height)
        self.mine_size = mine_size
        self.resolution = (self.mine_width*self.mine_size, self.mine_height*self.mine_size)
        self.state = PLAYING
        
    def set_mine_size(self,mine_size):
        self.mine_size = mine_size
        self.resolution = (self.mine_width*self.mine_size, self.mine_height*self.mine_size)

    def init(self):
        start = time.time()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("PySweeper")
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.font = pygame.font.Font('mine-sweeper.ttf', 24)
        pygame.display.flip()   
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.QUIT)
        print(f"Initialization time: {round(time.time()-start,3)}")

    def draw(self,mfc: MineFieldCover,mf: MineField):
        self.screen.fill((128,128,128))
        for y in range(mfc.field.height):
            for x in range(mfc.field.width):
                cover = mfc.cover[(x,y)]
                mine = mfc.field.grid[(x,y)]
                xpos = x * self.mine_size
                ypos = y * self.mine_size
                if cover == COVERED:
                    pygame.draw.rect(self.screen,(148,148,148),pygame.Rect(xpos,ypos,self.mine_size,self.mine_size))
                    pygame.draw.rect(self.screen,(60,60,60),pygame.Rect(xpos,ypos,self.mine_size,self.mine_size),2)                
                elif cover == FLAGGED:
                    pygame.draw.rect(self.screen,(148,148,148),pygame.Rect(xpos,ypos,self.mine_size,self.mine_size))
                    pygame.draw.rect(self.screen,(60,60,60),pygame.Rect(xpos,ypos,self.mine_size,self.mine_size),2)
                    flag = self.font.render('`', True, (255,0,0))
                    flag_rect = flag.get_rect()
                    flag_rect.center = (xpos + self.mine_size//2, ypos + self.mine_size//2)
                    self.screen.blit(flag, flag_rect)
                else:
                    pygame.draw.rect(self.screen,(60,60,60),pygame.Rect(xpos,ypos,self.mine_size,self.mine_size),2)
                    g = mfc.field.grid[(x,y)]
                    if g != 0:
                        num = self.font.render(DISPLAY[mfc.field.grid[(x,y)]], True, NUM_COLOR[g])
                        num_rect = num.get_rect()
                        num_rect.center = (xpos + self.mine_size//2, ypos + self.mine_size//2)
                        self.screen.blit(num, num_rect)
        if self.state == GAME_OVER:
            self.game_over()
        
    def game_over(self):
        self.state = GAME_OVER
        self.banner("Game Over!", (255,255,0))

    def win(self):
        self.state = WIN
        self.banner("YOU WIN!",(0,255,0))

    def banner(self,text,color,bg_color=(24,24,24)):
        txt = self.font.render(text, True, color, bg_color)
        txt_surf = pygame.Surface(txt.get_rect().inflate(24,12).size)
        txt_surf.fill(bg_color)
        txt_surf.blit(txt,txt.get_rect(center=txt_surf.get_rect().center))
        txt_surf_rect = txt_surf.get_rect()
        txt_surf_rect.center = (self.resolution[0]//2,self.resolution[1]//2)
        self.screen.blit(txt_surf,txt_surf_rect)
        
    def restart(self):
        self.state = PLAYING
