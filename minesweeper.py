#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from minefield import *
from graphics import *
import pygame
import sys
import argparse
import time


parser = argparse.ArgumentParser(description="Minesweeper")
parser.add_argument('-W','--width',type=int,nargs='?',default=15,
                    help='Width of minefield (default: %(default)i)')
parser.add_argument('-H','--height',type=int,nargs='?',default=10,
                    help='Height of minefield (default: %(default)i)')
parser.add_argument('-D','--difficulty',type=float,nargs='?',default=0.1,
                    help='Difficulty, measured as a percentage of total cells that have a bomb.\
                    A value of 0.1 means 10%% of the cells will have a bomb. (default: %(default)f)')
args = parser.parse_args()

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
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            if event.key == pygame.K_r:
                print("Restarting game")
                mf = MineField(WIDTH, HEIGHT, DIFF)
                mfc = MineFieldCover(mf)
                gfx.restart()
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()

pygame.quit()







