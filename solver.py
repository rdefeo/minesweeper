
from minefield import *
import sympy
from collections import Counter

class Solver():
    def __init__(self,mf:MineField):
        self.mf = mf
        
    def best_move(self):
        # if we haven't started this game, click anywhere
        if self.mf.started == False:
            x, y = self.mf.width // 2, self.mf.height // 2
            return (x,y), VISIBLE

        # Naive approach first:
        # For each visible numbered cell, count how many covered and
        # flagged neighbors. Based on how many we find, we can quickly
        # determine if we need to "click" or "flag" one of the unknown cells.
        for m,v in self.mf.grid.items():
            if self.mf.cover[m] == VISIBLE and v > EMPTY:
                flag_count = 0
                unknowns = []
                for n in self.mf.neighbors(m):
                    if self.mf.cover[n] == FLAGGED:
                        flag_count += 1
                    elif self.mf.cover[n] == COVERED:
                        unknowns.append(n)
                if v == flag_count and len(unknowns) > 0:
                    return unknowns[0], VISIBLE
                if flag_count == 0 and v == len(unknowns):
                    return unknowns[0], FLAGGED
                if v == (flag_count + len(unknowns)) and len(unknowns) > 0:
                    return unknowns[0], FLAGGED
        
        # Gaussian Elimination method:
        # For each visible numbered cell that has unknown neighbors, create
        # an equation that links the unknown cells to the mine count. From these
        # equations, we create a matrix and then compute the reduced row echelon form.
        # Then we check the resulting rows to see if there are any obvious solutions.
        point_index = []
        equations = []
        for m,v in self.mf.grid.items():
            if self.mf.cover[m] == VISIBLE and v > EMPTY:
                flag_count = 0
                unknowns = []
                for n in self.mf.neighbors(m):
                    if self.mf.cover[n] == COVERED:
                        unknowns.append(n)
                        if n not in point_index:
                            point_index.append(n)
                    elif self.mf.cover[n] == FLAGGED:
                        flag_count += 1    
                if len(unknowns):
                    equations.append((unknowns,v-flag_count))
        A = []
        for unknowns, answer in equations:
            eq = [0] * len(point_index)
            for u in unknowns:
                eq[point_index.index(u)] = 1
            eq.append(answer)
            A.append(eq)

        # Compute the reduced row echelon form of the matrix
        R, pivots = sympy.Matrix(A).rref()
        #print(R)

        for row in range(sympy.shape(R)[0]):
            r = list(R.row(row))
            count = Counter(r[:-1])
            if count[1] == 1 and count[0] == len(r)-2 and r[-1] in [0,1]:
                index = r[:-1].index(1)
                return point_index[index], [VISIBLE, FLAGGED][r[-1]]
            
        return None, None
