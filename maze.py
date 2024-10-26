"""
maze.py
"""

import time
from maze_support import *
from maze_files import *
import os
import sys


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
        self.cost = [None for _ in range(self.size * self.size)]
        self.walls = [ALL_UNKNOWN for _ in range(self.size * self.size)]
        self.mask = OPEN_MAZE_MASK

    def __str__(self) -> str:
        return self.get_maze_str(VIEW_PLAIN)

    # TODO: add a __repr__ method that will prodiuce a Python declaration?

    def cell_id(self, x, y):
        return y + x * self.size

    def cell_xy(self, cell):
        return (cell // self.size, cell % self.size)

    def init_walls(self):
        """
        Initialise the maze walls to all unknown
        Set the borders as walls
        Mark the start cell walls
        Does not set the goal area
        """
        self.walls = [ALL_UNKNOWN for _ in range(self.size * self.size)]
        for cell in range(16):
            maze.set_wall(self.cell_id(cell, 0), DIR_SOUTH, WALL_PRESENT)
            maze.set_wall(self.cell_id(cell, 15), DIR_NORTH, WALL_PRESENT)
            maze.set_wall(self.cell_id(0, cell), DIR_WEST,  WALL_PRESENT)
            maze.set_wall(self.cell_id(15, cell), DIR_EAST, WALL_PRESENT)
        maze.set_wall(0, DIR_EAST, WALL_PRESENT)
        maze.set_wall(0, DIR_NORTH, WALL_ABSENT)

    def init_walls_from_string(self, lines):
        ROW_DIVISOR = 2
        COL_DIVISOR = 4
        self.size = max(len(lines) // ROW_DIVISOR,
                        len(lines[0]) // COL_DIVISOR)
        self.walls = [ALL_UNKNOWN for _ in range(self.size * self.size)]
        cell_y = self.size - 1
        for i, line in enumerate(lines):
            if i >= ROW_DIVISOR * self.size:
                continue
            line = line.rstrip()  # remove \n
            if i % ROW_DIVISOR == 0:  # north walls
                for cell_x, c in enumerate(line[2::COL_DIVISOR]):
                    wall_state = WALL_PRESENT if c == '-' else WALL_ABSENT
                    self.update_wall(self.cell_id(
                        cell_x, cell_y), DIR_NORTH, wall_state)
            else:  # west walls
                wall_chars = line[0::COL_DIVISOR][:-1]
                for x, c in enumerate(wall_chars):
                    wall_state = WALL_PRESENT if c == '|' else WALL_ABSENT
                    self.update_wall(self.cell_id(x, cell_y),
                                     DIR_WEST, wall_state)
                # special case for the last character
                wall_state = WALL_PRESENT if line[-1] == '|' else WALL_ABSENT
                self.update_wall(self.cell_id(
                    self.size - 1, cell_y), DIR_EAST, wall_state)
            cell_y -= i % ROW_DIVISOR

        # special case for the last line
        cell_y = 0
        for cell_x, c in enumerate(line[2::COL_DIVISOR]):
            wall_state = WALL_PRESENT if c == '-' else WALL_ABSENT
            self.set_wall(self.cell_id(cell_x, cell_y), DIR_SOUTH, wall_state)
        return

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
        It will ensure that wall state can only be changed once.
        If you absolutely, positively have to set the wall state, use set_wall.
        """
        this_wall = (self.walls[cell] >> direction * 2) & WALL_MASK
        if this_wall != WALL_UNKNOWN:
            return
        self.set_wall(cell, direction, state)

    def set_mask(self, mask):
        """
        The mask determines the view of the maze
        The default is OPEN_MAZE_MASK which assumes unknown walls are absent
        The CLOSED_MAZE_MASK assumes unknown walls are present

        By using these two masks, you can view the maze as 'open' or 'closed'
        Flood using the 'open' view while exploring to find a way to the goal
        Flood using the 'closed' view to find a guaranteed safe route to the goal
        """
        self.mask = mask

    def cell_has_wall(self, cell, direction):
        """
        Returns True if there is a wall in the given cell and direction
        Uses the current mask to to view the maze as 'closed' or 'open'
        The 'closed' maze assumes unknown walls are present
        The 'open' maze assumes unknown walls are absent
        TODO: This method may be redundant
        """
        wall = self.walls[cell] >> direction * 2
        return wall & self.mask == WALL_PRESENT

    def cell_has_exit(self, cell, direction):
        """
        Returns True if there is an exit in the given cell and direction
        Uses the current mask to to view the maze as 'closed' or 'open'
        The 'closed' maze assumes unknown walls are present
        The 'open' maze assumes unknown walls are absent
        """
        wall = self.walls[cell] >> direction * 2
        return wall & self.mask == WALL_ABSENT

    def neighbour(self, cell, direction):
        """
        Calculate and return the offset of a neighbouring cell.
        The maze is assumed to be square and the returned value will
        wrap around the edges of the maze
        There is no error checking for the direction
        """
        neighbour = cell
        if direction == DIR_NORTH:
            neighbour = cell + 1
        elif direction == DIR_EAST:
            neighbour = cell + self.size
        elif direction == DIR_SOUTH:
            neighbour = cell + self.size*self.size - 1
        elif direction == DIR_WEST:
            neighbour = cell + self.size * self.size - self.size
        return neighbour % (self.size * self.size)

    def get_maze_str(self, view=VIEW_PLAIN, mask=OPEN_MAZE_MASK):
        """
        Print a visual representation of the maze
        If view == VIEW_COSTS, print the cost of each cell
        """
        old_mask = self.mask
        self.mask = mask
        str = ""
        for y in range(self.size - 1, -1, -1):
            line = "+"
            for x in range(self.size):
                if self.cell_has_exit(self.cell_id(x, y), DIR_NORTH):
                    line += "   +"
                else:
                    line += "---+"
            str += line + "\n"
            line = ""
            for x in range(self.size):
                cell = self.cell_id(x, y)
                if self.cell_has_exit(cell, DIR_WEST):
                    line += " "
                else:
                    line += "|"
                # now the cell space
                if cell == 0 and view == VIEW_PLAIN:
                    line += " S "
                elif view == VIEW_COSTS and self.cost[cell] is not None:
                    line += f"{self.cost[cell]:>3}"
                else:
                    line += "   "
            if self.cell_has_exit(self.cell_id(self.size-1, y), DIR_EAST):
                line += " "
            else:
                line += "|"  # Rightmost boundary
            str += line + "\n"
        line = "+"
        for x in range(self.size):
            if self.cell_has_exit(self.cell_id(x, 0), DIR_SOUTH):
                line += "   +"
            else:
                line += "---+"
        # print(line)
        str += line + "\n"
        self.mask = old_mask
        return str

    def flood(self, target_cell):
        """
        While exploring, the 'open' view should be used to find exits. This is  
        accomplished by adding a class variable which is used to set the mask used when 
        examining maze walls.

        The 'closed' view should be used to find the shortest path.

        For better performance, the flood method makes use of the intimate knowledge it has
        about the maze. 

        For example, calculating the neighbor does not use the built-in method because it
        is expensive and too general purpose. Instead, a short, inline version is used which
        relies ion the maze edges having known walls.

        This is not ideal in terms of maintenance but speed is king.
        """
        MASK = WALL_MASK & self.mask
        NORTH_MASK = MASK << DIR_NORTH * 2
        EAST_MASK = MASK << DIR_EAST * 2
        SOUTH_MASK = MASK << DIR_SOUTH * 2
        WEST_MASK = MASK << DIR_WEST * 2

        self.cost = [None for _ in range(self.size * self.size)]
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
                if self.cost[neighbour] == None:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & EAST_MASK == 0:
                neighbour = here + 16
                if self.cost[neighbour] == None:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & SOUTH_MASK == 0:
                neighbour = here - 1
                if self.cost[neighbour] == None:
                    self.cost[neighbour] = self.cost[here] + 1
                    queue[tail] = neighbour
                    tail += 1

            if walls_here & WEST_MASK == 0:
                neighbour = here - 16
                if self.cost[neighbour] == None:
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

    maze.init_walls()
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

    maze.get_maze_str()

    # exit()
    start_time = millis()
    target = maze.cell_id(7, 7)
    for _ in range(iterations()):
        distances = maze.flood(target)
    end_time = millis()
    t = end_time - start_time
    maze_str = maze.get_maze_str(VIEW_COSTS, OPEN_MAZE_MASK)
    print(maze_str)
    print("Flood distance correct: ", maze.cost[0] == 20)
    print(f"{sys.implementation.name} - maze: Execution Time for {iterations()} iterations: {t:} milliseconds")

    # maze.init_walls_from_string(all_japan_2007)
    # maze.flood(target)
    # maze_str = maze.get_maze_str(VIEW_COSTS, OPEN_MAZE_MASK)
    # print(maze)
