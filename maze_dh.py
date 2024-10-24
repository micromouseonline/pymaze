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

    Optimized flood fill for the maze. This version improves
    performance by reducing redundant checks and making queue handling more efficient.
    """
    global cost, walls
    cost = [MAX_COST] * MAZE_CELL_COUNT
    cost[target_cell] = 0

    # Static size queue - no modulo needed
    queue = [0] * MAZE_CELL_COUNT
    head = 0
    tail = 1
    queue[0] = target_cell

    while head < tail:
        here = queue[head]
        head += 1
        cost_here = cost[here]
        walls_here = walls[here]
        # Handle SOUTH_WALL (cell - 1)
        if (walls_here & SOUTH_WALL) == 0:
            south_cell = here - 1
            if cost[south_cell] == MAX_COST:
                cost[south_cell] = cost_here + 1
                queue[tail] = south_cell
                tail += 1

        # Handle EAST_WALL (cell + MAZE_SIZE)
        if (walls_here & EAST_WALL) == 0:
            east_cell = here + MAZE_SIZE
            if cost[east_cell] == MAX_COST:
                cost[east_cell] = cost_here + 1
                queue[tail] = east_cell
                tail += 1

        # Handle NORTH_WALL (cell + 1)
        if (walls_here & NORTH_WALL) == 0:
            north_cell = here + 1
            if cost[north_cell] == MAX_COST:
                cost[north_cell] = cost_here + 1
                queue[tail] = north_cell
                tail += 1

        # Handle WEST_WALL (cell - MAZE_SIZE)
        if (walls_here & WEST_WALL) == 0:
            west_cell = here - MAZE_SIZE
            if cost[west_cell] == MAX_COST:
                cost[west_cell] = cost_here + 1
                queue[tail] = west_cell
                tail += 1

    return cost


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
