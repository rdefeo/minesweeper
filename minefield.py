#!/usr/bin/env python3

from collections import defaultdict
from random import randrange

# Mine Field 
BOMB = -1
EMPTY = 0
DISPLAY = { -1: '*', 0: ' ', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8' }

# Mine Field Display
VISIBLE = 0
COVERED = 1
FLAGGED = 2

class MineField():
    def __init__(self, width, height, difficulty):
        self.width = int(width)
        self.height = int(height)
        self.difficulty = float(difficulty)
        self.bomb_count = int((self.width * self.height) * self.difficulty)
        self.grid = defaultdict(int)
        self.create()
        
    def create(self):
        # difficulty determines how many bombs in grid as a percentage of overall cells
        print(f"Creating {self.bomb_count} bombs on {self.width} x {self.height}")
        total = self.bomb_count
        while total:
            b = randrange(self.width * self.height)
            x = b % self.width
            y = b // self.width
            if self.grid[(x,y)] != BOMB:
                self.grid[(x,y)] = BOMB
                total -= 1
                        
        # add the number counts
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[(x,y)] == BOMB:
                    continue
                bombs = 0
                for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
                    p = (x+dx,y+dy)
                    if p in self.grid:
                        if self.grid[p] == BOMB:
                            bombs += 1
                self.grid[(x,y)] = bombs
            
    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                s += DISPLAY[self.grid[(x,y)]]
            s += '\n'
        return s

class MineFieldCover():
    def __init__(self, field):
        self.field = field
        self.cover = defaultdict(int)

        # nothing is visible at the start!
        for y in range(self.field.height):
            for x in range(self.field.width):
                self.cover[(x,y)] = COVERED

    def try_clear_space(self,pos):
        seen = set()
        q = [ pos ]
        while q:
            p = q.pop(0)
            if p in seen:
                continue
            seen.add(p)
            if self.field.grid[p] != EMPTY:
                continue
            for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
                np = (p[0]+dx,p[1]+dy)
                if np in self.field.grid:
                    if self.cover[np] == COVERED:
                        self.cover[np] = VISIBLE
                        q.append(np)

    def win(self):
        if sum([1 for c in self.cover.values() if c != VISIBLE]) == self.field.bomb_count:
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
    f = MineFieldCover(MineField(10,5,0.1))
    print(f)
    print(f.field)
