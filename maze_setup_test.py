import unittest
import mazehandling as mh


class TestMazeSetup(unittest.TestCase):

    def test_maze_size(self):
        cell_size = 50
        maze_width = 10
        maze_height = 10

        maze = mh.setup_maze(cell_size, maze_width, maze_height)

        self.assertEqual(maze.size, (maze_width * maze_height))

    def test_maze_neighbours(self):
        cell_size = 10
        maze_width = 10
        maze_height = 10

        maze = mh.setup_maze(cell_size, maze_width, maze_height)
        cell = maze[0][0]
        number_of_neighbours = len([n for n in cell.neighbours.values() if n is not None and n.empty])

        self.assertEqual(2, number_of_neighbours)


if __name__ == '__main__':
    unittest.main()
