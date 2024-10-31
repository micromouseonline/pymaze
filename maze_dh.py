# maze_dh.py
# Maze code for MicroPython
# Copyright (c) 2024 David Hannaford
# Contributions from Peter Harrison and Paul Busby
# Released under the MIT License (https://opensource.org/licenses/MIT)

# Example flood routines and example of use

# These items in capitals are constants used in the routines.
# Add these after any include statements at the start of your program
WIDTH = 16  # is 16 in full size maze
HEIGHT = 16  # is 16 in full size maze
TABLEWIDTH = 16
TABLEHEIGHT = 16
START = 0  # the start cell number
# int((TABLEWIDTH * HEIGHT /2) + (WIDTH / 2)) # middle of full size maze
MIDDLE = 135   # middle cell number of a standard full size maze
NORTH = 1      # bit value set when there is a wall on the North side of the cell
EAST = 2       # bit value set when there is a wall on the North side of the cell
SOUTH = 4      # bit value set when there is a wall on the North side of the cell
WEST = 8       # bit value set when there is a wall on the North side of the cell
VISITED = 16   # bit value set when the mouse has entered a cell
numcells = TABLEWIDTH * (TABLEHEIGHT + 1)
floodfail = 0  # global flag that is sset if teh flood routine is unable to find a coplete route
# set up and initialise lists for walls and flood values in maze

walls = [0] * numcells  # list of cell wall items initialised to zero starting at cell 0
# walls[0] = 30   example of setting an indexed value for all walls in cell zero
# walls[16} = walls[16] | EAST   example of adding an East wall to cell 16
# To check bits in the walls byte to check if a wall is previously recorded as present
# use walls[n] & NORTH to check the north wall bit, or walls[n] & EAST for the EAST bit etc

maze = [0] * numcells  # list that holds flood values for maze cells
# wall and maze cells are numbered from left to right then upwards from start cell as zero


proclist = [0] * numcells  # This holds the list of cells to be processed next by the flood routine

# Call this routine to fill the flood table with high values prior to doing the flood


def floodclear():  # clear the flood table
    global maze
    for x in range(256):
        maze[x] = numcells

# This routine does a Manhatten flood from the start cell to the finish cell
# On the explore out, flood from MIDDLE To START On the way beck to the start, flood from START to MIDDLE


def floodmaze(strt, fin):   # flood the maze from the strt cell to the fin cell
    global maze, walls, floodfail, numcells
    floodclear()                    # clear the flood table to all 283
    flooded = 0                     # set flag to not finished flooding yet
    floodfail = 0                   # flag to show if flood failed to complete to end point
    curr = strt                     # current cell being processed
    floodval = 0
    maze[strt] = 1                  # set start cell flood value to one
    n = 0                           # index for end of processing list of cells
    nxt = 0                         # pointer to the first unprocessed item on the list
    while (flooded == 0):
        fval = maze[curr]           # get current value of current cell
        if ((walls[curr] & SOUTH) == 0):     # is there a gap to the SOUTH of current cell
            if (maze[curr - TABLEWIDTH] == numcells):
                maze[curr - TABLEWIDTH] = fval + 1  # set flood value in this cell
                proclist[n] = curr-TABLEWIDTH       # save flood cell for future processing
                n = n + 1                           # update processing list number
                if (proclist[n-1] == fin):          # check if finished flooding
                    flooded = 1                     # set flag to stop loop

        if ((walls[curr] & EAST) == 0):      # is there a gap to the EAST of current cell
            if (maze[curr + 1] == numcells):
                maze[curr + 1] = fval + 1           # set flood value in this cell
                proclist[n] = curr + 1              # save flood cell for future processing
                n = n + 1                           # update processing list number
                if (proclist[n-1] == fin):          # check if finished flooding
                    flooded = 1                     # set flag to stop loop

        if ((walls[curr] & NORTH) == 0):     # is there a gap to the NORTH of current cell
            if (maze[curr + TABLEWIDTH] == numcells):
                maze[curr + TABLEWIDTH] = fval + 1  # set flood value in this cell
                proclist[n] = curr + TABLEWIDTH     # save flood cell for future processing
                n = n + 1                           # update processing list number
                if (proclist[n-1] == fin):          # check if finished flooding
                    flooded = 1                     # set flag to stop loop

        if ((walls[curr] & WEST) == 0):      # is there a gap to the WEST of current cell
            if (maze[curr - 1] == numcells):
                maze[curr - 1] = fval + 1           # set flood value in this cell
                proclist[n] = curr - 1              # save flood cell for future processing
                n = n + 1                           # update processing list number
                if (proclist[n-1] == fin):          # check if finished flooding
                    flooded = 1                     # set flag to stop loop

        # get the location of the next cell to process
        curr = proclist[nxt]
        nxt = nxt + 1       # point to next item to process on the list
        if (nxt > n):       # check if flood unable to continue as no more cells accessible
            floodfail = 1   # set flood failure status flag
            flooded = 1     # stop  the flooding loo

    return

