"""
 Here can go tests for the maze implementations
"""
import sys

import time
from maze_support import *
from maze import *


def iterations():
    if sys.implementation.name == 'micropython':
        return 100
    else:
        return 10000


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
    maze = Maze()
    print("This system is running {}".format(sys.implementation.name))
    print("start...")
    test_wall_states()
