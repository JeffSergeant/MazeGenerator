import numpy as np
import random
from enum import Enum


def test_prime(candidate):
    if candidate < 2:
        return False

    for divisor in range(2, round(candidate / 2)):
        if candidate / divisor == int(candidate / divisor):
            return False
    return True


class MazeWrapper:
    def __init__(self):
        self.nextNumber = 1
        self.f = open("c:\\test\\primes.txt", "r")
        primes_list = [int(n) for n in self.f.readlines()]
        self.max_prime = primes_list[-1]
        self.primes = set(primes_list)

    def test_prime(self, x):
        if x <= self.max_prime:
            return x in self.primes
        else:
            raise Exception("Not Enough Primes")


class MazeCell:
    def __init__(self, position, maze, mazewrapper):
        self.position = position
        self.exits = {"left": 0, "down": 0, "up": 0, "right": 0}
        self.empty = True
        self.next = None
        self.neighbours = {"left": None, "down": None,"right": None, "up": None }
        self.maze = maze
        self.stale = False
        self.mazewrapper = mazewrapper
        self.start = False

    def get_neighbours(self):
        x, y = self.position
        max_x, max_y = self.maze.shape

        if x > 0:
            self.neighbours["left"] = self.maze[x - 1][y]

        if y > 0:
            self.neighbours["up"] = self.maze[x][y - 1]

        if x + 1 < max_x:
            self.neighbours["right"] = self.maze[x + 1][y]

        if y + 1 < max_y:
            self.neighbours["down"] = self.maze[x][y + 1]

    def count_empty_neighbours(self):

        number_of_neighbours = len(
            [n for n in self.neighbours.values() if n is not None and n.empty])

        return number_of_neighbours

    def add_to_route(self, route, maze, prime_counter=2):

        self.empty = False
        self.stale = True

        neighbouring_cells = [n for n in self.neighbours.values() if n is not None]

        for number_of_empty_neighbours in reversed(range(0, 4)):

            valid_neighbours = [n for n in neighbouring_cells if n.empty and n.count_empty_neighbours() <= number_of_empty_neighbours]
            #valid_neighbours = [n for n in neighbouring_cells if n.empty]

            if valid_neighbours:
                return self.add_random_neighbour(valid_neighbours)
                #return self.add_neighbour_prime(valid_neighbours)

    def add_random_neighbour(self, valid_neighbours, neighbour=None):

        if not neighbour:

            neighbour = random.choice(valid_neighbours)

        if neighbour == self.neighbours["left"]:
            self.exits["left"] = 1
            neighbour.exits["right"] = 1
        if neighbour == self.neighbours["right"]:
            self.exits["right"] = 1
            neighbour.exits["left"] = 1
        if neighbour == self.neighbours["up"]:
            self.exits["up"] = 1
            neighbour.exits["down"] = 1
        if neighbour == self.neighbours["down"]:
            self.exits["down"] = 1
            neighbour.exits["up"] = 1
        return neighbour

    def add_neighbour_prime(self, valid_neighbours):
        while True:

            for neighbour in valid_neighbours:
                self.mazewrapper.nextNumber = (self.mazewrapper.nextNumber + 2)
                if self.mazewrapper.test_prime(self.mazewrapper.nextNumber) and neighbour:
                    return self.add_random_neighbour(valid_neighbours, neighbour)


def setup_maze(cell_size, maze_width, maze_height,mazewrapper):
    maze = np.zeros((maze_width, maze_height), MazeCell)

    for x in range(0, maze_width):
        for y in range(0, maze_height):
            maze[x, y] = MazeCell((x, y), maze,mazewrapper)

    for cell in maze.flat:
        cell.get_neighbours()

    return maze


def initialise_route(maze, starting_x, starting_y):
    next_cell = maze[starting_x][starting_y]
    return [next_cell]


class BranchingMethod(Enum):
    FIRST = 0
    LAST = 1
    RANDOM = 2


def backtrack(route, branching_method):
    """For a given route, identify a cell with empty neighbours:
    RANDOM picks a random cell, FIRST finds the earliest, LAST finds the last"""
    nonempty_cells = [n for n in route if n.count_empty_neighbours()]
    if nonempty_cells:
        if branching_method == BranchingMethod.RANDOM:
            return random.choice(nonempty_cells)
        elif branching_method == BranchingMethod.FIRST:
            return nonempty_cells[0]
        elif branching_method == BranchingMethod.LAST:
            return nonempty_cells[-1]