# this routine sets up the outside walls for the maze. Use it once at tha start of the program


def setoutsidewalls():
    for x in range(WIDTH):    # does range 0 to 15 when WIDTH = 16
        y = TABLEWIDTH * (HEIGHT - 1) + x
        walls[y] = walls[y] | NORTH    # set top (NORTH) walls
        walls[x] = walls[x] | SOUTH    # set bottom (SOUTH) walls
    for x in range(HEIGHT):
        y = (x * TABLEHEIGHT) + WIDTH - 1
        walls[y] = walls[y] | EAST     # set right (EAST) walls
        y = x * TABLEWIDTH
        walls[y] = walls[y] | WEST     # set left (WEST) walls
    # set wall to east of start cell
    walls[0] = walls[0] | EAST
    walls[1] = walls[1] | WEST
    walls[0] = walls[0] | VISITED

# This routine sets left, right or front walls in the walls table when seen at the start of the cell boundary
# It also sets the corresponding wall in the adjacent cell
# Call it after detecting if the walls the mouse is seeing in the cell are PRESENT or NOT PRESENT and
#   setting these values in fields leftwall, rightwall and frontwall


def setwalls():
    # sets left, right and front walls seen when at start of cell boundary
    global leftwall, rightwall, frontwall, heading, currentcell
    if (heading == NORTH):
        if (leftwall == PRESENT):
            walls[currentcell] = walls[currentcell] | WEST         # record left wall
            if (currentcell > 0):
                # record right wall in cell to left of current cell
                walls[currentcell - 1] = walls[currentcell - 1] | EAST
        if (rightwall == PRESENT):
            walls[currentcell] = walls[currentcell] | EAST         # record right wall
            walls[currentcell + 1] = walls[currentcell + 1] | WEST  # record left wall in cell to right of current cell
        if (frontwall == PRESENT):
            walls[currentcell] = walls[currentcell] | NORTH         # record front wall
            if (currentcell < (TABLEWIDTH * (TABLEHEIGHT - 1))):
                walls[currentcell + TABLEWIDTH] = walls[currentcell + TABLEWIDTH] | SOUTH
    if (heading == SOUTH):
        if (leftwall == PRESENT):
            walls[currentcell] = walls[currentcell] | EAST         # record left wall
            walls[currentcell + 1] = walls[currentcell + 1] | WEST  # record right wall in cell to left of current cell
        if (rightwall == PRESENT):
            walls[currentcell] = walls[currentcell] | WEST         # record right wall
            walls[currentcell - 1] = walls[currentcell - 1] | EAST  # record left wall in cell to right of current cell
        if (frontwall == PRESENT):
            walls[currentcell] = walls[currentcell] | SOUTH         # record front wall
            if (currentcell > TABLEWIDTH):
                walls[currentcell - TABLEWIDTH] = walls[currentcell - TABLEWIDTH] | NORTH
    if (heading == EAST):
        if (leftwall == PRESENT):
            # print (currentcell)
            walls[currentcell] = walls[currentcell] | NORTH         # record left wall
            # record right wall in cell to left of current cell
            walls[currentcell + TABLEWIDTH] = walls[currentcell + TABLEWIDTH] | SOUTH
        if (rightwall == PRESENT):
            walls[currentcell] = walls[currentcell] | SOUTH         # record right wall
            if (currentcell >= TABLEWIDTH):
                # record left wall in cell to right of current cell
                walls[currentcell - TABLEWIDTH] = walls[currentcell - TABLEWIDTH] | NORTH
        if (frontwall == PRESENT):
            walls[currentcell] = walls[currentcell] | EAST         # record front wall
            walls[currentcell + 1] = walls[currentcell + 1] | WEST
    if (heading == WEST):
        if (leftwall == PRESENT):
            # print (currentcell)
            walls[currentcell] = walls[currentcell] | SOUTH         # record left wall
            if (currentcell >= 0):
                # record right wall in cell to left of current cell
                walls[currentcell - TABLEWIDTH] = walls[currentcell - TABLEWIDTH] | NORTH
        if (rightwall == PRESENT):
            walls[currentcell] = walls[currentcell] | NORTH         # record right wall
            # record left wall in cell to right of current cell
            walls[currentcell + TABLEWIDTH] = walls[currentcell + TABLEWIDTH] | SOUTH
        if (frontwall == PRESENT):
            walls[currentcell] = walls[currentcell] | WEST         # record front wall
            walls[currentcell - 1] = walls[currentcell - 1] | EAST
    walls[currentcell] = walls[currentcell] | VISITED         # mark cell as visited after putting in the walls seen

