
import time

TABLEWIDTH = 16
WALL_PRESENT = 0
WALL_ABSENT = 1 
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8

numcells = 256
cost = [0]*numcells
walls = [0]*numcells
proclist = [0]*numcells
floodfail = 0
debug = 0

def cell_id(x,y):
    return y + x * TABLEWIDTH

def cell_xy(cell):
    return (cell // 16, cell % 16)

def add_wall(cell, heading):
    x,y = cell_xy(cell)
    if (heading == NORTH):
        walls[cell] |= NORTH
        if y < 15:
            walls[cell+1] |= SOUTH
    elif (heading == EAST):
        walls[cell] |= EAST
        if x < 15:
            walls[cell+16] |= WEST
    elif (heading == SOUTH):
        walls[cell] |= SOUTH
        if y > 0:
            walls[cell-1] |= NORTH
    elif (heading == WEST):
        walls[cell] |= WEST
        if x > 0:
            walls[cell-16] |= EAST

def get_walls(x,y):
    return walls[cell_id(x,y)]

def get_cost(x,y):
    return cost[cell_id(x,y)]

def maze_clear():
  walls = [0]*256
  for x in range(16):
      add_wall(cell_id(x,0), SOUTH)
      add_wall(cell_id(x,15), NORTH)
      add_wall(cell_id(0,x), WEST)
      add_wall(cell_id(15,x), EAST)

def floodclear(): # clear the flood table
   for x in range(256):
       cost[x] = numcells +1

def showmaze(): # show the maze
   
  for y in range(15, -1, -1):
      # Print the north walls and top boundary
      line = "+"
      for x in range(16):
          if get_walls(x,y) & NORTH:
              line += "---+"
          else:
              line += "   +"
      print(line)
      # Print the west walls and cell boundary
      line = ""
      for x in range(16):
          if get_walls(x,y) & WEST:
              line += "|"
          else:
              line += " "
          if get_cost(x,y) is not None:
              line += f"{get_cost(x,y):>3}"
          else:
              line += "   "
      if get_walls(15,y) & EAST: 
          line += "|"  # Rightmost boundary
      else:
          line += " " 
      print(line)

    # Print the bottom boundary
  line = "+"
  for x in range(16):
      if get_walls(x,y) & SOUTH:
          line += "---+"
      else:
          line += "   +"
  print(line)

def floodmaze(strt,fin):   # flood the maze from the strt cell to the fin cell
   global cost, walls, floodfail, debug
   floodstart = time.time() # get time now
   floodclear()           # clear the flood table to all 283
   floodcleared = time.time() # get time now
   floodcleared = floodcleared - floodstart
   flooded = 0            # set flag to not finished flooding yet
   floodfail = 0          # flag to show if flood failed to complete to end point
   curr = strt            # current cell being processed
   floodval = 0
   cost[strt] = 0         # set start cell flood value to one
   n = 0                  # index for processing list array of cells to say where to add to end of list
   nxt = 0                # pointer to the first unprocessed item on the list
   while (flooded == 0):
       fval = cost[curr]  # get current value of current cell
       if ((walls[curr] & SOUTH) == 0):     # is there a gap to the SOUTH of current cell
           if ((cost[curr - 1] == 0) | ((fval + 1) < cost[curr - 1])):
               cost[curr - 1] = fval + 1    # set flood value in this cell
               proclist[n] = curr-1         # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):       # check if finished flooding
                   flooded = 1                  # set flag to stop loop
       if ((walls[curr] & EAST) == 0):      # is there a gap to the EAST of current cell
           if ((cost[curr + TABLEWIDTH] == 0) | ((fval + 1) < cost[curr + TABLEWIDTH])):
               cost[curr + TABLEWIDTH] = fval + 1        # set flood value in this cell
               proclist[n] = curr + TABLEWIDTH           # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):           # check if finished flooding
                   flooded = 1                      # set flag to stop loop
       if ((walls[curr] & NORTH) == 0):     # is there a gap to the NORTH of current cell
           if ((cost[curr + 1] == 0) | ((fval + 1) < cost[curr + 1])):
               cost[curr + 1] = fval + 1    # set flood value in this cell
               proclist[n] = curr + 1       # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):           # check if finished flooding
                      flooded = 1                      # set flag to stop loop
       if ((walls[curr] & WEST) == 0):      # is there a gap to the WEST of current cell
           if ((cost[curr - TABLEWIDTH] == 0) | ((fval + 1) < cost[curr - TABLEWIDTH])):
               cost[curr - TABLEWIDTH] = fval + 1        # set flood value in this cell
               proclist[n] = curr - TABLEWIDTH           # save flood cell for future processing
               n = n + 1                        # update processing list number
               if (proclist[n-1] == fin):       # check if finished flooding
                   flooded = 1                  # set flag to stop loop
       #print (proclist[n-1] , fin)
        # print (strt, fin, nxt, n, proclist)
       curr = proclist[nxt]                 # get the location of the next cell to process
       nxt = nxt + 1                        # point to next item to process on the list
       if (nxt > n):                        # check if flood unable to continue as no more cells accessible
           floodfail = 1                     # set flood failure status flag
           flooded = 1 # stop  the flooding loop
           if (debug == 1):
               print (strt, fin, nxt, n, proclist)
       #print ("after flood")
       #showflood()
   floodend = time.time() # get time now
   floodtime = floodend - floodstart
   if (debug == 1):
       print ("floodtime", floodtime, " cleared", floodcleared )
   return                                    # return
       #print (curr, n, nxt, fval, proclist[n-1])
   #showflood()
   #showwalls()
   #halt()  

start = numcells-1
fin = 0
maze_clear()
add_wall(cell_id(0, 0),EAST)

add_wall(cell_id(7, 7),WEST)
add_wall(cell_id(7, 7),SOUTH)
add_wall(cell_id(8, 7),SOUTH)
add_wall(cell_id(8, 7),EAST)
# add_wall(cell_id(8, 8),EAST)
add_wall(cell_id(8, 8),NORTH)
add_wall(cell_id(7, 8),NORTH)
add_wall(cell_id(7, 8),WEST)

add_wall(cell_id(4, 4),NORTH)
add_wall(cell_id(4, 4),EAST)
add_wall(cell_id(4, 4),SOUTH)
add_wall(cell_id(4, 4),WEST)

showmaze()
floodclear()
floodmaze(cell_id(7,7),fin)
showmaze()
start_time = time.time()
iterations = 1000
for _ in range(iterations):
  floodmaze(cell_id(7,7),fin)
  
end_time = time.time()
t = end_time - start_time
showmaze()
print("Flood distance correct: ",get_cost(0,0) == 20)
print(f"Execution Time for {iterations} iterations: {t:.6f} seconds")