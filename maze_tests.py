"""
 Here can go tests for the maze implementations
"""
import sys

if sys.implementation.name == 'micropython':
    print("Unit tests not currently supported on MicroPython")
    sys.exit()


import unittest
import time
from maze_support import *
from maze import *
from maze_files import *


def millis():
    """
    A relatitvely platform independent version of time.ticks_ms()
    """
    if sys.implementation.name == 'micropython':
        # MicroPython
        return time.ticks_ms()
    else:
        # Desktop Python
        return int(round(time.time() * 1000))


def iterations():
    """
    Since the pico is much slower than a PC, it makes sense that any
    timing/performance tests are run a different number of times on each.
    """
    if sys.implementation.name == 'micropython':
        return 100
    else:
        return 10000


class TestTiming(unittest.TestCase):

    def test_millis(self):
        t = millis()
        time.sleep(1.0)
        t = millis() - t
        self.assertTrue(abs(t - 1000) <= 1, "Should be 1000")


class TestMazeCellID(unittest.TestCase):

    def test_maze_cell_id(self):
        maze = Maze()
        self.assertEqual(maze.cell_id(0, 0), 0)
        self.assertEqual(maze.cell_id(0, 1), 1)
        self.assertEqual(maze.cell_id(1, 0), maze.size)
        self.assertEqual(maze.cell_id(1, 1), maze.size+1)

    def test_maze_cell_xy(self):
        maze = Maze()
        x, y = maze.cell_xy(18)
        self.assertEqual(x, 18 // maze.size)
        self.assertEqual(y, 18 % maze.size)
                         


class TestMazeCellNeighbour(unittest.TestCase):

    def test_maze_cell_neighbour(self):
        maze = Maze()
        cell = maze.cell_id(1, 1)
        self.assertEqual(maze.neighbour(cell, DIR_NORTH), cell + 1)
        self.assertEqual(maze.neighbour(cell, DIR_EAST),  cell + maze.size)
        self.assertEqual(maze.neighbour(cell, DIR_SOUTH), cell - 1)
        self.assertEqual(maze.neighbour(cell, DIR_WEST),  cell - maze.size)


class TestMazeWalls(unittest.TestCase):

    def test_default_size_is_maze_size(self):
        maze = Maze()
        self.assertEqual(maze.size, maze.size)

    def test_maze_default_walls(self):
        maze = Maze()
        for cell in maze.walls:
            self.assertEqual(cell, ALL_UNKNOWN)

    def test_maze_default_cost(self):
        maze = Maze()
        self.assertEqual(maze.cost[0], maze.MAX_COST)

    def test_maze_mask_setting(self):
        maze = Maze()
        self.assertEqual(maze.mask, OPEN_MAZE_MASK)
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertEqual(maze.mask, CLOSED_MAZE_MASK)
        maze.set_mask(OPEN_MAZE_MASK)
        self.assertEqual(maze.mask, OPEN_MAZE_MASK)

    def test_maze_set_wall(self):
        maze = Maze()
        cell = maze.cell_id(0, 0)
        neighbour_north = maze.cell_id(0, 1)
        self.assertTrue(maze.cell_has_exit(cell, DIR_NORTH))
        self.assertTrue(maze.cell_has_exit(neighbour_north, DIR_SOUTH))
        maze.set_wall(cell, DIR_NORTH, WALL_PRESENT)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))
        self.assertFalse(maze.cell_has_exit(neighbour_north, DIR_SOUTH))

    def test_maze_mask_use(self):
        maze = Maze()
        cell = maze.cell_id(4, 4)
        # wall defaults to WALL_UNKNOWN - OPEN is exit, CLOSED it not
        maze.set_mask(OPEN_MAZE_MASK)
        self.assertTrue(maze.cell_has_exit(cell, DIR_NORTH))
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))

        # wall set to WALL_PRESENT - never an exit
        maze.set_wall(cell, DIR_NORTH, WALL_PRESENT)
        maze.set_mask(OPEN_MAZE_MASK)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))

        # wall set to WALL_ABSENT - always an exit
        maze.set_wall(cell, DIR_NORTH, WALL_ABSENT)
        maze.set_mask(OPEN_MAZE_MASK)
        self.assertTrue(maze.cell_has_exit(cell, DIR_NORTH))
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertTrue(maze.cell_has_exit(cell, DIR_NORTH))

        # wall set to WALL_VIRTUAL - never an exit
        maze.set_wall(cell, DIR_NORTH, WALL_VIRTUAL)
        maze.set_mask(OPEN_MAZE_MASK)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertFalse(maze.cell_has_exit(cell, DIR_NORTH))

    def test_maze_init_walls(self):
        maze = Maze()
        maze.init_walls()
        cell = maze.cell_id(0, 0)
        self.assertTrue(maze.cell_has_exit(cell, DIR_NORTH))
        self.assertFalse(maze.cell_has_exit(cell, DIR_EAST))
        self.assertFalse(maze.cell_has_exit(cell, DIR_SOUTH))
        self.assertFalse(maze.cell_has_exit(cell, DIR_WEST))

    def test_maze_updates_only_once(self):
        maze = Maze()
        maze.init_walls()
        cell = maze.cell_id(8, 8)
        self.assertTrue(maze.cell_has_exit(cell, DIR_SOUTH))
        maze.update_wall(cell, DIR_SOUTH, WALL_PRESENT)
        self.assertFalse(maze.cell_has_exit(cell, DIR_SOUTH))
        maze.update_wall(cell, DIR_SOUTH, WALL_ABSENT)
        self.assertFalse(maze.cell_has_exit(cell, DIR_SOUTH))

