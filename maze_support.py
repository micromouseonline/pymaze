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

WALL_UNKNOWN = 0
WALL_PRESENT = 1
WALL_ABSENT = 2
WALL_VIRTUAL = 3

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

# bit masks used for wall presence
NORTH_WALL = (1 << DIR_NORTH)
EAST_WALL  = (1 << DIR_EAST)
SOUTH_WALL = (1 << DIR_SOUTH)
WEST_WALL  = (1 << DIR_WEST)

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

def right_from(heading : int) -> int :
    return ((heading + 1) % HDG_COUNT)


def left_from(heading : int) -> int :
    return ((heading + HDG_COUNT - 1) % HDG_COUNT)


def ahead_from(heading : int) -> int :
    return heading


def behind_from(heading : int) -> int :
    return ((heading + 2) % HDG_COUNT)

# '''
#  * Directions are relative to the robot's orientation. They do not refer to
#  * any particular heading and are just used to make code more readable where
#  * decisions are made about which way to turn.
# '''

# class Direction :
#     AHEAD = 0
#     RIGHT = 1
#     BACK = 2
#     LEFT = 3
#     DIRECTION_COUNT = 4
 

'''
 * Location stores a position in the maze as an (x,y) coordinate pair(zero index). This is
 * probably a more intuitive representation than storing just a single index
 * into and array. The method takes a little more code to manage than historical
 * methods but they were devised for processors with very little program memory.
 *
 *
 * Locations have a number of supporting operations collected into the struct so
 * that you don't have to keep re-writing the same bits of code.
 *
 *******************************************************************************88
 * PH: This is probably just overkill and confusing
 *     it is particularly irksome to pass the size all the time

 '''
class Location :
    #TODO this class has a big reliance on the overall maze size. Need to find a way to have this set once for each run rather than keep passing it around from the maze object
    #TODO type hinting fails for methods that return an instance of theselves. 
 
    def __init__(self, x: int=0, y: int=0, size : int=16) :
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return f"<Location({self.x},{self.y})>"

    def is_in_maze(self) -> bool :
        return self.x < self.size and self.y < self.size
    
    
    def operatorEqual(self, obj) -> bool :
         return self.x == obj.x and self.y == obj.y
    

    def operatorNotEqual(self, obj) -> bool :
         return self.x != obj.x or self.y != obj.y
    

    # these operators prevent the user from exceeding the bounds of the maze
    # by wrapping to the opposite edge
    def north(self) : #-> Location :
        return Location(self.x, (self.y + 1) % self.size)
    

    def east(self) : #-> Location :
        return Location((self.x + 1) % self.size, self.y)
    

    def south(self) : #-> Location :
        return Location(self.x, (self.y + self.size - 1) % self.size)
    

    def west(self) : #-> Location :
        return Location((self.x + self.size - 1) % self.size, self.y)
    

    def neighbour(self, heading : int)  -> 'Location'  : #-> Location :
        
        if heading == HDG_NORTH :
            return self.north()
            
        elif heading == HDG_EAST:
            return self.east()
            
        elif heading == HDG_SOUTH:
            return self.south()
            
        elif heading == HDG_WEST:
            return self.west()
            
        else :
            return Location()  # TODO this is actually an error and should be handled
        
    # def toArray(self) -> array.array[int] :
    #     data = array.array('i', (0 for _ in range(4)))
    #     data[0] = self.x
    #     data[1] = self.y
    #     data[2] = self.mazeWidth
    #     data[3] = self.size

        return data            



class WallInfo :
    def __init__(self):
        self.north = WALL_UNKNOWN
        self.east = WALL_UNKNOWN
        self.south = WALL_UNKNOWN
        self.west = WALL_UNKNOWN     

    def __str__(self):
        return f"<WallInfo({self.north},{self.east},{self.south},{self.west})>"       