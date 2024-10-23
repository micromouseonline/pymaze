from maze_support import * #Location, WallInfo  # as cc #import *
import os
import sys

class Queue:
    def __init__(self, num_items=64):
        self.mData = [Location()] * (num_items + 1)
        self.mHead = 0
        self.mTail = 0
        self.mItemCount = 0

    def size(self) -> int:
        return self.mItemCount

    def clear(self):
        self.mHead = 0
        self.mTail = 0
        self.mItemCount = 0

    def add(self, item : Location):
        self.mData[self.mTail] = item
        self.mTail += 1
        self.mItemCount += 1
        if self.mTail > len(self.mData) - 1:
            self.mTail = 0

    def head(self)  -> Location:
        result = self.mData[self.mHead]
        self.mHead += 1
        if self.mHead > len(self.mData) - 1:
            self.mHead = 0
        self.mItemCount -= 1
        return result

class Maze:

    # @timed_function
    # Print time taken by a function call
    # https://github.com/peterhinch/micropython-samples/blob/master/timed_function/timed_func.py

 

    def __init__(self, size : int = 16,  start : Location = Location(7,7,16) ) :
        self.m_width = size
        self.m_height = size
        self.m_walls = [[WallInfo() for i in range(size)] for j in range(size)] 
        self.m_cost =  [[0 for i in range(size)] for j in range(size)]   
        self.m_goal =  Location(7,7, size)
        start.mazeHeight = size
        start.size = size
        self.m_start = Location(0,0, size)
        self.m_maze_cell_count = size * size
        self.m_max_cost = self.m_maze_cell_count - 1
        self.initialise()


    def goal(self) -> Location :
        return self.m_goal


    #changes the default goal. For example in a practice maze
    def set_goal(self, goal : Location) -> None :
        goal.mazeHeight = self.m_height
        goal.size = self.m_width
        self.m_goal = goal

    # return the state of the walls in a cell
    def walls(self, cell : Location) -> WallInfo :
        return self.m_walls[cell.x][cell.y]
    

    #return true if ANY walls in a cell have NOT been seen
    def has_unknown_walls(self, cell: Location) -> bool :
        walls_here = self.m_walls[cell.x][cell.y]
        
        if (walls_here.north == WALL_UNKNOWN or walls_here.east == WALL_UNKNOWN or walls_here.south == WALL_UNKNOWN or walls_here.west == WALL_UNKNOWN) :
            return True
        else :
            return False


    # return true if ALL the walls in a cell have been seen
    def cell_is_visited(self, cell : Location) -> bool : 
        return not self.has_unknown_walls(cell)
    

    #  Test if the given wall is an exit. This will allow travel through unseen walls
    # This is used in costing / flooding the mase
    # Only the concepct of an open maze is used here
    def is_exit(self,  cell : Location, heading : int) -> bool :
        result = False
        walls = self.m_walls[cell.x][cell.y]

        if heading == HDG_NORTH :
            result = walls.north != WALL_PRESENT #This is a change to the UKMARSBOT code as it used a bitwise operating for open and closed mazes
        elif heading == HDG_EAST :
            result = walls.east  != WALL_PRESENT
        elif heading == HDG_SOUTH :
            result = walls.south != WALL_PRESENT
        elif heading == HDG_WEST :
            result = walls.west  != WALL_PRESENT
        
        return result


    # only change a wall if it is unknown
    # This is what you use when exploring. Once seen, a wall should not be changed again.
    def update_wall_state(self,  cell : Location, heading : int, state : int) -> None :

        if heading == HDG_NORTH :
            if (self.m_walls[cell.x][cell.y].north  != WALL_UNKNOWN) :
                return
        elif heading == HDG_EAST :
            if (self.m_walls[cell.x][cell.y].east != WALL_UNKNOWN) :
                return
        elif heading == HDG_WEST :
            if (self.m_walls[cell.x][cell.y].west != WALL_UNKNOWN) :
                return
        elif heading == HDG_SOUTH :
            if (self.m_walls[cell.x][cell.y].south != WALL_UNKNOWN) :
                return
        
        self.set_wall_state(cell, heading, state)

    #@brief set empty maze with border walls and the start cell, zero costs
    def initialise(self) -> None :

        for x in range(self.m_width) : 
            for y in range(self.m_height) : 
                self.m_walls[x][y].north = WALL_UNKNOWN
                self.m_walls[x][y].east = WALL_UNKNOWN
                self.m_walls[x][y].south = WALL_UNKNOWN
                self.m_walls[x][y].west = WALL_UNKNOWN

        for x in range(self.m_width) : 
            self.m_walls[x][0].south = WALL_PRESENT
            self.m_walls[x][self.m_height - 1].north = WALL_PRESENT
        
        for y in range(self.m_height) : 
            self.m_walls[0][y].west = WALL_PRESENT
            self.m_walls[self.m_width - 1][y].east = WALL_PRESENT
        
        print(self.m_start)
        self.m_walls[0][0].north = WALL_ABSENT
        self.m_walls[0][0].north = WALL_UNKNOWN

        self.flood(self.goal())
        

    #return cost for neighbour cell in supplied heading
    def neighbour_cost(self, cell : Location, heading : int) -> int :
        if not self.is_exit(cell, heading) :
            return self.m_max_cost
        
        next_cell = cell.neighbour(heading)
        return self.m_cost[next_cell.x][next_cell.y]

    # return the cost associated withthe supplied cell location
    def cost(self, cell : Location) -> int :
        return self.m_cost[cell.x][cell.y]
    

    '''   * @brief basic manhattan flood of the maze
    *
    * Very simple cell counting flood fills m_cost array with the
    * manhattan distance from every cell to the target.
    *
    * Although the queue looks complicated, this is a fast flood that
    * examines each accessible cell exactly once. Consequently, it runs
    * in fairly constant time, taking 5.3ms when there are no interrupts.
    *
    * @param target - the cell from which all distances are calculated
    */
    '''

    def flood(self, target: Location) -> None:
         #TODO should the target be checked to see if it can exist in the maze?

        m_width = self.m_width
        m_height = self.m_height
        m_max_cost = self.m_max_cost
        m_cost = self.m_cost
        m_maze_cell_count = self.m_maze_cell_count

        for x in range(m_width) : 
            for y in range(m_height) :
                self.m_cost[x][y] = m_max_cost 
                    
        queue = Queue(m_maze_cell_count)

        m_cost[target.x][target.y] = 0
        queue.add(target)
        while (queue.size() > 0) :
            here = queue.head()
            here.size = self.m_width
            here.mazeHeight = self.m_height # Bit of a bodge to stop errors on small maze sizes
            newCost = m_cost[here.x][here.y] + 1
            
            for h in range(HDG_COUNT) : # (int h = NORTH; h < HEADING_COUNT; h++) {
                heading = h
                if (self.is_exit(here, heading)) : 
                    nextCell = here.neighbour(heading)  
                    if (m_cost[nextCell.x][nextCell.y] > newCost) :
                        self.m_cost[nextCell.x][nextCell.y] = newCost
                        queue.add(nextCell)
            

    '''* Algorithm looks around the current cell and records the smallest
    * neighbour and its direction. By starting with the supplied direction,
    * then looking right, then left, the result will preferentially be
    * ahead if there are multiple neighbours with the same m_cost.
    *
    * This could be extended to look ahead then towards the goal but it
    * probably is not worth the effort
    * @brief get the geating to the lowest cost neighbour
    * @param cell
    * @param start_heading
    * @return
    */'''
    def heading_to_smallest(self, cell :  Location, start_heading :  int) -> int : 
        next_heading = start_heading
        best_heading = HDG_BLOCKED
        best_cost = self.cost(cell)
        
        cost = self.neighbour_cost(cell, next_heading)
        
        if (cost < best_cost) :
            best_cost = cost
            best_heading = next_heading
        
        next_heading = right_from(start_heading)
        cost = self.neighbour_cost(cell, next_heading)
        if (cost < best_cost) :
            best_cost = cost
            best_heading = next_heading
        
        next_heading = left_from(start_heading)
        cost = self.neighbour_cost(cell, next_heading)
        if (cost < best_cost) :
            best_cost = cost
            best_heading = next_heading
        
        next_heading = behind_from(start_heading)
        cost = self.neighbour_cost(cell, next_heading)
        if (cost < best_cost) :
            best_cost = cost
            best_heading = next_heading
        
        if (best_cost == self.m_max_cost) :
            best_heading = HDG_BLOCKED
        
        return best_heading

    def set_wall_state(self,x,y, heading : int, state : int) -> None:
        if heading == HDG_NORTH:
            self.m_walls[x][y].north = state
            self.m_walls[y][y+1].south = state
        elif heading == HDG_EAST:
            self.m_walls[x][y].east = state
            self.m_walls[x+1][y].west = state
        elif heading == HDG_WEST:
            self.m_walls[x][y].west = state
            self.m_walls[x-1][y].east = state
        elif heading == HDG_SOUTH:
            self.m_walls[x][y].south = state
            self.m_walls[x][y-1].north = state
        else:
            # ignore any other heading (blocked)
            pass
    # def set_wall_state(self, x : int, y : int, heading : int, state : int) -> None:
    #     self.set_wall_state(Location(x,y,self.m_width, self.m_height), heading, state)

    POST = 'o'
    ERR = '?'
    GAP = "   "
    H_WALL = "---"
    H_EXIT = "   "
    H_UNKN = " . "
    H_VIRT = "###"
    V_WALL = '|'
    V_EXIT = ' '
    V_UNKN = ':'
    V_VIRT = '#'

    def print_h_wall(self, state : int) -> None :
        if state == WALL_ABSENT:
            print(self.H_EXIT, end="")
        elif state == WALL_PRESENT :
            print(self.H_WALL, end="")
        elif state == WALL_VIRTUAL :
            print(self.H_VIRT, end="")
        else:
            print(self.H_UNKN, end="")

    def printNorthWalls(self, y : int):
        for x in range(self.m_width):
            print(self.POST, end="")
            walls = self.walls(Location(x,y,self.m_width))
            self.print_h_wall(walls.north)
        print(self.POST)

    def printSouthWalls(self, y : int):
        for x in range(self.m_width):
            print(self.POST, end="")
            walls = self.walls(Location(x,y,self.m_width))
            self.print_h_wall(walls.south)
        print(self.POST)

    def print_justified(self, value, width) -> None:
        v = value
        w = width
        w -= 1

        if v < 0:
            w -= 1

        while v // 10:
            w -= 1
            v //= 10

        while w > 0:
            print(' ', end="")
            w -= 1

        print(value, end="")

    def print_maze2(self):
        for row in range(self.m_width - 1, -1, -1):
            # Print the north walls and top boundary
            line = "+"
            for col in range(self.m_width):
                walls = self.walls(Location(col,row))
                if walls.north == WALL_PRESENT:
                    line += "---+"
                else:
                    line += "   +"
            print(line)

            # Print the west walls and cell boundary
            line = ""
            for col in range(self.m_width):
                walls = self.walls(Location(col,row))
                if walls.west == WALL_PRESENT:
                    line += "|"
                else:
                    line += " "
                if self.m_cost[row][col] is not None:
                    line += f"{self.m_cost[col][row]:>3}"
                else:
                    line += "   "
            walls = self.walls(Location(15,row))
            if walls.east == WALL_PRESENT: 
                line += "|"  # Rightmost boundary
            else:
                line += " " 
            print(line)

        # Print the bottom boundary
        line = "+"
        for col in range(self.m_width):
            walls = self.walls(Location(col,row))
            if walls.south == WALL_PRESENT:
                line += "---+"
            else:
                line += "   +"
        print(line)

    def print_maze(self,  style : int = VIEW_PLAIN) -> None:
        dir_chars = "^>v<* "
        #self.flood(self.goal())

        for y in range(self.m_height-1,-1,-1) :
            self.printNorthWalls(y)
            for x in range(self.m_width) :
                location = Location(x,y,self.m_width)
                walls = self.walls(location)
                state = walls.west
                if state == WALL_ABSENT :
                    print(self.V_EXIT, end="")
                elif state == WALL_PRESENT :
                    print(self.V_WALL, end="")
                elif state == WALL_VIRTUAL :
                    print(self.V_VIRT, end="")
                else:
                    print(self.V_UNKN, end="")
                
                if style == VIEW_COSTS :
                    self.print_justified(self.cost(location), 3)

                elif style == VIEW_DIRS :
                    direction = self.heading_to_smallest(location, HDG_NORTH)
                    if location == self.goal() :
                        direction = HDG_COUNT
                    
                    arrow = ' ' 
                    if direction != HDG_BLOCKED :
                        arrow = dir_chars[direction]
                    print(" ", end="")
                    print(arrow, end="")
                    print(" ", end="")
                
                else :
                    print(self.GAP, end="")
            print(self.V_WALL)
        self.printSouthWalls(0)
        print()


    
