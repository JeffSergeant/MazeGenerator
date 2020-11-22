import pygame
import numpy as np
import random
import sys


class MazeCell:
    def __init__(self, position, maze):
        self.position = position
        self.exits = {"left": 0, "down": 0, "up": 0, "right": 0}
        self.empty = True
        self.next = None
        self.neighbours = {"left": None, "down": None, "up": None, "right": None}
        self.maze = maze
        self.stale = False

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

    def add_to_route(self, route, maze):

        self.empty = False
        self.stale = True

        neighbouring_cells = [n for n in self.neighbours.values() if n is not None]

        for number_of_neighbours in reversed(range(0, 4)):

            valid_neighbours = [n for n in neighbouring_cells if n.empty and n.count_empty_neighbours() <= number_of_neighbours]
            #valid_neighbours = [n for n in neighbouring_cells if n.empty]

            if valid_neighbours:
                return self.add_random_neighbour(valid_neighbours)

    def add_random_neighbour(self, valid_neighbours):
        neighbour = random.choice(valid_neighbours + [valid_neighbours[0]])

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


def setup_maze(cell_size, maze_width, maze_height):
    maze = np.zeros((maze_width, maze_height), MazeCell)

    for x in range(0, maze_width):
        for y in range(0, maze_height):
            maze[x, y] = MazeCell((x, y), maze)

    for cell in maze.flat:
        cell.get_neighbours()

    return maze


def initialise_route(maze, starting_x, starting_y):
    next_cell = maze[starting_x][starting_y]
    return [next_cell]


def backtrack(route, random_branch=False):
    nonempty_cells = [n for n in route if n.count_empty_neighbours()]
    if nonempty_cells:
        if random_branch:
            return random.choice(nonempty_cells)
        else:
            return nonempty_cells[0]


