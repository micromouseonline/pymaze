# Example flood routines and example of use
# import these 2 items if not already imported in your code
import time
# These items in capitals are constants used in the routines
WIDTH = 16  # is 16 in full size maze
HEIGHT = 16  # is 16 in full size maze
TABLEWIDTH = 16
TABLEHEIGHT = 16
START = 0  # the start cell number
# int((TABLEWIDTH * HEIGHT /2) + (WIDTH / 2)) # middle of full size maze
MIDDLE = 135
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
VISITED = 16
numcells = (TABLEWIDTH * (TABLEHEIGHT + 1)) + 10
# set up and initialise lists for walls and flood values in maze
# list of cell items initialised to zero starting at cell 0
walls = [0]*numcells
# walls[0] = 99   example of setting an indexed value
# list that holds flood values for maze cells
maze = [0]*numcells
# cells are numbers from left to right then upwards from start cell as zero
# to check bits in a byte use walls[n] & NORTH to check the north wall bit, walls[n] & EAST for next bit etc
# list that holds the list of cells to be processed next by teh flood routine
proclist = [0]*numcells

# Call this routine to fill the flood table with high values prior to doing the flood


def floodclear():  # clear the flood table
    global maze
    for x in range(256):
        maze[x] = numcells

# This routine does a Manhatten flood form the start cell to the finish cell


def floodmaze(strt, fin):   # flood the maze from the strt cell to the fin cell
    global maze, walls, floodfail, numcells
    floodstart = time.ticks_ms()  # get time now
    floodclear()           # clear the flood table to all 283
    floodcleared = time.ticks_ms()  # get time now
    floodcleared = floodcleared - floodstart
    flooded = 0            # set flag to not finished flooding yet
    floodfail = 0          # flag to show if flood failed to complete to end point
    curr = strt            # current cell being processed
    floodval = 0
    maze[strt] = 1         # set start cell flood value to one
    # index for processing list of cells to say where to add to end of list
    n = 0
    nxt = 0                # pointer to the first unprocessed item on the list
    while (flooded == 0):
        fval = maze[curr]  # get current value of current cell
        if ((walls[curr] & SOUTH) == 0):     # is there a gap to the SOUTH of current cell
            if (maze[curr - TABLEWIDTH] == numcells):
                # set flood value in this cell
                maze[curr - TABLEWIDTH] = fval + 1
                # save flood cell for future processing
                proclist[n] = curr-TABLEWIDTH
                n = n + 1                        # update processing list number
                if (proclist[n-1] == fin):       # check if finished flooding
                    flooded = 1                  # set flag to stop loop
        if ((walls[curr] & EAST) == 0):      # is there a gap to the EAST of current cell
            if (maze[curr + 1] == numcells):
                maze[curr + 1] = fval + 1        # set flood value in this cell
                # save flood cell for future processing
                proclist[n] = curr + 1
                n = n + 1                        # update processing list number
                if (proclist[n-1] == fin):           # check if finished flooding
                    flooded = 1                      # set flag to stop loop
        if ((walls[curr] & NORTH) == 0):     # is there a gap to the NORTH of current cell
            if (maze[curr + TABLEWIDTH] == numcells):
                # set flood value in this cell
                maze[curr + TABLEWIDTH] = fval + 1
                # save flood cell for future processing
                proclist[n] = curr + TABLEWIDTH
                n = n + 1                        # update processing list number
                if (proclist[n-1] == fin):           # check if finished flooding
                    flooded = 1                      # set flag to stop loop
        if ((walls[curr] & WEST) == 0):      # is there a gap to the WEST of current cell
            if (maze[curr - 1] == numcells):
                maze[curr - 1] = fval + 1        # set flood value in this cell
                # save flood cell for future processing
                proclist[n] = curr - 1
                n = n + 1                        # update processing list number
                if (proclist[n-1] == fin):       # check if finished flooding
                    flooded = 1                  # set flag to stop loop

        # get the location of the next cell to process
        curr = proclist[nxt]
        nxt = nxt + 1                        # point to next item to process on the list
        if (nxt > n):                        # check if flood unable to continue as no more cells accessible
            floodfail = 1                     # set flood failure status flag
            flooded = 1  # stop  the flooding loop

    floodend = time.ticks_ms()  # get time now
    floodtime = floodend - floodstart

    return                                    # return

# this routine sets up the outside walls for the maze. Use once at tha start


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

# This routine prints out the flood table - use it for diagnostic purposes


def showflood():
    x = ((HEIGHT-1) * TABLEWIDTH)
    y = HEIGHT - 1
    print("Flood table")
    while (x >= 0):
        if (y < 10):
            space = "  "
        else:
            space = " "
        print(y, space, maze[x], maze[x+1], maze[x+2], maze[x+3], maze[x+4], maze[x+5], maze[x+6], maze[x+7],
              maze[x+8], maze[x+9], maze[x+10], maze[x+11], maze[x+12], maze[x+13], maze[x+14], maze[x+15])
        x = x - TABLEWIDTH
        y = y - 1

# This routine prints out the maze walls table - use it for diagnostic purposes


def showwalls():
    x = ((HEIGHT-1) * TABLEWIDTH)
    y = HEIGHT - 1
    print("Maze walls")
    while (x >= 0):
        if (y < 10):
            space = "  "
        else:
            space = " "
        print(y, space, walls[x], walls[x+1], walls[x+2], walls[x+3], walls[x+4], walls[x+5], walls[x+6], walls[x+7],
              walls[x+8], walls[x+9], walls[x+10], walls[x+11], walls[x+12], walls[x+13], walls[x+14], walls[x+15])
        x = x - TABLEWIDTH
        y = y - 1


# ********************************************************************************
# example usage
setoutsidewalls()
floodclear()
floodmaze(MIDDLE, START)
# these two statements will print out the flood table and the walls table
showflood()
showwalls()
