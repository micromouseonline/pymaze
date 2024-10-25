import os
import sys

from maze_support import *

# Initialize a 1D array of size 256 for the maze (16x16)
maze = [0 for _ in range(16 * 16)]

# Default start and goal positions
start_x, start_y = 0, 0  # Start position
goal_x, goal_y = 7, 7    # Goal position


# Initialize the cost array (16x16) with all values set to 255
# cost = [[255 for _ in range(16)] for _ in range(16)]
cost = [255] * 256

# Define masks and bit positions for wall states and visited status
WALL_NORTH_SHIFT = 0  # Bit position for North wall (2 bits)
WALL_EAST_SHIFT = 2   # Bit position for East wall (2 bits)
WALL_SOUTH_SHIFT = 4  # Bit position for South wall (2 bits)
WALL_WEST_SHIFT = 6   # Bit position for West wall (2 bits)
VISITED_SHIFT = 8     # Bit position for visited status (1 bit)

WALL_STATE_MASK = 0b11

# Wall state encoding
UNKNOWN = 0b00
PRESENT = 0b01
ABSENT = 0b10
VIRTUAL = 0b11

# Helper function to compute index in the 1D array


def compute_index(x, y):
    # return x * 16 + y
    return y + x * 16

# Function to set wall state for a cell and its adjacent cell


def set_wall(x, y, wall_shift, state):
    # Compute the index of the current cell
    index = compute_index(x, y)

    # Clear the 2 bits corresponding to the wall in the current cell
    maze[index] &= ~(WALL_STATE_MASK << wall_shift)
    # Set the wall state using bitwise OR
    maze[index] |= (state << wall_shift)

    # Now handle the adjacent cell
    if wall_shift == WALL_NORTH_SHIFT and x > 0:
        # Calculate index for the cell above (North wall -> South wall of the above cell)
        index_above = compute_index(x, (y + 1) % 16)
        # Clear South wall bits of the above cell
        maze[index_above] &= ~(WALL_STATE_MASK << WALL_SOUTH_SHIFT)
        # Set South wall bits of the above cell
        maze[index_above] |= (state << WALL_SOUTH_SHIFT)
    elif wall_shift == WALL_EAST_SHIFT and y < 15:
        # Calculate index for the cell to the right (East wall -> West wall of the right cell)
        index_right = compute_index((x + 1) % 16, y)
        # Clear West wall bits of the right cell
        maze[index_right] &= ~(WALL_STATE_MASK << WALL_WEST_SHIFT)
        # Set West wall bits of the right cell
        maze[index_right] |= (state << WALL_WEST_SHIFT)
    elif wall_shift == WALL_SOUTH_SHIFT and x < 15:
        # Calculate index for the cell below (South wall -> North wall of the below cell)
        index_below = compute_index(x, (y + 16 - 1) % 16)
        # Clear North wall bits of the below cell
        maze[index_below] &= ~(WALL_STATE_MASK << WALL_NORTH_SHIFT)
        # Set North wall bits of the below cell
        maze[index_below] |= (state << WALL_NORTH_SHIFT)
    elif wall_shift == WALL_WEST_SHIFT and y > 0:
        # Calculate index for the cell to the left (West wall -> East wall of the left cell)
        index_left = compute_index((x + 16 - 1) % 16, y)
        # Clear East wall bits of the left cell
        maze[index_left] &= ~(WALL_STATE_MASK << WALL_EAST_SHIFT)
        # Set East wall bits of the left cell
        maze[index_left] |= (state << WALL_EAST_SHIFT)


# Function to get wall state
def get_wall(x, y, wall_shift):
    index = compute_index(x, y)
    # Extract the 2 bits corresponding to the wall
    return (maze[index] >> wall_shift) & WALL_STATE_MASK


def get_wall_from_index(index, wall_shift):
    # Extract the 2 bits corresponding to the wall
    return (maze[index] >> wall_shift) & WALL_STATE_MASK


# Function to mark a cell as visited
def set_visited(x, y):
    index = compute_index(x, y)
    maze[index] |= (1 << VISITED_SHIFT)

# Function to check if a cell has been visited


def is_visited(x, y):
    index = compute_index(x, y)
    return (maze[index] >> VISITED_SHIFT) & 1

# Function to initialize the maze


def initialize_maze():

    for x in range(16):
        for y in range(16):
            set_wall(x, y, WALL_NORTH_SHIFT, UNKNOWN)
            set_wall(x, y, WALL_EAST_SHIFT, UNKNOWN)
            set_wall(x, y, WALL_SOUTH_SHIFT, UNKNOWN)
            set_wall(x, y, WALL_WEST_SHIFT, UNKNOWN)

    for x in range(16):
        set_wall(x, 0, WALL_SOUTH_SHIFT, PRESENT)
        set_wall(x, 15, WALL_NORTH_SHIFT, PRESENT)

    for y in range(16):
        set_wall(0, y, WALL_WEST_SHIFT, PRESENT)
        set_wall(15, y, WALL_EAST_SHIFT, PRESENT)

    set_wall(0, 0, WALL_EAST_SHIFT, PRESENT)

