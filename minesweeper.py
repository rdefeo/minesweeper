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
args = parser.parse_args()

bombs = int(args.width*args.height*args.difficulty)
if bombs <= 0 or bombs >= (args.width*args.height)//2:
    print("ERROR: Bad arguments!")
    exit()
    
print(args.width,args.height,args.difficulty)

gfx = Graphics(args.width,args.height)
gfx.init()

mf = MineField(args.width,args.height,args.difficulty)
mfc = MineFieldCover(mf)

print("Starting game loop")

# game loop
running = True
while running:
    gfx.clock.tick(30)

    gfx.draw(mfc,mf)

    if mfc.win():
        gfx.win()
        
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and gfx.state == PLAYING:
            mx, my = event.pos
            cx = mx // gfx.mine_size
            cy = my // gfx.mine_size
            if event.button == 1:
                if mfc.cover[(cx,cy)] == COVERED:
                    mfc.cover[(cx,cy)] = VISIBLE
                    if mfc.field.grid[(cx,cy)] == BOMB:
                        print("GAME OVER!")
                        gfx.game_over()
                    else:
                        mfc.try_clear_space((cx,cy))
            elif event.button == 3:
                if mfc.cover[(cx,cy)] != VISIBLE:
                    if mfc.cover[(cx,cy)] == COVERED:
                        mfc.cover[(cx,cy)] = FLAGGED
                    else:
                        mfc.cover[(cx,cy)] = COVERED
            continue
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False
                break
            if event.key == pygame.K_r:
                print("Restarting game")
                mf = MineField(args.width, args.height, args.difficulty)
                mfc = MineFieldCover(mf)
                gfx.restart()
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()

pygame.quit()







