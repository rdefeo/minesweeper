#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from minefield import *
from graphics import *
import pygame
import sys
import argparse
import time


class MultiLineFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('ML|'):
            return text[3:].splitlines()
        return argparse.HelpFormatter._split_lines(self,text,width)
    
parser = argparse.ArgumentParser(description="Minesweeper", formatter_class=MultiLineFormatter)
parser.add_argument('-W','--width',type=int,nargs='?',default=15,
                    help="ML|Width of minefield\n(default: %(default)i)")
parser.add_argument('-H','--height',type=int,nargs='?',default=10,
                    help="ML|Height of minefield\n(default: %(default)i)")
parser.add_argument('-D','--difficulty',type=float,nargs='?',default=0.1,
                    help="ML|Difficulty, measured as a percentage of total cells that have a bomb.\n"
                    "A value of 0.15 means 15%% of the cells will have a bomb.\n"
                    "(default: %(default)f)")
parser.add_argument('--debug',type=int,nargs='?',default=0)
args = parser.parse_args()

bombs = int(args.width*args.height*args.difficulty)
#if bombs <= 0 or bombs >= (args.width*args.height)//2:
#    print("ERROR: Bad arguments! Difficulty too high or grid poorly sized")
#    exit()
    
print(args.width,args.height,args.difficulty)

gfx = Graphics(args.width,args.height)
gfx.init()

mf = MineField(args.width,args.height,args.difficulty)

print("Starting game loop")

# game loop
running = True
while running:
    gfx.clock.tick(30)

    gfx.draw(mf)

    if mf.win():
        gfx.win()
        
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and gfx.state == PLAYING:
            mx, my = event.pos
            cx = mx // gfx.mine_size
            cy = my // gfx.mine_size
            if event.button == 1:
                if mf.started == False:
                    mf.place_bombs((cx,cy))
                    
                if mf.cover[(cx,cy)] == COVERED:
                    mf.cover[(cx,cy)] = VISIBLE
                    if mf.grid[(cx,cy)] == MINE:
                        print("GAME OVER!")
                        mf.losing_mine = (cx,cy)
                        gfx.game_over(mf)
                    else:
                        mf.try_clear_space((cx,cy))
            elif event.button == 3:
                if mf.cover[(cx,cy)] != VISIBLE:
                    if mf.cover[(cx,cy)] == COVERED:
                        mf.cover[(cx,cy)] = FLAGGED
                    else:
                        mf.cover[(cx,cy)] = COVERED
            continue
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False
                break
            if event.key == pygame.K_r:
                print("Restarting game")
                mf = MineField(args.width, args.height, args.difficulty)
                gfx.restart()
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()

pygame.quit()







