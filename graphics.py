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
BORDER = 6

class Graphics():

    def __init__(self,mine_width,mine_height,mine_size=40):
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
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('mine-sweeper.ttf', 18)
        pygame.display.flip()   
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.QUIT)
        print(f"Initialization time: {round(time.time()-start,3)}")

    def draw(self,mf: MineField):
        self.screen.fill((192,192,192))
        for y in range(mf.height):
            for x in range(mf.width):
                cover = mf.cover[(x,y)]
                mine = mf.grid[(x,y)]
                xpos = x * self.mine_size
                ypos = y * self.mine_size
                if cover == COVERED or cover == FLAGGED:
                    pygame.draw.polygon(self.screen,(222,222,222),[(xpos,ypos),(xpos+self.mine_size,ypos),(xpos,ypos+self.mine_size)])
                    pygame.draw.polygon(self.screen,(128,128,128),[(xpos+self.mine_size,ypos),(xpos+self.mine_size,ypos+self.mine_size),(xpos,ypos+self.mine_size)])
                    pygame.draw.rect(self.screen,(192,192,192),pygame.Rect(xpos+BORDER,ypos+BORDER,self.mine_size-(BORDER*2),self.mine_size-(BORDER*2)))
                if cover == FLAGGED:
                    flag = self.font.render('`', True, (255,0,0))
                    flag_rect = flag.get_rect()
                    flag_rect.center = (xpos + self.mine_size//2, ypos + self.mine_size//2)
                    self.screen.blit(flag, flag_rect)
                elif cover == VISIBLE:
                    pygame.draw.line(self.screen,(128,128,128),(xpos,ypos),(xpos,ypos+self.mine_size),3)
                    pygame.draw.line(self.screen,(128,128,128),(xpos,ypos),(xpos+self.mine_size,ypos),3)
                    if (x,y) == mf.losing_mine:
                        pygame.draw.rect(self.screen,(220,0,0),pygame.Rect(xpos+2,ypos+2,self.mine_size-4,self.mine_size-4))
                    g = mf.grid[(x,y)]
                    if g != 0:
                        num = self.font.render(DISPLAY[mf.grid[(x,y)]], True, NUM_COLOR[g])
                        num_rect = num.get_rect()
                        num_rect.center = (xpos + self.mine_size//2, ypos + self.mine_size//2)
                        self.screen.blit(num, num_rect)
        if self.state == GAME_OVER:
            self.game_over(mf)
        
    def game_over(self,mf:MineField):
        self.state = GAME_OVER
        for c,v in mf.cover.items():
            if mf.grid[c] == MINE:
                mf.cover[c] = VISIBLE
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
