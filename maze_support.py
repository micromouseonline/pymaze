# a place for most of the custom classes that are used


import array
import sys
import time

###############################################
# a couple of convenience functions for testing


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

###############################################


# The following are all more relevant to the mouse
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
