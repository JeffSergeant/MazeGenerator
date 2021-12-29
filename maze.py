import numpy as np
import random
from enum import Enum


class BranchingMethod(Enum):
    FIRST = 0
    LAST = 1
    RANDOM = 2


class Maze:
    longest_route = 0
    last_cell = None
    route = []

    def __init__(self, maze_width, maze_height, starting_position=(0,0), branching_method=BranchingMethod.FIRST):
        self.maze = np.zeros((maze_width, maze_height), MazeCell)
        self.branching_method = branching_method

        for x in range(0, maze_width):
            for y in range(0, maze_height):
                self.maze[x, y] = MazeCell((x, y), self.maze)

        for cell in self.maze.flat:
            cell.get_neighbours()

        self.create_maze(starting_position)

    def create_maze(self, starting_position):
        starting_x, starting_y = starting_position
        self.maze[starting_x][starting_y].start = True
        current_cell = self.maze[starting_x][starting_y]
        self.route = [current_cell]

        while current_cell:
            prev_distance = current_cell.distance
            # if our last iteration found a cell, add it to the route and find the next one
            self.route.append(current_cell)
            current_cell = current_cell.get_next_cell()
            # if we don't find a next cell, we've reached the end of the path, backtrack until we find a route
            if not current_cell:
                current_cell = self.backtrack()

            else:
                distance = prev_distance + 1
                current_cell.distance = distance
                if distance > self.longest_route:
                    self.last_cell = current_cell
                    self.longest_route = distance

        self.last_cell.end = True

    def backtrack(self):
        """
        For a given route, identify a cell with empty neighbours:
        RANDOM picks a random cell to restart from,
        FIRST finds the earliest cell with unvisited neighours,
        LAST finds the last cell with unvisited neighours
        """
        self.route = [c for c in self.route if not c.done]

        if self.branching_method == BranchingMethod.RANDOM:
            for i, n in enumerate([cell for cell in self.route if not cell.done]):
                if n.count_empty_neighbours():
                    return n

        elif self.branching_method == BranchingMethod.FIRST:
            for i, n in enumerate(self.route):
                if n.count_empty_neighbours():
                    return n

        elif self.branching_method == BranchingMethod.LAST:
            for i, n in enumerate(self.route[::-1]):
                if n.count_empty_neighbours():
                    return n

        else:
            raise NotImplementedError('Branching Method Not Implemented')

    def solve(self):
        next_cell = self.last_cell
        distance = next_cell.distance
        while distance > 1:
            next_cell = min([cell for direction,cell in next_cell.neighbours.items() if cell is not None and next_cell.exits[direction]])
            next_cell.onroute = True
            distance = next_cell.distance

    def __str__(self):
        string = ''
        for r, row in enumerate(self.maze):
            printable=['','','']
            for cell in row:
                cell_printable = cell.printable()
                for i,printable_row in enumerate(cell_printable):
                    printable[i] += printable_row
            if r == 0:
                string += '\n'.join(printable)+'\n'
            else:
                string += '\n'.join(printable[1:3])+'\n'
        return string


class MazeCell:
    def __init__(self, position, maze):
        self.position = position
        self.exits = {"left": 0, "down": 0, "up": 0, "right": 0}
        self.neighbours = {"left": None, "down": None,"right": None, "up": None }
        self.maze = maze
        self.start = False
        self.end = False
        self.distance = 0
        self.onroute = False
        self.unvisited = True
        self.done = False

    def printable(self):
        up = ' ' if self.exits['left'] else '-'
        down = ' ' if self.exits['right'] else '-'
        left = ' ' if self.exits['up'] else '|'
        right = ' ' if self.exits['down'] else '|'

        printable = [f'+{up}+']
        printable.append(f'{left}{"X" if self.start else "O" if self.end else "." if self.onroute else " "}{right}')
        printable.append(f'+{down}+')

        if self.position[1] > 0:
            printable = [p[1:3] for p in printable]

        return printable

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
            [n for n in self.neighbours.values() if n is not None and n.unvisited])
        if number_of_neighbours == 0:
            self.done = True
        return number_of_neighbours

    def get_next_cell(self):
        self.unvisited = False
        valid_neighbours = [n for n in self.neighbours.values() if n is not None and n.unvisited]

        if valid_neighbours:
            return self.add_random_neighbour(valid_neighbours)

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

    def  __gt__(self,other):
        return self.distance>other.distance

    def  __lt__(self,other):
        return self.distance<other.distance


if __name__ == '__main__':
    import time


    for branching_method in BranchingMethod:
        start = time.time()
        print(f"\n***{branching_method}***\n")
        maze = Maze(100,250,branching_method=branching_method)
        end = time.time()
        maze.solve()
        starts = len([cell for cell in maze.maze.flat if cell.start])
        ends = len([cell for cell in maze.maze.flat if cell.end])
        unvisited = len([cell for cell in maze.maze.flat if cell.unvisited])
        print(f'{branching_method} {starts} starts, {ends} ends, {unvisited} unvisited. {end - start}, "seconds")')
        print(str(maze)[0:2000])
        assert starts == 1 and ends == 1 and unvisited == 0