# This routine prints out the flood table - use it for diagnostic purposes


def showflood():
    y = HEIGHT - 1
    print("Flood Table")
    # all the north walls
    while y >= 0:                   # work down from the top
        line = '    '
        for x in range(WIDTH):
            line += 'o---' if walls[y * WIDTH + x] & NORTH else 'o   '
        line = line + 'o'
        print(line)
        line = f'{y:>2}  '  # the row number
        for x in range(WIDTH):
            line += '|' if walls[y * WIDTH + x] & WEST else ' '
            line += f'{maze[y * WIDTH + x]:>3}'
        line = line + '|' if walls[y * WIDTH + x] & EAST else ' '
        print(line)
        y = y - 1
    line = '    '
    for x in range(WIDTH):
        line += 'o---' if walls[0 * WIDTH + x] & SOUTH else 'o   '
    line = line + 'o'
    print(line)
    line = '     '
    for x in range(WIDTH):
        line += f'{x:>3} '  # the column number
    print(line)
    print()


# This routine prints out the maze walls table - use it for diagnostic purposes
def showwalls():
    y = HEIGHT - 1
    print("Maze walls")
    # all the north walls
    while y >= 0:                   # work down from the top
        line = '    '
        for x in range(WIDTH):
            line += 'o---' if walls[y * WIDTH + x] & NORTH else 'o   '
        line = line + 'o'
        print(line)
        line = f'{y:>2}  '  # the row number
        for x in range(WIDTH):
            line += '|   ' if walls[y * WIDTH + x] & WEST else '    '
        line = line + '|' if walls[y * WIDTH + x] & EAST else ' '
        print(line)
        y = y - 1
    line = '    '
    for x in range(WIDTH):
        line += 'o---' if walls[0 * WIDTH + x] & SOUTH else 'o   '
    line = line + 'o'
    print(line)
    line = '     '
    for x in range(WIDTH):
        line += f'{x:>3} '  # the column number
    print(line)
    print()


# ********************************************************************************
# example usage
setoutsidewalls()
floodclear()
floodmaze(MIDDLE, START)
# these two statements will print out the flood table and the walls table
showflood()
showwalls()
