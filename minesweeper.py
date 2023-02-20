#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from minefield import *
from graphics import *
import pygame
import sys
import time


WIDTH, HEIGHT, DIFF = 10, 5, 0.1
if len(sys.argv) == 3:
    WIDTH, HEIGHT = sys.argv[1:3]
elif len(sys.argv) == 4:
    WIDTH, HEIGHT, DIFF = sys.argv[1:4]
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)
print(WIDTH, HEIGHT, DIFF)

gfx = Graphics(WIDTH,HEIGHT)
gfx.init()


mf = MineField(WIDTH, HEIGHT, DIFF)
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







