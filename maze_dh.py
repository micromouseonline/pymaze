import os
import sys

from  maze_support import *



cost = [0]*MAZE_CELL_COUNT
walls = [0]*MAZE_CELL_COUNT
proclist = [0]*MAZE_CELL_COUNT

floodfail = 0
debug = 0

def cell_id(x,y):
    return y + x * MAZE_SIZE

def cell_xy(cell):
    return (cell // 16, cell % 16)

def add_wall(cell, heading):
    x,y = cell_xy(cell)
    if (heading == DIR_NORTH):
        walls[cell] |= NORTH_WALL
        if y < 15:
            walls[cell+1] |= SOUTH_WALL
    elif (heading == DIR_EAST):
        walls[cell] |= EAST_WALL
        if x < 15:
            walls[cell+16] |= WEST_WALL
    elif (heading == DIR_SOUTH):
        walls[cell] |= SOUTH_WALL
        if y > 0:
            walls[cell-1] |= NORTH_WALL
    elif (heading == DIR_WEST):
        walls[cell] |= WEST_WALL
        if x > 0:
            walls[cell-16] |= EAST_WALL

def get_walls(x,y):
    return walls[cell_id(x,y)]

def get_cost(x,y):
    return cost[cell_id(x,y)]

def maze_clear():
  walls = [0]*MAZE_CELL_COUNT
  for x in range(16):
      add_wall(cell_id(x,0), DIR_SOUTH)
      add_wall(cell_id(x,15), DIR_NORTH)
      add_wall(cell_id(0,x), DIR_WEST)
      add_wall(cell_id(15,x), DIR_EAST)

def showmaze(): # show the maze
   
  for y in range(15, -1, -1):
      # Print the north walls and top boundary
      line = "+"
      for x in range(16):
          if get_walls(x,y) & NORTH_WALL:
              line += "---+"
          else:
              line += "   +"
      print(line)
      # Print the west walls and cell boundary
      line = ""
      for x in range(16):
          if get_walls(x,y) & WEST_WALL:
              line += "|"
          else:
              line += " "
          if get_cost(x,y) is not None:
              line += f"{get_cost(x,y):>3}"
          else:
              line += "   "
      if get_walls(15,y) & EAST_WALL: 
          line += "|"  # Rightmost boundary
      else:
          line += " " 
      print(line)

    # Print the bottom boundary
  line = "+"
  for x in range(16):
      if get_walls(x,y) & SOUTH_WALL:
          line += "---+"
      else:
          line += "   +"
  print(line)

def floodmaze(strt,fin):   # flood the maze from the strt cell to the fin cell
   global cost, walls, floodfail, debug
   flooded = 0            # set flag to not finished flooding yet
   floodfail = 0          # flag to show if flood failed to complete to end point
   curr = strt            # current cell being processed
   floodval = 0
   cost = [MAX_COST]*MAZE_CELL_COUNT
   cost[strt] = 0         # set start cell flood value to one
   n = 0                  # index for processing list array of cells to say where to add to end of list
   nxt = 0                # pointer to the first unprocessed item on the list
   while (flooded == 0):
       fval = cost[curr]  # get current value of current cell
       if ((walls[curr] & SOUTH_WALL) == 0):     # is there a gap to the SOUTH of current cell
           if ((cost[curr - 1] == 256)):
               cost[curr - 1] = fval + 1    # set flood value in this cell
               proclist[n] = curr-1         # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):       # check if finished flooding
                   flooded = 1                  # set flag to stop loop
       if ((walls[curr] & EAST_WALL) == 0):      # is there a gap to the EAST of current cell
           if ((cost[curr + MAZE_SIZE] == 256)):
               cost[curr + MAZE_SIZE] = fval + 1        # set flood value in this cell
               proclist[n] = curr + MAZE_SIZE           # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):           # check if finished flooding
                   flooded = 1                      # set flag to stop loop
       if ((walls[curr] & NORTH_WALL) == 0):     # is there a gap to the NORTH of current cell
           if ((cost[curr + 1] == 256) ):
               cost[curr + 1] = fval + 1    # set flood value in this cell
               proclist[n] = curr + 1       # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):           # check if finished flooding
                      flooded = 1                      # set flag to stop loop
       if ((walls[curr] & WEST_WALL) == 0):      # is there a gap to the WEST of current cell
           if ((cost[curr - MAZE_SIZE] == 256)):
               cost[curr - MAZE_SIZE] = fval + 1        # set flood value in this cell
               proclist[n] = curr - MAZE_SIZE           # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):       # check if finished flooding
                   flooded = 1                  # set flag to stop loop
       curr = proclist[nxt]                 # get the location of the next cell to process
       nxt = nxt + 1                        # point to next item to process on the list
       if (nxt > n):                        # check if flood unable to continue as no more cells accessible
           floodfail = 1                     # set flood failure status flag
           flooded = 1 # stop  the flooding loop
           if (debug == 1):
               print (strt, fin, nxt, n, proclist)


maze_clear()
add_wall(cell_id(0, 0),DIR_EAST)
add_wall(cell_id(7, 7),DIR_WEST)
add_wall(cell_id(7, 7),DIR_SOUTH)
add_wall(cell_id(8, 7),DIR_SOUTH)
add_wall(cell_id(8, 7),DIR_EAST)
add_wall(cell_id(8, 8),DIR_NORTH)
add_wall(cell_id(7, 8),DIR_NORTH)
add_wall(cell_id(7, 8),DIR_WEST)
add_wall(cell_id(4, 4),DIR_NORTH)
add_wall(cell_id(4, 4),DIR_EAST)
add_wall(cell_id(4, 4),DIR_SOUTH)
add_wall(cell_id(4, 4),DIR_WEST)

start_time = millis()
for _ in range(iterations()):
  floodmaze(cell_id(7,7),cell_id(0,0))
  
end_time = millis()
t = end_time - start_time
showmaze()
print("Flood distance correct: ",get_cost(0,0) == 20)
print(f"{sys.implementation.name} - maze_dh: Execution Time for {iterations()} iterations: {t:} milliseconds")
