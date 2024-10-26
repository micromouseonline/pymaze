# a place for most of the custom classes that are used


import array
import sys
import time


def millis():
    if sys.implementation.name == 'micropython':
        # MicroPython
        return time.ticks_ms()
    else:
        # Desktop Python
        return int(round(time.time() * 1000))


def iterations():
    if sys.implementation.name == 'micropython':
        return 1
    else:
        return 1000


MAZE_SIZE = 16
MAZE_CELL_COUNT = MAZE_SIZE*MAZE_SIZE
MAX_COST = MAZE_CELL_COUNT

WALL_ABSENT = 0
WALL_PRESENT = 1
WALL_UNKNOWN = 2
WALL_VIRTUAL = 3
WALL_MASK = 3

ALL_UNKNOWN = 0b10101010

CLOSED_MAZE_MASK = 3
OPEN_MAZE_MASK = 1


VIEW_PLAIN = 0
VIEW_COSTS = 1
VIEW_DIRS = 2


"""
 * Directions are absolute and are not relative to any particular heading
"""
DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_COUNT = 4
DIR_BLOCKED = -1


"""
 * Heading represents the direction that the robot is facing. 
 * For example, a robot is facing east when heading is HDG_EAST
"""
HDG_NORTH = 0
HDG_EAST = 1
HDG_SOUTH = 2
HDG_WEST = 3
HDG_COUNT = 4
HDG_BLOCKED = -1


def right_from(heading: int) -> int:
    return ((heading + 1) % HDG_COUNT)


def left_from(heading: int) -> int:
    return ((heading + HDG_COUNT - 1) % HDG_COUNT)


def ahead_from(heading: int) -> int:
    return heading


def behind_from(heading: int) -> int:
    return ((heading + 2) % HDG_COUNT)