# Flood-fill method to calculate Manhattan distances from the goal


def flood_fill(target_cell, start_cell=0, closedMaze=False):
    global cost, maze

    MAX_COST = 255
    MAZE_CELL_COUNT = 256

    cost = [MAX_COST] * MAZE_CELL_COUNT
    cost[target_cell] = 0

    # Static size queue - no modulo needed
    queue = [0] * MAZE_CELL_COUNT
    head = 0
    tail = 1
    queue[0] = target_cell

    while head < tail:
        here = queue[head]
        head += 1
        cost_here = cost[here]
        walls_here = maze[here]
        # (maze[index] >> wall_shift) & 0b11
        # Handle SOUTH_WALL (cell - 1)
        if ((walls_here >> WALL_SOUTH_SHIFT) & WALL_STATE_MASK) != PRESENT:
            south_cell = here - 1
            if cost[south_cell] == MAX_COST:
                cost[south_cell] = cost_here + 1
                queue[tail] = south_cell
                tail += 1

        # Handle EAST_WALL (cell + MAZE_SIZE)
        if ((walls_here >> WALL_EAST_SHIFT) & WALL_STATE_MASK) != PRESENT:
            east_cell = here + 16
            if cost[east_cell] == MAX_COST:
                cost[east_cell] = cost_here + 1
                queue[tail] = east_cell
                tail += 1

        # Handle NORTH_WALL (cell + 1)
        if ((walls_here >> WALL_NORTH_SHIFT) & WALL_STATE_MASK) != PRESENT:
            north_cell = here + 1
            if cost[north_cell] == MAX_COST:
                cost[north_cell] = cost_here + 1
                queue[tail] = north_cell
                tail += 1

        # Handle WEST_WALL (cell - MAZE_SIZE)
        if ((walls_here >> WALL_WEST_SHIFT) & WALL_STATE_MASK) != PRESENT:
            west_cell = here - 16
            if cost[west_cell] == MAX_COST:
                cost[west_cell] = cost_here + 1
                queue[tail] = west_cell
                tail += 1

    # return cost


# Wall and post representations for printing
POST = 'o'
GAP = "   "
H_WALL = "---"
H_EXIT = "   "
H_UNKN = " . "
H_VIRT = "###"
V_WALL = '|'
V_EXIT = ' '
V_UNKN = ':'
V_VIRT = '#'


def print_h_wall(state) -> None:
    if state == ABSENT:
        print(H_EXIT, end="")
    elif state == PRESENT:
        print(H_WALL, end="")
    elif state == VIRTUAL:
        print(H_VIRT, end="")
    else:
        print(H_UNKN, end="")


def printNorthWalls(y):
    for x in range(16):
        print(POST, end="")
        print_h_wall(get_wall(x, y, WALL_NORTH_SHIFT))
    print(POST)


def printSouthWalls(y: int):
    for x in range(16):
        print(POST, end="")
        print_h_wall(get_wall(x, y, WALL_SOUTH_SHIFT))
    print(POST)
# Function to print the maze with posts and correct orientation


def print_maze():
    for y in range(15, -1, -1):
        printNorthWalls(y)
        for x in range(16):
            state = get_wall(x, y, WALL_WEST_SHIFT)

            if state == ABSENT:
                print(V_EXIT, end="")
            elif state == PRESENT:
                print(V_WALL, end="")
            elif state == VIRTUAL:
                print(V_VIRT, end="")
            else:
                print(V_UNKN, end="")
            print(f"{cost[compute_index(x,y)]:3}", end="")
            # print(GAP, end="")
        print(V_WALL)
    printSouthWalls(0)


# Initialize the maze
initialize_maze()

set_wall(7, 7, WALL_WEST_SHIFT, PRESENT)
set_wall(7, 7, WALL_SOUTH_SHIFT, PRESENT)
set_wall(8, 7, WALL_SOUTH_SHIFT, PRESENT)
set_wall(8, 7, WALL_EAST_SHIFT, PRESENT)
set_wall(8, 8, WALL_EAST_SHIFT, ABSENT)
set_wall(8, 8, WALL_NORTH_SHIFT, PRESENT)
set_wall(7, 8, WALL_NORTH_SHIFT, PRESENT)
set_wall(7, 8, WALL_WEST_SHIFT, PRESENT)
set_wall(4, 4, WALL_NORTH_SHIFT, PRESENT)
set_wall(4, 4, WALL_EAST_SHIFT, PRESENT)
set_wall(4, 4, WALL_SOUTH_SHIFT, PRESENT)
set_wall(4, 4, WALL_WEST_SHIFT, PRESENT)

# Call the flood-fill method to populate the cost array
flood_fill(compute_index(7, 7))
print_maze()
# print_maze_with_cost()


start_time = millis()


for _ in range(iterations()):
    # Assuming the target cell is at (7, 7)
    distances = flood_fill(compute_index(7, 7))
end_time = millis()
t = end_time - start_time
print_maze()
print(f"{sys.implementation.name} - maze_pb: Execution Time for {iterations()} iterations: {t:} milliseconds")
