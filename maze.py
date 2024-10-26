"""
maze.py
"""

import time
from maze_support import *
import os
import sys


class Maze:

    def __init__(self, size=16):
        self.size = size
        self.cost = [MAX_COST for _ in range(self.size * self.size)]
        self.walls = [ALL_UNKNOWN for _ in range(self.size * self.size)]
        self.mask = OPEN_MAZE_MASK

    def cell_id(self, x, y):
        return y + x * self.size

    def cell_xy(self, cell):
        return (cell // self.size, cell % self.size)

    def clear_walls(self):
        self.walls = [ALL_UNKNOWN for _ in range(self.size * self.size)]
        for cell in range(16):
            maze.set_wall(self.cell_id(cell, 0), DIR_SOUTH, WALL_PRESENT)
            maze.set_wall(self.cell_id(cell, 15), DIR_NORTH, WALL_PRESENT)
            maze.set_wall(self.cell_id(0, cell), DIR_WEST,  WALL_PRESENT)
            maze.set_wall(self.cell_id(15, cell), DIR_EAST, WALL_PRESENT)
        maze.set_wall(0, DIR_EAST, WALL_PRESENT)
        maze.set_wall(0, DIR_NORTH, WALL_ABSENT)

    def set_wall(self, cell, direction, state):
        """
        Unconditionally set the state of a single wall in the maze
        This would normally only get used when initialising the maze - either
        as a blank maze or when copying a pre-defined maze
        """
        x, y = self.cell_xy(cell)
        wall = state << direction * 2
        mask = ~(WALL_MASK << direction * 2)
        self.walls[cell] &= mask
        self.walls[cell] |= wall
        if direction == DIR_NORTH and y < self.size - 1:
            next = self.neighbour(cell, DIR_NORTH)
            self.walls[next] &= ~(WALL_MASK << DIR_SOUTH * 2)
            self.walls[next] |= (state << DIR_SOUTH * 2)
        elif direction == DIR_EAST and x < self.size - 1:
            next = self.neighbour(cell, DIR_EAST)
            self.walls[next] &= ~(WALL_MASK << DIR_WEST * 2)
            self.walls[next] |= (state << DIR_WEST * 2)
        elif direction == DIR_SOUTH and y > 0:
            next = self.neighbour(cell, DIR_SOUTH)
            self.walls[next] &= ~(WALL_MASK << DIR_NORTH * 2)
            self.walls[next] |= (state << DIR_NORTH * 2)
        elif direction == DIR_WEST and x > 0:
            next = self.neighbour(cell, DIR_WEST)
            self.walls[next] &= ~(WALL_MASK << DIR_EAST * 2)
            self.walls[next] |= (state << DIR_EAST * 2)

    def update_wall(self, cell, direction, state):
        """
        Use this to update the maze while exploring. 
        It will ensure that wal state can only be changed once.
        If you absolutely, positively have to set the wall state, use set_wall.
        """
        this_wall = (self.walls[cell] >> direction * 2) & WALL_MASK
        if this_wall != WALL_UNKNOWN:
            return
        self.set_wall(cell, direction, state)

    def set_mask(self, mask):
        self.mask = mask

    def cell_has_wall(self, cell, direction):
        wall = self.walls[cell] >> direction * 2
        return wall & self.mask == WALL_PRESENT

    def cell_has_exit(self, cell, direction):
        wall = self.walls[cell] >> direction * 2
        return wall & self.mask == WALL_ABSENT

    def neighbour(self, cell, direction):
        if direction == DIR_NORTH:
            return cell + 1
        elif direction == DIR_EAST:
            return cell + self.size
        elif direction == DIR_SOUTH:
            return cell - 1
        elif direction == DIR_WEST:
            return cell - self.size

    def print_maze(self, view=VIEW_PLAIN, mask=OPEN_MAZE_MASK):
        old_mask = self.mask
        self.mask = mask
        for y in range(self.size - 1, -1, -1):
            line = "+"
            for x in range(self.size):
                if self.cell_has_wall(self.cell_id(x, y), DIR_NORTH) == WALL_PRESENT:
                    line += "---+"
                else:
                    line += "   +"
            print(line)
            line = ""
            for x in range(self.size):
                cell = self.cell_id(x, y)
                if self.cell_has_wall(cell, DIR_WEST) == WALL_PRESENT:
                    line += "|"
                else:
                    line += " "
                if view == VIEW_COSTS and self.cost[cell] is not None:
                    line += f"{self.cost[cell]:>3}"
                else:
                    line += "   "
            if self.cell_has_wall(self.cell_id(self.size-1, y), DIR_EAST) == WALL_PRESENT:
                line += "|"  # Rightmost boundary
            else:
                line += " "
            print(line)
        line = "+"
        for x in range(self.size):
            if self.cell_has_wall(self.cell_id(x, 0), DIR_SOUTH) == WALL_PRESENT:
                line += "---+"
            else:
                line += "   +"
        print(line)
        self.mask = old_mask

    def flood(self, target_cell):
        """
        While exploring, the 'open' view should be used to find exits. This is  
        accomplished by adding a class variable which is used to set the mask used when 
        examining maze walls.

        The 'closed' view should be used to find the shortest path.

        For better performance, the flood method makes use of the intimate knowledge it has
        about the maze. This is not ideal in terms of maintentance but speed is king.

        """
        MASK = WALL_MASK & self.mask
        NORTH_MASK = MASK << DIR_NORTH * 2
        EAST_MASK = MASK << DIR_EAST * 2
        SOUTH_MASK = MASK << DIR_SOUTH * 2
        WEST_MASK = MASK << DIR_WEST * 2

        self.cost = [MAX_COST for _ in range(self.size * self.size)]
        self.cost[target_cell] = 0
        head = 0
        tail = 0
        queue = [0 for _ in range(self.size * self.size)]
        queue[tail] = target_cell
        tail += 1
        while head < tail:
            here = queue[head]
            head += 1
            walls_here = self.walls[here]

            if walls_here & NORTH_MASK == 0:
                neighbour = here + 1
                if self.cost[neighbour] == MAX_COST:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & EAST_MASK == 0:
                neighbour = here + 16
                if self.cost[neighbour] == MAX_COST:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & SOUTH_MASK == 0:
                neighbour = here - 1
                if self.cost[neighbour] == MAX_COST:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & WEST_MASK == 0:
                neighbour = here - 16
                if self.cost[neighbour] == MAX_COST:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

        return self.cost[0]


def test_wall_states():
    # check the wall storage method
    walls = maze.walls[maze.cell_id(0, 0)]
    print(f'{walls:08b}')
    print(maze.cell_has_exit(maze.cell_id(0, 0), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(0, 0), DIR_EAST))
    print(maze.cell_has_exit(maze.cell_id(0, 0), DIR_SOUTH))
    print(maze.cell_has_exit(maze.cell_id(0, 0), DIR_WEST))

    maze.set_wall(maze.cell_id(2, 2), DIR_NORTH, WALL_ABSENT)
    maze.set_wall(maze.cell_id(3, 2), DIR_NORTH, WALL_PRESENT)
    maze.set_wall(maze.cell_id(4, 2), DIR_NORTH, WALL_UNKNOWN)
    maze.set_wall(maze.cell_id(5, 2), DIR_NORTH, WALL_VIRTUAL)

    walls = maze.walls[maze.cell_id(2, 2)]
    print(f'{walls:08b}')
    walls = maze.walls[maze.cell_id(3, 2)]
    print(f'{walls:08b}')
    walls = maze.walls[maze.cell_id(4, 2)]
    print(f'{walls:08b}')
    walls = maze.walls[maze.cell_id(5, 2)]
    print(f'{walls:08b}')

    maze.set_mask(CLOSED_MAZE_MASK)
    print("CLOSED VIEW")
    print(f'{maze.mask:08b}')
    print(maze.cell_has_exit(maze.cell_id(2, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(3, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(4, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(5, 2), DIR_NORTH))
    maze.set_mask(OPEN_MAZE_MASK)
    print("OPEN VIEW")
    print(f'{maze.mask:08b}')
    print(maze.cell_has_exit(maze.cell_id(2, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(3, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(4, 2), DIR_NORTH))
    print(maze.cell_has_exit(maze.cell_id(5, 2), DIR_NORTH))


if __name__ == "__main__":
    # Example usage
    maze = Maze()

    maze.clear_walls()
    maze.update_wall(maze.cell_id(7, 7), DIR_WEST, WALL_PRESENT)
    maze.update_wall(maze.cell_id(7, 7), DIR_SOUTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(8, 7), DIR_SOUTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(8, 7), DIR_EAST, WALL_PRESENT)
    maze.update_wall(maze.cell_id(8, 8), DIR_EAST, WALL_ABSENT)
    maze.update_wall(maze.cell_id(8, 8), DIR_NORTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(7, 8), DIR_NORTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(7, 8), DIR_WEST, WALL_PRESENT)
    # check that a closed off area does not get flooded
    maze.update_wall(maze.cell_id(4, 4), DIR_NORTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(4, 4), DIR_EAST, WALL_PRESENT)
    maze.update_wall(maze.cell_id(4, 4), DIR_SOUTH, WALL_PRESENT)
    maze.update_wall(maze.cell_id(4, 4), DIR_WEST, WALL_PRESENT)

    maze.print_maze()

    # exit()
    start_time = millis()
    target = maze.cell_id(7, 7)
    for _ in range(iterations()):
        distances = maze.flood(target)
    end_time = millis()
    t = end_time - start_time
    maze.print_maze(VIEW_COSTS, OPEN_MAZE_MASK)
    maze.print_maze(VIEW_COSTS, CLOSED_MAZE_MASK)
    print("Flood distance correct: ", maze.cost[0] == 20)
    print(f"{sys.implementation.name} - maze: Execution Time for {iterations()} iterations: {t:} milliseconds")
