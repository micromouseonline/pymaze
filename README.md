# pymaze

A Maze class for micromouse robots running MicroPython

For those people building a micromouse and wanting to program it in Python - specifically 
MicroPython - there are many challenges. One of those is to store a map of the maze that can be updated and flooded in an efficient manner. Python is not known for its high performance and it is not always obvious how to get the best speed out of your code.

Depending on how you structure your micromouse code, it can be especially important to flood the maze map as quickly as possible. The method used in the example code described here can perform a flood of an empty maze in about 14ms when running on a stock Raspberry Pi Pico board. By comparison, the code proposed by CoPilot took 1.3 seconds.

This code is only about manipulatng and flooding the maze. It is not, by any mans, a startnig point for getting your robot moving.

Thanks go to David Hannaford and Paul Busby for their help and suggestions.

If you have suggestions, corrections or contributions, hen please make use of the Github Issues system. Pull requests will be considered for revisions.

## Implementations

There are two separate but similar implementations included in this repository. In terms of the basic flood of the maze, both implementations take the same approach and use a well established algorithm that can be found in many other examples. Except CoPilot of course :) Note that the two implementations are not interchangeable or compatible as they use different assumptions about the mapping of the maze.

 - **Inline Code**
An implementation by David Hannaford (`maze_dh.py`) that is intended to be simply included in your main Python application gives you a way to perform a flood of the stored maze map. It purposely concerns itself almost entirely with that function though there are also functions that let you see the wall and flood data on a terminal. This code is only meant to run under micropython. 


 - **Maze Class**
The other implementation (`maze.py`) is intended to be a more complete implementation of all the functions needed to allow you to map, store and flood a micromouse maze. Although normally used as part of a multi-file Python application, the class definition and associated constants could be copied into a single-file application and used there. this is a more complex implementation because it provides additional functionality. However, if you look at the `flood()` method you will see that it uses essentially the same algorithm as the other example. The following text describes this Maze class in more detail

---

## Files

There are several files in the repository. For the inline code you should only need the `maze_dh.py` file. For the Maze Class you should need only the `maze.py` file for your project. The other files provide some support and testing functions for development on a PC.

### `maze_dh.py`
This contains code fragments meant to be copied directly into another project. It is not a standalone item. You should copy in the sections up to the examples at the bottom. Only use those if you want to  manually flood the maze and print the results. You will need to provide your own implemnation of the functions needed to set and update the map. there are a number of constants defined at thee top of the file. Do not try to use this file's contents with the maze class described below - they are not compatible.


### `maze.py`
This contains the Maze class that you add to your project along with some definitions for constants and a couple of utilities related to pathfinding. You can keep it as a single file or add just the code into your main python script if that is the way you are set up. See below for details of the methods provided by the Maze class. Do not try to use this file's contents with the inline maze code described above - they are not compatible.

For demonstration purposes, at the end of the file is an entry point (the `if __name__ == "___main__":` part) that will run a flood several times depending on the platform you use. It can be run on the desktop or directly on the target board. It is safe to delete this if you do not want to run that code.


### `maze_tests.py`
In here you will find a whole bunch of unit tests that are intended to exercise the Maze class and make sure it is working as expected. If you run this file, the tests wil run and you will get a printout of the success or failure of each. This file and its contents are only useful if you intend editing the Maze class and want to know if it still works. There is no guarantee that the tests are complete or comprehensive but they should catch most problems.

### `maze_files.py`
For testing purposes it can be useful to have some predefined mazes. This file contains two examples. They are stored as strings in just the same way as the maze files in the repository to be found here: https://github.com/micromouseonline/mazefiles.
NOTE that the method used to read these examples will not currently work in MicroPython. It is intended only to run on the desktop. 


## The Maze class

### Overview
The Maze class is concerned only with storing a map of the micromuse maze and providing a way to perform a simple flood of that map so that the micromouse robot can find its way to the goal. As part of that functionality there is a way to print out the map, calculate the distance from any cell to a single target cell, find out if the maze is mapped sufficiently for fast, safe speed runs and to calculate, for any cell, the direction to the cell that is next closest to the target.

