import os
import sys

from maze_support import *


cost = [0]*MAZE_CELL_COUNT
walls = [0]*MAZE_CELL_COUNT


floodfail = 0
debug = 0


def cell_id(x, y):
    return y + x * MAZE_SIZE


def cell_xy(cell):
    return (cell // 16, cell % 16)


def add_wall(cell, heading):
    x, y = cell_xy(cell)
    if (heading == DIR_NORTH):
        walls[cell] |= NORTH_WALL
        if y < 15:
            walls[cell+1] |= SOUTH_WALL
    elif (heading == DIR_EAST):
        walls[cell] |= EAST_WALL
        if x < 15:
            walls[cell+16] |= WEST_WALL
    elif (heading == DIR_SOUTH):
        walls[cell] |= SOUTH_WALL
        if y > 0:
            walls[cell-1] |= NORTH_WALL
    elif (heading == DIR_WEST):
        walls[cell] |= WEST_WALL
        if x > 0:
            walls[cell-16] |= EAST_WALL


def get_walls(x, y):
    return walls[cell_id(x, y)]


def get_cost(x, y):
    return cost[cell_id(x, y)]


def maze_clear():
    walls = [0]*MAZE_CELL_COUNT
    for x in range(16):
        add_wall(cell_id(x, 0), DIR_SOUTH)
        add_wall(cell_id(x, 15), DIR_NORTH)
        add_wall(cell_id(0, x), DIR_WEST)
        add_wall(cell_id(15, x), DIR_EAST)


def showmaze():  # show the maze
    for y in range(15, -1, -1):
        line = "+"
        for x in range(16):
            if get_walls(x, y) & NORTH_WALL:
                line += "---+"
            else:
                line += "   +"
        print(line)
        line = ""
        for x in range(16):
            if get_walls(x, y) & WEST_WALL:
                line += "|"
            else:
                line += " "
            if get_cost(x, y) is not None:
                line += f"{get_cost(x,y):>3}"
            else:
                line += "   "
        if get_walls(15, y) & EAST_WALL:
            line += "|"
        else:
            line += " "
        print(line)
    line = "+"
    for x in range(16):
        if get_walls(x, y) & SOUTH_WALL:
            line += "---+"
        else:
            line += "   +"
    print(line)


def floodmaze(target_cell, start_cell=0):
    """
    Floods the maze from target_cell to all other cells.
    The shortest path (cost) from the target cell to each 
    other cell is stored in the cost array.
    The start_cell parameter is not used (yet). It could be used to 
    terminate the search early.
   """
    global cost, walls
    cost = [MAX_COST]*MAZE_CELL_COUNT
    cost[target_cell] = 0
    queue = [0]*MAZE_CELL_COUNT  # fixed size queue more efficient?
    head = 0
    tail = 0
    queue[tail] = target_cell
    tail += 1
    while (head != tail):
        here = queue[head]
        head = head + 1
        cost_here = cost[here]
        if ((walls[here] & SOUTH_WALL) == 0):
            if ((cost[here - 1] == MAX_COST)):
                cost[here - 1] = cost_here + 1
                queue[tail] = here-1
                tail = tail + 1
        if ((walls[here] & EAST_WALL) == 0):
            if ((cost[here + MAZE_SIZE] == MAX_COST)):
                cost[here + MAZE_SIZE] = cost_here + 1
                queue[tail] = here + MAZE_SIZE
                tail = tail + 1
        if ((walls[here] & NORTH_WALL) == 0):
            if ((cost[here + 1] == 256)):
                cost[here + 1] = cost_here + 1
                queue[tail] = here + 1
                tail = tail + 1
        if ((walls[here] & WEST_WALL) == 0):
            if ((cost[here - MAZE_SIZE] == MAX_COST)):
                cost[here - MAZE_SIZE] = cost_here + 1
                queue[tail] = here - MAZE_SIZE
                tail = tail + 1


maze_clear()
add_wall(cell_id(0, 0), DIR_EAST)
add_wall(cell_id(7, 7), DIR_WEST)
add_wall(cell_id(7, 7), DIR_SOUTH)
add_wall(cell_id(8, 7), DIR_SOUTH)
add_wall(cell_id(8, 7), DIR_EAST)
add_wall(cell_id(8, 8), DIR_NORTH)
add_wall(cell_id(7, 8), DIR_NORTH)
add_wall(cell_id(7, 8), DIR_WEST)
add_wall(cell_id(4, 4), DIR_NORTH)
add_wall(cell_id(4, 4), DIR_EAST)
add_wall(cell_id(4, 4), DIR_SOUTH)
add_wall(cell_id(4, 4), DIR_WEST)

start_time = millis()
for _ in range(iterations()):
    floodmaze(cell_id(7, 7), cell_id(0, 0))

end_time = millis()
t = end_time - start_time
showmaze()
print("Flood distance correct: ", get_cost(0, 0) == 20)
print(f"Flood fail is {floodfail}")
print(f"{sys.implementation.name} - maze_dh: Execution Time for {iterations()} iterations: {t:} milliseconds")
