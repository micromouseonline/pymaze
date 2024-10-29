# pymaze

A Maze class for micromouse robots running MicroPython

For those people building a micromouse and wanting to program it in Python - specifically 
MicroPython - there are many challenges. One of those is to store a map of the maze that can be updated and flooded in an efficient manner. Python is not known for its high performance and it is not always obvious how to get the best speed out of your code.

Depending on how you structure your micromouse code, it can be especially important to flood the maze map as quickly as possible. The method used in the example code described here can perform a flood of an empty maze in about 14ms when running on a stock Raspberry Pi Pico board. By comparison, the code proposed by CoPilot took 1.3 seconds.

## Implementations

There are two separate but similar implementations included in this repository. In terms of the basic flood of the maze, both implementations take the same approach and use a well established algorithm that can be found in many other examples. Except CoPilot of course :)

 - **Inline Code**
An implementation by David Hannaford (`maze_dh.py`) that is intended to be simply included in your main Python application gives you a way to perform a flood of the stored maze map. It purposely concerns itself almost entirely with that function though there are also functions that let you see the wall and flood data on a terminal. This code is only meant to run under micropython. 


 - **Maze Class**
The other implementation (`maze.py`) is intended to be a more complete implementation of all the functions needed to allow you to map, store and flood a micromouse maze. Although normally used as part of a multi-file Python application, the class definition and associated constants could be copied into a single-file application and used there. this is a more complex implementation because it provides additional functionality. However, if you look at the `flood()` method you will see that it uses essentially the same algorithm as the other example. The following text describes this Maze class in more detail

---

## Files

There are several files in the repository. You should need only the `maze.py` file for your project. The other files provide some support and testing functions for development on a PC.


### `maze.py`
This contains the Maze class that you add to your project along with some definitions for constants and a couple of utilities related to pathfinding. You can keep it as a single file or add just the code into your main python script if that is the way you are set up. See below for details of the methods provided by the Maze class

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

### Maze Functions

Here s a list of the functions available to you with a description of what they are for and suggestions about how to use them. Not every function is shown as some are meant to be internal to the class byt Python does not provide a way to hide them. instead, the list shows the function you are most likely to actually call from the mouse.