if __name__ == "__main__":    
    maze = Maze()
    maze.set_wall_state(7, 7, HDG_WEST, WALL_PRESENT)
    maze.set_wall_state(7, 7, HDG_SOUTH, WALL_PRESENT)
    maze.set_wall_state(8, 7, HDG_SOUTH, WALL_PRESENT)
    maze.set_wall_state(8, 7, HDG_EAST, WALL_PRESENT)
    maze.set_wall_state(8, 8, HDG_EAST, WALL_ABSENT)
    maze.set_wall_state(8, 8, HDG_NORTH, WALL_PRESENT)
    maze.set_wall_state(7, 8, HDG_NORTH, WALL_PRESENT)
    maze.set_wall_state(7, 8, HDG_WEST, WALL_PRESENT)
    maze.set_wall_state(4, 4, HDG_NORTH, WALL_PRESENT)
    maze.set_wall_state(4, 4, HDG_EAST, WALL_PRESENT)
    maze.set_wall_state(4, 4, HDG_SOUTH, WALL_PRESENT)
    maze.set_wall_state(4, 4, HDG_WEST, WALL_PRESENT)
    
    start_time = millis()
  
 
    for _ in range(iterations()):
        distances = maze.flood(maze.goal())  # Assuming the target cell is at (7, 7)
    end_time = millis()
    t = end_time - start_time
    maze.print_maze2()
    maze.print_maze(VIEW_COSTS)
    print(f"{sys.implementation.name} - maze_pb: Execution Time for {iterations()} iterations: {t:} milliseconds")