This is not the place to find out how to program a micromouse, this is just about storing and manipulating the maze map.

### Wall Storage
Wall information is stored for every cell in the maze. While the maze can be any size, it is assumed to be square. The classic micromouse contest uses a 16x16 maze map but the code should also work with a 32x32 maze. For performance reasons, the wall data is held in a list with one element per cell. The maze start cell corresponds to walls[0], the cell immediately to the North is walls[1] and, for a 16x16 maze, the cell to the East of the start corresponds to walls[16]. Some people have a different ordering. Make ure that your choice matches that used here or strangeness will follow.

Each element holds information about all four walls for that cell. That means that allbut the outermost walls are stored twice. The class takes care of that duplication so you should not have to worry about it so long as you only use the provided methods to manipulate the walls.

Walls can have one of four states. Each can be present or absent and it can be unknown or known. By tracking whether walls are known - that is, they have been positively identified by the mouse - the code is able to easily detect when the maze has been explored enough to permit a safe, fast run from start to goal. You would not normally have to concern yourself with these states in detail, the code keeps track for you.

At initialisation, all the possible walls are marked as unknown. When your mouse wants to update the map, the updates are automatically marked as known walls or exits. A good side effect of this is that a wall state is never changed after it has been updated once. This is generally a benefit that can help avoid mapping errors.

You can query the state of the walls in a cell or of a single wall if you need to. the best way to do this is to think only in terms of whether there is an exit from a cell in a particular direction. After all, you want to know where the mouse _can_ go more that where it _cannot_.

### Flooding and Costs
Costs after flooding are stored in a list in just the same way as the wall information. The method used to flood the map is a very simple Manhattan Flood. This just counts the number of cells from one cell to another when moving only North, East, South or West. Diagonal moves are not used. This distance is called the **cost** for a given cell. The term cost is used rather than distance as a reminder that there other ways to find routes. You might, for instance, assign a larger cost to a turn compared to moving straight ahead since it will be slower and take more time. That is up to you and when you are ready to write your own flood method, you can look into the provided code for some clues. Meanwhile you can use the floding methods withut having to undertand how they work. All you need to know is that, after a flood, your can get the cost for any cell just by looking it up. For example, after a flood to the goal, the cost for the target cell will always be zero and the cost in the start cell will tell you the cost for a complete path to the goal. every accesible cell with have a cost and you can use the information to calculate and run a path to the tareget.

When flooding, you can set any cell as the target. After reaching the goal, for  instance, you would normally set the start cell as the target and perform floods to help you find your way back.

There are actually two flooding methods you should use. One is intended for use while searching and one is intended to let you find paths that are safe to run at speed as they will not pass through any unknown cells or walls. There is also a way to find out if you have found the shortest path yet - although it won't directly tell you what that path is. That is your job.

### Using the class

In your code, you must create an object of type Maze. Once that is done you can refer to it and its methods. there are examples at hte bottom of the `maze.py` file. You might, perhaps, have code like this:

```
maze = Maze()
maze.init_walls()
maze.update_wall(maze.cell_id(4,6),NORTH)
maze.flood(maze.get_goal())
```

These functions, and others are described below.

### Maze Functions

**Note that these functions have been tested (see `maze_tests.py`) but generally have no error checking or correction built in**

Here is a list of the functions that the MAze class makes available to you with a description of what they are for and suggestions about how to use them. Not every function is shown as some are meant to be internal to the class but Python does not provide a way to hide them. instead, the list shows the function you are most likely to actually call from the mouse.


**`cell_id(x,y)`** Calculates and returns the index number of a cell given its (x,y) coordinate pair. Cell (0,0) is the start cell in the bottom left, (0,1) is the cell immediately to its North. If you prefer to think of the maze as a 2D array, this lets you describe location that way.

**`cell_xy(index)`** will return a tuple containing the (x,y) location of a cell given its index number. This is effectivelly the opposite of `cell_id` and can be useful if you want to display a cell coordinate. Internally, only th eindex number is used to refer to cells.

