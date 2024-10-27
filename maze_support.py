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

MOVE_AHEAD = 0
MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_BACK = 3
MOVE_COUNT = 4

def move_from_heading_change(heading_now, heading_next):
    if heading_next == heading_now:
        return MOVE_AHEAD
    elif heading_next == left_from(heading_now):
        return MOVE_LEFT
    elif heading_next == right_from(heading_now):
        return MOVE_RIGHT
    else:
        return MOVE_BACK

def right_from(heading: int) -> int:
    return ((heading + 1) % HDG_COUNT)


def left_from(heading: int) -> int:
    return ((heading + HDG_COUNT - 1) % HDG_COUNT)


def ahead_from(heading: int) -> int:
    return heading


def behind_from(heading: int) -> int:
    return ((heading + 2) % HDG_COUNT)

if __name__ == "__main__":
    print("test headings:")
    heading_name = {HDG_NORTH : 'NORTH', HDG_SOUTH : 'SOUTH', HDG_WEST : 'WEST', HDG_EAST : 'EAST'}
    move_name = {MOVE_AHEAD : 'AHEAD', MOVE_LEFT : 'LEFT', MOVE_RIGHT : 'RIGHT', MOVE_BACK : 'BACK'}
    line = f"         "
    for hdg in range(HDG_COUNT):
        line += f"{heading_name[hdg]:8}"
    print(line)

    for now in range(HDG_COUNT):
        line = f"{heading_name[now]:8} "
        for next in range(HDG_COUNT):
            line += f"{move_name[move_from_heading_change(now, next)]:8}"

        print(line)