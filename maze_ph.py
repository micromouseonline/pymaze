"""
maze-ph.py
A simple, naive implementation of the maze and manhattan flood algorithm
The code is mostly developed from suggestions by copilot
"""

import time
from maze_support import *
import os
import sys

MAX_COST = 999
WALL_ABSENT = 0
WALL_PRESENT = 1
WALL_UNKNOWN = 2
WALL_VIRTUAL = 3
WALL_MASK = 3

ALL_UNKNOWN = 0b10101010


CLOSED_MAZE_MASK = 3
OPEN_MAZE_MASK = 1


# ways we can represent the maze as a string
VIEW_PLAIN = 0
VIEW_COSTS = 1
VIEW_DIRS = 2

"""
 * Directions are absolute and are not relative to any particular heading
 * these are maze things
"""
DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_COUNT = 4
DIR_BLOCKED = -1


class Maze:

    def __init__(self, size=16):
        self.size = size
        self.cost = [[None for _ in range(
            self.size)] for _ in range(self.size)]
        self.walls = {
            (row, col): {DIR_NORTH: WALL_UNKNOWN, DIR_EAST: WALL_UNKNOWN, DIR_SOUTH: WALL_UNKNOWN, DIR_WEST: WALL_UNKNOWN}
            for row in range(size)
            for col in range(size)
        }

    def clear_walls(self):
        self.walls = {
            (row, col): {DIR_NORTH: WALL_UNKNOWN, DIR_EAST: WALL_UNKNOWN, DIR_SOUTH: WALL_UNKNOWN, DIR_WEST: WALL_UNKNOWN}
            for row in range(self.size)
            for col in range(self.size)
        }
        for cell in range(16):
            maze.set_wall(cell, 0, DIR_SOUTH, WALL_PRESENT)
            maze.set_wall(cell, 15, DIR_NORTH, WALL_PRESENT)
            maze.set_wall(0, cell, DIR_WEST,  WALL_PRESENT)
            maze.set_wall(15, cell, DIR_EAST, WALL_PRESENT)

    def set_wall(self, col, row, direction, state):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            self.walls[(col, row)][direction] = state
            # Add wall on the opposite side for the neighboring cell
            if direction == DIR_NORTH and row < self.size - 1:
                self.walls[(col, row + 1)][DIR_SOUTH] = state
            elif direction == DIR_EAST and col < self.size - 1:
                self.walls[(col + 1, row)][DIR_WEST] = state
            elif direction == DIR_SOUTH and row > 0:
                self.walls[(col, row - 1)][DIR_NORTH] = state
            elif direction == DIR_WEST and col > 0:
                self.walls[(col - 1, row)][DIR_EAST] = state

    def get_wall(self, col, row, direction):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            return self.walls[(col, row)][direction]
        return

    def has_wall(self, col, row, direction):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            return self.walls[(col, row)][direction] == WALL_PRESENT
        return False

    def print_maze(self):
        for row in range(self.size - 1, -1, -1):
            line = "+"
            for col in range(self.size):
                if self.get_wall(col, row, DIR_NORTH) == WALL_PRESENT:
                    line += "---+"
                else:
                    line += "   +"
            print(line)
            line = ""
            for col in range(self.size):
                if self.get_wall(col, row, DIR_WEST) == WALL_PRESENT:
                    line += "|"
                else:
                    line += " "
                if self.cost[row][col] is not None:
                    line += f"{self.cost[col][row]:>3}"
                else:
                    line += "   "
            if self.get_wall(15, row, DIR_EAST) == WALL_PRESENT:
                line += "|"  # Rightmost boundary
            else:
                line += " "
            print(line)
        line = "+"
        for col in range(self.size):
            if self.get_wall(col, 0, DIR_SOUTH) == WALL_PRESENT:
                line += "---+"
            else:
                line += "   +"
        print(line)

    def flood(self, target_col, target_row):
        # Initialize cost matrix and queue
        self.cost = [[MAX_COST] * self.size for _ in range(self.size)]
        queue = [(target_col, target_row, 0)]  # dynamic queue
        self.cost[target_col][target_row] = 0  # Set target to zero distance

        head = 0
        while head < len(queue):
            x, y, dist = queue[head]
            head += 1
            dist += 1

            # Check and update neighboring cells
            if not self.has_wall(x, y, DIR_NORTH) and self.cost[x][y + 1] == MAX_COST:
                self.cost[x][y + 1] = dist
                queue.append((x, y + 1, dist))

            if not self.has_wall(x, y, DIR_EAST) and self.cost[x + 1][y] == MAX_COST:
                self.cost[x + 1][y] = dist
                queue.append((x + 1, y, dist))

            if not self.has_wall(x, y, DIR_SOUTH) and self.cost[x][y - 1] == MAX_COST:
                self.cost[x][y - 1] = dist
                queue.append((x, y - 1, dist))

            if not self.has_wall(x, y, DIR_WEST) and self.cost[x - 1][y] == MAX_COST:
                self.cost[x - 1][y] = dist
                queue.append((x - 1, y, dist))

        return self.cost


if __name__ == "__main__":
    # Example usage
    maze = Maze()

    maze.clear_walls()
    maze.set_wall(7, 7, DIR_WEST, WALL_PRESENT)
    maze.set_wall(7, 7, DIR_SOUTH, WALL_PRESENT)
    maze.set_wall(8, 7, DIR_SOUTH, WALL_PRESENT)
    maze.set_wall(8, 7, DIR_EAST, WALL_PRESENT)
    maze.set_wall(8, 8, DIR_EAST, WALL_ABSENT)
    maze.set_wall(8, 8, DIR_NORTH, WALL_PRESENT)
    maze.set_wall(7, 8, DIR_NORTH, WALL_PRESENT)
    maze.set_wall(7, 8, DIR_WEST, WALL_PRESENT)
    # check that a closed off area does not get flooded
    maze.set_wall(4, 4, DIR_NORTH, WALL_PRESENT)
    maze.set_wall(4, 4, DIR_EAST, WALL_PRESENT)
    maze.set_wall(4, 4, DIR_SOUTH, WALL_PRESENT)
    maze.set_wall(4, 4, DIR_WEST, WALL_PRESENT)

    maze.print_maze()

    start_time = millis()
    for _ in range(iterations()):
        distances = maze.flood(7, 7)  # Assuming the target cell is at (7, 7)
    end_time = millis()
    t = end_time - start_time
    maze.print_maze()
    print("Flood distance correct: ", maze.cost[0][0] == 20)
    print(f"{sys.implementation.name} - maze_ph: Execution Time for {iterations()} iterations: {t:} milliseconds")
