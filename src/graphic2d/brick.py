import os
import random
import colorsys

import graphic2d
from graphic2d import general

# 
class Brick:
    def __init__(self):
        rowcol = [0,0]
        coords = [0,0]
        pyrect = None
        color1 = (255,0,0)
        displayed = True

    def getNextBrick(self, side):
        
        row2 = self.rowcol[0]
        col2 = self.rowcol[1]
        if side == general.INTER_LEFT: 
            col2 -= 1
            if col2 < 0: return None
        if side == general.INTER_RIGHT: 
            col2 += 1
            if col2 >= general.brick_nb_cols: return None
        if side == general.INTER_TOP: 
            row2 -= 1
            if row2 < 0: return None
        if side == general.INTER_BOTTOM: 
            row2 += 1
            if row2 >= general.brick_nb_rows: return None
        ix1 = row2 * general.brick_nb_cols + col2
        return general.bricksArray[ix1]
        
def isBrickDisplayed(brickB):
    if brickB is None: return False
    return brickB.displayed
    
        
