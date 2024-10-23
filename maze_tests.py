"""
 Here can go tests for the maze implementations
"""
import time


cost_lin = [0]*256
cost_xy = [[0]*16]*16

def clear_lin_cost():
    for i in range(256):
        cost_lin[i] = 0

def clear_xy_cost():
    for i in range(16):
        for j in range(16):
            cost_xy[i][j] = 0 

t = time.time()
for i in range(10000):
    clear_lin_cost()
t = time.time() - t
print(f"Linear: {t:.6f} seconds")

t = time.time() 
for i in range(10000):
    clear_xy_cost()
t = time.time() - t 
print(f"XY: {t:.6f} seconds")            