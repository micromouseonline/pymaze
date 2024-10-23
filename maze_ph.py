"""
maze-ph.py
A simple, naive implementation of the maze and manhattan flood algorithm
The code is mostly developed from suggestions by copilot
"""

import time
from maze_support import *
import os
import sys


class Maze:

    def __init__(self, size=16):
        self.size = size
        self.cost = [[None for _ in range(
            self.size)] for _ in range(self.size)]
        self.walls = {
            (row, col): {"N": WALL_UNKNOWN, "E": WALL_UNKNOWN, "S": WALL_UNKNOWN, "W": WALL_UNKNOWN}
            for row in range(size)
            for col in range(size)
        }

    def clear_walls(self):
        self.walls = {
            (row, col): {"N": WALL_UNKNOWN, "E": WALL_UNKNOWN, "S": WALL_UNKNOWN, "W": WALL_UNKNOWN}
            for row in range(self.size)
            for col in range(self.size)
        }
        for cell in range(16):
            maze.set_wall(cell, 0, "S", WALL_PRESENT)
            maze.set_wall(cell, 15, "N", WALL_PRESENT)
            maze.set_wall(0, cell, "W",  WALL_PRESENT)
            maze.set_wall(15, cell, "E", WALL_PRESENT)

    def set_wall(self, col, row, direction, state):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            self.walls[(col, row)][direction] = state
            # Add wall on the opposite side for the neighboring cell
            if direction == "N" and row < self.size - 1:
                self.walls[(col, row + 1)]["S"] = state
            elif direction == "E" and col < self.size - 1:
                self.walls[(col + 1, row)]["W"] = state
            elif direction == "S" and row > 0:
                self.walls[(col, row - 1)]["N"] = state
            elif direction == "W" and col > 0:
                self.walls[(col - 1, row)]["E"] = state

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
                if self.get_wall(col, row, "N") == WALL_PRESENT:
                    line += "---+"
                else:
                    line += "   +"
            print(line)
            line = ""
            for col in range(self.size):
                if self.get_wall(col, row, "W") == WALL_PRESENT:
                    line += "|"
                else:
                    line += " "
                if self.cost[row][col] is not None:
                    line += f"{self.cost[col][row]:>3}"
                else:
                    line += "   "
            if self.get_wall(15, row, "E") == WALL_PRESENT:
                line += "|"  # Rightmost boundary
            else:
                line += " "
            print(line)
        line = "+"
        for col in range(self.size):
            if self.get_wall(col, 0, "S") == WALL_PRESENT:
                line += "---+"
            else:
                line += "   +"
        print(line)

    def flood(self, target_col, target_row):
        self.cost = [[MAX_COST for _ in range(
            self.size)] for _ in range(self.size)]
        QUEUE_LENGTH = 64
        queue = [None] * QUEUE_LENGTH
        tail = 0
        head = 0
        queue[tail] = (target_col, target_row, 0)
        tail += 1
        while head != tail:
            x, y, dist = queue[head]
            head += 1
            dist = dist + 1
            if (head >= QUEUE_LENGTH):
                head = 0
            if not self.has_wall(x, y, "N") and self.cost[x][y+1] == MAX_COST:
                queue[tail] = (x, y + 1, dist)
                self.cost[x][y+1] = dist
                tail += 1
                if (tail >= QUEUE_LENGTH):
                    tail = 0
            if not self.has_wall(x, y, "E") and self.cost[x + 1][y] == MAX_COST:
                self.cost[x + 1][y] = dist
                queue[tail] = (x + 1, y, dist)
                tail += 1
                if (tail >= QUEUE_LENGTH):
                    tail = 0
            if not self.has_wall(x, y, "S") and self.cost[x][y - 1] == MAX_COST:
                self.cost[x][y - 1] = dist
                queue[tail] = (x, y - 1, dist)
                tail += 1
                if (tail >= QUEUE_LENGTH):
                    tail = 0
            if not self.has_wall(x, y, "W") and self.cost[x - 1][y] == MAX_COST:
                self.cost[x - 1][y] = dist
                queue[tail] = (x - 1, y, dist)
                tail += 1
                if (tail >= QUEUE_LENGTH):
                    tail = 0

        return self.cost


if __name__ == "__main__":
    # Example usage
    maze = Maze()

    maze.clear_walls()
    maze.set_wall(7, 7, "W", WALL_PRESENT)
    maze.set_wall(7, 7, "S", WALL_PRESENT)
    maze.set_wall(8, 7, "S", WALL_PRESENT)
    maze.set_wall(8, 7, "E", WALL_PRESENT)
    maze.set_wall(8, 8, "E", WALL_ABSENT)
    maze.set_wall(8, 8, "N", WALL_PRESENT)
    maze.set_wall(7, 8, "N", WALL_PRESENT)
    maze.set_wall(7, 8, "W", WALL_PRESENT)
    # check that a closed off area does not get flooded
    maze.set_wall(4, 4, "N", WALL_PRESENT)
    maze.set_wall(4, 4, "E", WALL_PRESENT)
    maze.set_wall(4, 4, "S", WALL_PRESENT)
    maze.set_wall(4, 4, "W", WALL_PRESENT)

    maze.print_maze()

    start_time = millis()
    for _ in range(iterations()):
        distances = maze.flood(7, 7)  # Assuming the target cell is at (7, 7)
    end_time = millis()
    t = end_time - start_time
    maze.print_maze()
    print("Flood distance correct: ", maze.cost[0][0] == 20)
    print(f"{sys.implementation.name} - maze_ph: Execution Time for {iterations()} iterations: {t:} milliseconds")