class TestMazeCellVisited(unittest.TestCase):
    def test_maze_cell_is_visited(self):
        maze = Maze()
        self.assertFalse(maze.cell_is_visited(0))
        maze.init_walls()
        self.assertTrue(maze.cell_is_visited(0))
        self.assertFalse(maze.cell_is_visited(1))
    

class TestMazeGoal(unittest.TestCase):
    def test_maze_goal_default(self):
        maze = Maze()
        self.assertEqual(maze.get_goal(), maze.cell_id(7, 7))

    def test_maze_set_goal(self):
        maze = Maze()
        maze.set_goal(maze.cell_id(8, 8))
        self.assertEqual(maze.get_goal(), maze.cell_id(8, 8))


class TestMazeFlood(unittest.TestCase):

    def test_maze_flood_empty_maze_open(self):
        maze = Maze()
        maze.set_mask(OPEN_MAZE_MASK)
        maze.init_walls()
        target = maze.get_goal()
        start = maze.cell_id(0, 0)
        maze.flood(target)
        self.assertEqual(maze.cost[start], 14)

    def test_maze_flood_empty_maze_closed(self):
        maze = Maze()
        maze.set_mask(CLOSED_MAZE_MASK)
        maze.init_walls()
        target = maze.get_goal()
        start = maze.cell_id(0, 0)
        maze.flood(target)
        MAX_COST = maze.size * maze.size
        self.assertEqual(maze.cost[start], MAX_COST)

    def test_maze_flood_empty_maze_reverse(self):
        maze = Maze()
        maze.set_mask(OPEN_MAZE_MASK)
        maze.init_walls()
        target = maze.get_goal()
        start = maze.cell_id(0, 0)
        maze.flood(start)
        self.assertEqual(maze.cost[target], 14)
        top_right = maze.cell_id(maze.size-1, maze.size-1)
        self.assertEqual(maze.cost[top_right], 30)

class TestDirectionToSmallest(unittest.TestCase):

    def test_direction_to_smallest(self):
        maze = Maze()
        maze.init_walls()
        maze.set_mask(OPEN_MAZE_MASK)
        maze.flood(maze.get_goal())
        cell = maze.cell_id(1,1)

        self.assertEqual(maze.direction_to_smallest(cell,DIR_NORTH), DIR_NORTH)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_EAST), DIR_EAST)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_SOUTH), DIR_EAST)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_WEST), DIR_NORTH)
        
        cell = maze.cell_id(0,0)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_NORTH), DIR_NORTH)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_EAST), DIR_NORTH)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_SOUTH), DIR_NORTH)
        self.assertEqual(maze.direction_to_smallest(cell,DIR_WEST), DIR_NORTH)


class TestMazeSolution(unittest.TestCase):
    def test_maze_has_no_solution_after_init(self):
        maze = Maze()
        maze.init_walls()
        self.assertFalse(maze.speed_run_possible())

    def test_maze_has_solution_after_explore(self):
        maze = Maze()
        maze.init_walls_from_string(all_japan_2007)
        self.assertTrue(maze.speed_run_possible())


class TestMazeLoad(unittest.TestCase):

    def test_maze_load(self):
        maze = Maze()
        maze.init_walls_from_string(all_japan_2007)
        goal_cell = maze.get_goal()
        start_cell = maze.cell_id(0, 0)
        self.assertTrue(maze.cell_has_exit(goal_cell, DIR_NORTH))
        self.assertTrue(maze.cell_has_exit(goal_cell, DIR_EAST))
        self.assertFalse(maze.cell_has_exit(goal_cell, DIR_SOUTH))
        self.assertFalse(maze.cell_has_exit(goal_cell, DIR_WEST))
        maze.flood(goal_cell)
        self.assertEqual(maze.cost[goal_cell], 0)
        self.assertEqual(maze.cost[start_cell], 72)
        maze.set_mask(CLOSED_MAZE_MASK)
        self.assertEqual(maze.cost[start_cell], 72)


if __name__ == "__main__":
    print("This system is running {}".format(sys.implementation.name))
    print("start...")
    unittest.main()