**`get_goal()`** and **`set_goal(index)`** The maze flood regards only one cell as the legitimate goal. You may wish to change that for practice or testing for example. The default is to use the cell (7,7)

**`init_walls()`** will clear all the walls in the maze and then set the outside perimeter as having walls around the edge. It will then set the start cell to have a wall to the East and an exit to the North. Although an instace of the maze will normally be initialised in this way correctly, you might want to do this task manually.

**`set_walls_from_string(lines)`** In the file `maze_files.py` are two declarations for example mazes in a format that can be read by this function. The format is exactly the same as that used in the collection of maze files to be found here (https://github.com/micromouseonline/mazefiles). With this function, you can edit your own maze map with any text editor and have the maze loaded up for you to test out new software.

**`get_maze_string()`** will return a text object that contains lines, similar to those used in `maze_files.py` which are a text representation of the current map. In this way, you can easily print a visualisation of the maze or save it to a file. If you provide an optional argument, the visualisation will also contain the current value sin the cost table. For example

```
  str = maze.get_maze_string()                   ## creates a view with just the walls
  str = maze.get_maze_string(view = VIEW_COSTS)  ## creates a view with the walls and the costs 
  print(str)                                     ## prints that representation
```
Here is an example of the output from the version with costs after loading the Japan 2007 maze:

```
o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
| 43  42  41  40  39  38  37  36  35  34  33  32  31  30  29  28|
o   o---o---o---o---o---o---o---o---o---o---o---o---o---o---o   o
| 44| 45  44| 41  40| 37  36  35  34  33  32  31  30  29  28  27|
o   o   o   o   o   o   o---o---o---o---o---o---o   o---o   o   o
| 45  46| 43  42| 39  38| 39  38  37  36  35| 32  31| 28  29| 26|
o---o   o---o---o---o---o   o---o---o---o   o   o---o   o---o   o
| 48  47  48| 49| 48| 47| 40  41| 42  41| 34  33| 26  27| 18| 25|
o---o---o   o   o   o   o---o   o   o   o   o---o   o---o   o   o
| 55  54| 49| 48  47  46  45| 42| 43| 40| 35| 24  25| 18  17| 24|
o   o   o   o   o   o   o   o   o   o   o   o   o---o   o   o   o
| 56| 53| 50| 49| 48| 47| 44  43| 44| 39| 36| 23| 20  19| 16| 23|
o   o   o   o   o---o---o---o---o   o   o   o   o   o---o   o   o
| 57| 52  51| 50| 49  48  47  46  45| 38  37| 22  21| 14  15| 22|
o   o---o---o   o   o---o---o---o---o---o---o---o---o   o---o   o
| 58  59  60| 51| 50| 53  54|  1   2|  3|  4|  5| 12  13| 20  21|
o---o   o   o   o   o   o   o   o   o   o   o   o   o---o   o   o
| 61  60| 61| 52| 51  52| 55|  0   1   2   3   4| 11| 18  19| 22|
o   o---o   o   o---o   o   o---o---o   o---o   o   o   o---o   o
| 62  63| 62| 53  54| 53| 56  57| 60|  3   4|  5| 10| 17  16| 23|
o---o   o   o---o   o---o   o---o   o---o   o   o   o---o   o   o
| 65  64| 63  64| 55  56  57  58  59  60|  5|  6|  9| 14  15| 24|
o   o---o---o   o   o   o---o---o   o   o   o   o   o   o---o   o
| 66  67| 68| 65| 56| 57  58  59| 60| 61|  6|  7   8| 13  12| 25|
o---o   o   o   o---o---o---o   o---o   o   o   o---o---o   o   o
| 69  68| 67  66| 69| 68| 67| 60  61| 62|  7|  8   9  10  11| 26|
o   o---o   o---o   o   o   o---o   o   o   o---o---o---o---o   o
| 70| 69  68| 69  68  67  66  65| 62| 63|  8   9  10  11  12| 25|
o   o   o   o   o   o   o   o   o   o   o---o---o---o---o   o   o
| 71  70| 69  70| 69| 68| 67| 64  63| 64| 17  16  15  14  13| 24|
o   o   o   o   o   o   o   o---o   o   o   o---o---o---o---o   o
| 72| 71  70| 69  68  67  66  65  64  65| 18  19  20  21  22  23|
+---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
```

**`update_wall(cell,direction,state)`** will set a wall for the given cell and direction where direction is one of `NORTH`, `EAST`, `SOUTH` or `WEST`. The state should be one of `WALL_PRESENT` or `WALL_ABSENT`. The function takes care of setting the adjacent wall as needed to keep the maze consistent. Once a wall has be set, it can no longer be changed by this method. That is the normal way that mapping is done during exploration. If you do need to unconditionally set a wall state, use the `set_wall_state()` method. 

**`cell_has_exit(cell, direction)`** returns `True` is there is an exit for the given cell in the supplied direction and`False` if not. Normally this is all you need to generate paths for your robot or to implement new flooding rourines. It is generally better to worry about where your robot __can__ go than where it cannot. However, if you absolutely must know about the walls, there is a corresponding method called `cell_has_wall(cell, direction)`.

**`cell_is_visited(cell)`** will return `True` if all of the walls in a cell have been updated. You do not have to actually visit the cell physically, just update all of the walls. Normally this is rare but could happen if you drive around the outside of a cell and get to see all of the walls. This method can be used when plotting paths to make sure you do not stray into the wilderness or to find unknown cells during the search. For creating speed runs, there a way to guarantee that you cannot pass through unknown cells by using the special flood method `flood_for_speed_run()' - see below.

**`neighbour(cell, direction)`** returns the index of the adjacent cell in the given direction. You are likely to want this utility when planning a route through the maze or when searching to update the location of the mouse.

**`direction_to_smallest(cell,direction)`** When searching the maze, or creating a possible speed run path, you will want to know which way to go to find the cell closest to the goal. The method will scan the costs for all four cells around the given cell, and return the direction to the one with hte least cost. By passing in a direction, you tell the method to look in that direction first, then to the left and right in order and finally to the rear in case you are in a dead end. The method will not look through walls, so the direction you get back will be a valid direction for movement. You must flood the maze before calling this method or you will get nonsense back.

**`flood_for_search(target)`** Given a target cell to aim for, this helper method will flood the maze in such a way as to assume that any walls you have not yet seen are **assumed to be absent**. Thus is tries to find the most optimistic but unsafe distance to the target. Each cell is filled witha number representing the Manhattan distance to the target. Cells that are to reachable will have a cost of 256 (for the 16x16 maze). The target cell will have a cost of zero You can examine the cost of any cell directly by looking at the value in `maze.cost[cell]`. After using this method, there may still be unknown walls on what appears to be a good path so you need to proceed with caution, mapping as you go.

**`flood_for_speed_run(target)`** Similar to the previous helper but only for use when you have found the goal. Given a target cell to aim for, this helper method will flood the maze in such a way as to assume that any walls you have not yet seen are **assumed to be present**. Thus is tries to find the most pessimistic but safe distance to the target. Each cell is filled witha number representing the Manhattan distance to the target. Cells that are to reachable will have a cost of 256 (for the 16x16 maze). The target cell will have a cost of zero. You can examine the cost of any cell directly by looking at the value in `maze.cost[cell]`. After calling this method, you may safely follow the flooded values to the goal secure in the knowledge that you will not encounter any unknown walls.



**`flood(target)`** This is the core that makes the magic happen when exploring or creating a path for a speed run. You can use this method directly but it is better to use the two helpers just described. Both call this method which performs some internal magic to get the right result. Only worry about how the magic works when you are ready to. If you are the kind of person who must know their car engine works, this may suit you. If you just want to get to the beach, there is no need to open the bonnet. The code in this flood has been written for the best performance. On a stock Raspberry Pi Pico it should run in under 15 milliseconds. If you can make it faster, let the authors know. 
