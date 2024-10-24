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
cost_lin = [0 for _ in range(256)]
cost_xy = [[0 for _ in range(16)] for _ in range(16)] # this is correct

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
print(f"init in loop - List: {t:} millisseconds")

t = millis() 
for i in range(iterations()):
    clear_xy_cost()
t = millis() - t 
print(f"init in loop - list of lists: {t:} milliseconds")            

t = millis() 
for i in range(iterations()):
    cost_lin = [0]*256
t = millis() - t 
print(f"list comprehension - 'cost_lin = [0]*256'   : {t:} milliseconds")            

t = millis() 
for i in range(iterations()):
    cost_lin = [[0]*16 for _ in range(16)]
t = millis() - t 
print(f"list comprehension - 'cost_lin = [[0]*16 for _ in range(16)]'   : {t:} milliseconds")            
