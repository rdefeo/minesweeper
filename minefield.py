#!/usr/bin/env python3

from collections import defaultdict
from random import randrange

# Mine Field 
FLAG = -2
MINE = -1
EMPTY = 0
DISPLAY = { -2: '`', -1: '*', 0: ' ', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8' }

# Mine Field Display
VISIBLE = 0
COVERED = 1
FLAGGED = 2

class MineField():
    def __init__(self, width, height, difficulty, debug=0):
        self.width = int(width)
        self.height = int(height)
        self.difficulty = float(difficulty)
        self.mine_count = int((self.width * self.height) * self.difficulty)
        self.grid = defaultdict(int)
        self.cover = defaultdict(int)
        self.started = False # has the player clicked yet?
        self.losing_mine = None
        self.debug = debug
        self.create()
        
    def create(self):
        # difficulty determines how many mines in grid as a percentage of overall cells
        print(f"Creating {self.mine_count} mines on {self.width} x {self.height}, difficulty = {self.difficulty}")

        # nothing is visible at the start!
        for y in range(self.height):
            for x in range(self.width):
                self.cover[(x,y)] = COVERED if self.debug == 0 else VISIBLE

        if self.debug:
            self.place_mines((self.width//2,self.height//2))

    def neighbors(self, pos):
        for (dx,dy) in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            n = (pos[0]+dx,pos[1]+dy)
            if n not in self.grid:
                continue
            yield n
        
    def place_mines(self, clicked):
        total = self.mine_count
        while total:
            # try to place a mine at x,y
            b = randrange(self.width * self.height)
            x = b % self.width
            y = b // self.width
            # don't place a mine here - it's instant game over!
            if (x,y) == clicked:
                continue
            # make sure the mine isn't one of our neighbor cells
            good_mine = True
            for n in self.neighbors(clicked):
                if (x,y) == n:
                    good_mine = False
                    break
            if not good_mine:
                continue
            if self.grid[(x,y)] != MINE:
                self.grid[(x,y)] = MINE
                total -= 1
                        
        # add the number counts
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[(x,y)] == MINE:
                    continue
                mines = 0
                for n in self.neighbors((x,y)):
                    if self.grid[n] == MINE:
                        mines += 1
                self.grid[(x,y)] = mines
        self.started = True
                
    def try_clear_space(self,pos):
        seen = set()
        q = [ pos ]
        while q:
            p = q.pop(0)
            if p in seen:
                continue
            seen.add(p)
            if self.grid[p] != EMPTY:
                continue
            for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
                np = (p[0]+dx,p[1]+dy)
                if np in self.grid:
                    if self.cover[np] == COVERED:
                        self.cover[np] = VISIBLE
                        q.append(np)
    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                s += DISPLAY[self.grid[(x,y)]]
            s += '\n'
        return s

    def win(self):
        if sum([1 for c in self.cover.values() if c != VISIBLE]) == self.mine_count:
            return True
        return False

    def __str__(self):
        s = ''
        for y in range(self.field.height):
            for x in range(self.field.width):
                if self.cover[(x,y)] == VISIBLE:
                    s += DISPLAY[self.field[(x,y)]]
                elif self.cover[(x,y)] == FLAGGED:
                    s += 'F'
                else:
                    s += '_'
            s += '\n'
        return s

if __name__ == "__main__":
    print("Running tests...")
    f = MineField(10,5,0.1)
    print(f)

