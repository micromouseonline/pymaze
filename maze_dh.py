"""
maze-ph.py
A simple, naive implementation of the maze and manhattan flood algorithm
The code is mostly developed from suggestions by copilot
"""

import time
from maze_support import *
from collections import deque

class Maze:
    


    def __init__(self, size=16):
        self.size = size
        self.cost = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.walls = {
            (row, col): {"N": WALL_UNKNOWN, "E": WALL_UNKNOWN, "S": WALL_UNKNOWN, "W": WALL_UNKNOWN}
            for row in range(size)
            for col in range(size)
        }


    def clear_walls(self):
        self.walls = {
            (row, col): {"N": WALL_UNKNOWN, "E": WALL_UNKNOWN, "S": WALL_UNKNOWN, "W": WALL_UNKNOWN}
            for row in range(self.size)
            for col in range(self.size)
        }
        for cell in range(16):
            maze.set_wall(cell, 0, "S", WALL_PRESENT)
            maze.set_wall(cell, 15, "N", WALL_PRESENT)
            maze.set_wall(0, cell, "W",  WALL_PRESENT)
            maze.set_wall(15, cell, "E", WALL_PRESENT)

    def set_wall(self, col, row, direction, state):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            self.walls[(col, row)][direction] = state
            # Add wall on the opposite side for the neighboring cell
            if direction == "N" and row < self.size - 1:
                self.walls[(col, row + 1)]["S"] = state
            elif direction == "E" and col < self.size - 1:
                self.walls[(col + 1, row)]["W"] = state
            elif direction == "S" and row > 0:
                self.walls[(col, row - 1)]["N"] = state
            elif direction == "W" and col > 0:
                self.walls[(col - 1, row)]["E"] = state

    def get_wall(self, col, row, direction):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            return self.walls[(col, row)][direction]
        return
    
    def has_wall(self, col, row, direction):
        if (col, row) in self.walls and direction in self.walls[(col, row)]:
            return self.walls[(col,row)][direction] == WALL_PRESENT
        return False

    def print_maze(self):
        for row in range(self.size - 1, -1, -1):
            # Print the north walls and top boundary
            line = "+"
            for col in range(self.size):
                if self.get_wall(col, row, "N") == WALL_PRESENT:
                    line += "---+"
                else:
                    line += "   +"
            print(line)

            # Print the west walls and cell boundary
            line = ""
            for col in range(self.size):
                if self.get_wall(col, row, "W") == WALL_PRESENT:
                    line += "|"
                else:
                    line += " "
                if self.cost[row][col] is not None:
                    line += f"{self.cost[col][row]:>3}"
                else:
                    line += "   "
            if self.get_wall(15, row, "E") == WALL_PRESENT: 
                line += "|"  # Rightmost boundary
            else:
                line += " " 
            print(line)

        # Print the bottom boundary
        line = "+"
        for col in range(self.size):
            if self.get_wall(col, 0, "S") == WALL_PRESENT:
                line += "---+"
            else:
                line += "   +"
        print(line)


    def floodclear(self): # clear the flood table
        self.cost = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def cell_id(self,col,row):
        return row+col*self.size
    
    def cell_xy(self,cell):
        return (cell // 16, cell % 16)
    
    def floodmaze(self,target,end_cell):   # flood the maze from the strt cell to the fin cell
        # global maze, walls, floodfail
        proclist = [0]*self.size*self.size
        self.floodclear()           # clear the flood table to all 283
        flooded = 0                 # set flag to not finished flooding yet
        here = target               # current cell being processed
        x,y = self.cell_xy(target)
        self.cost[x][y] = 0         # set start cell flood value to one
        n = 0                       # index for processing list array of cells to say where to add to end of list
        nxt = 0                     # pointer to the first unprocessed item on the list
        while (flooded == 0):
            x,y = self.cell_xy(here)
            cost_here = self.cost[x][y]                                                             # get current value of current cell
            if not self.has_wall(x,y,"S") and y > 0:                                               # is there a gap to the SOUTH of current cell
                if ((self.cost[x][y-1] == 0) or ((cost_here + 1) < self.cost[x][y-1])):
                    self.cost[x][y-1] = cost_here + 1                                               # set flood value in this cell
                    proclist[n] = here-1                                                    # save flood cell for future processing
                    n = n + 1                                                                       # update processing list number
                    if (proclist[n-1] == end_cell):                                                 # check if finished flooding
                        flooded = 1                                                                 # set flag to stop loop
                
            if not self.has_wall(x,y,"E") and x < self.size-1:                                              # is there a gap to the EAST of current cell
                if ((self.cost[x+1][y] == 0) or ((cost_here + 1) < self.cost[x+1][y])):
                    self.cost[x+1][y] = cost_here + 1        # set flood value in this cell
                    proclist[n] = here + self.size           # save flood cell for future processing
                    n = n + 1                        # update processing list number
                    if (proclist[n-1] == end_cell):           # check if finished flooding
                        flooded = 1                      # set flag to stop loop
            if (not self.has_wall(x,y,"N") and y < self.size-1):     # is there a gap to the NORTH of current cell
                if ((self.cost[x][y+1] == 0) or ((cost_here + 1) < self.cost[x][y+1])):
                    self.cost[x][y+1] = cost_here + 1    # set flood value in this cell
                    proclist[n] = here + 1       # save flood cell for future processing
                    n = n + 1                        # update processing list number
                    if (proclist[n-1] == end_cell):           # check if finished flooding
                           flooded = 1                      # set flag to stop loop
            if (not self.has_wall(x,y,"W") and x > 0):      # is there a gap to the NORTH of current cell
                if ((self.cost[x-1][y] == 0) or ((cost_here + 1) < self.cost[x-1][y])):
                    self.cost[x-1][y] = cost_here + 1        # set flood value in this cell
                    proclist[n] = here - self.size           # save flood cell for future processing
                    n = n + 1                        # update processing list number
                    if (proclist[n-1] == end_cell):       # check if finished flooding
                        flooded = 1                  # set flag to stop loop
            
            here = proclist[nxt]                 # get the location of the next cell to process
            nxt = nxt + 1                        # point to next item to process on the list
            
            if (nxt > n):                        # check if flood unable to continue as no more cells accessible
                floodfail = 1                     # set flood failure status flag
                flooded = 1 # stop  the flooding loop
                # if (debug == 1):
                #     print (target, end_cell, nxt, n, proclist)
            #print ("after flood")
            #showflood()
        return    



    def flood(self, target_col, target_row):
        
        queue = deque([(target_col, target_row, 0)])
        visited = set()

        while queue:
            col, row, dist = queue.popleft()

            if (col,row) in visited:
                continue

            visited.add((col,row))
            self.cost[col][row] = dist

            for direction, (dc, dr) in {'N': (0, 1), 'E': (1, 0), 'S': (0,-1), 'W': (-1, 0)}.items():
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    if not self.has_wall(col, row, direction) and (new_col, new_row) not in visited:
                        queue.append((new_col, new_row, dist + 1))

        return self.cost

if __name__ == "__main__":
    # Example usage
    maze = Maze()

    maze.clear_walls()   
    maze.set_wall(7, 7, "W", WALL_PRESENT)
    maze.set_wall(7, 7, "S", WALL_PRESENT)
    maze.set_wall(8, 7, "S", WALL_PRESENT)
    maze.set_wall(8, 7, "E", WALL_PRESENT)
    maze.set_wall(8, 8, "E", WALL_ABSENT)
    maze.set_wall(8, 8, "N", WALL_PRESENT)
    maze.set_wall(7, 8, "N", WALL_PRESENT)
    maze.set_wall(7, 8, "W", WALL_PRESENT)
    # check that a closed off area does not get flooded
    maze.set_wall(4, 4, "N", WALL_PRESENT)
    maze.set_wall(4, 4, "E", WALL_PRESENT)
    maze.set_wall(4, 4, "S", WALL_PRESENT)
    maze.set_wall(4, 4, "W", WALL_PRESENT)

    maze.print_maze()
       
    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        # distances = maze.flood(7, 7)  # Assuming the target cell is at (7, 7)
        maze.floodmaze(maze.cell_id(7,7),maze.cell_id(0,0))
    end_time = time.time()
    t = end_time - start_time
    maze.print_maze()
    print("Flood distance correct: ",maze.cost[0][0] == 20)
    print(f"Execution Time for {iterations} iterations: {t:.6f} seconds")
    # print(maze.cell_id(0,0))
    # print(maze.cell_id(1,0))
    # print(maze.cell_id(1,1))
    # print(maze.cell_id(0,1))
    # print(maze.cell_xy(0))
    # print(maze.cell_xy(16))
    # print(maze.cell_xy(17))
    # print(maze.cell_xy(1))
    # print("========================================================")
    # maze.print_maze()
