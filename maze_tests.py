"""
 Here can go tests for the maze implementations
"""
import sys

import time
from maze_support import *

def iterations():
    if sys.implementation.name == 'micropython':
        return 100
    else:
        return 10000

print(sys.implementation.name)
print("start...")
cost_lin = [0]*256
cost_xy = [[0]*16]*16

def clear_lin_cost():
    for i in range(256):
        cost_lin[i] = 0

def clear_xy_cost():
    for i in range(16):
        for j in range(16):
            cost_xy[i][j] = 0 

t = millis()
for i in range(iterations()):
    clear_lin_cost()
t = millis() - t
print(f"Linear: {t:} millisseconds")

t = millis() 
for i in range(iterations()):
    clear_xy_cost()
t = millis() - t 
print(f"XY: {t:} milliseconds")            
