from Scenes.IScene import IScene

import pygame
from maze import Maze


class MazeScene(IScene):
    def __init__(self, args, next_scene):
        self.args = args

        self.cell_size = args["cell_size"]
        self.maze_height = args["maze_height"]
        self.maze_width = args["maze_width"]
        self.branching_method = args["branching_method"]
        self.margin = 10

        self.game_window = self.setup_window()

        self.next_cell = None
        self.next_scene = next_scene
        self.maze = []
        self.route = []

    def initialise(self):
        pygame.init()
        self.game_window.fill((255, 255, 255))
        self.draw_maze(0, 0)

        return True

    def update(self):
        # called once per game-loop

        for event in pygame.event.get():
            # If the user presses the 'X', return false so the runner knows we're done
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # draw a new maze where the user clicked
                #if self.next_cell is None:
                self.create_maze_on_mouseclick()

        # Draw as many cells as we can in 1/30th of a second, the human eye can't see more than 30 fps anyway
        start_time = pygame.time.get_ticks()

        self.game_window.fill((255, 255, 255))
        self.draw_walls_from_maze()

        pygame.display.update()
        return True

    def create_maze_on_mouseclick(self):

        clicked_location = pygame.mouse.get_pos()
        x = ((clicked_location[0]-self.margin) // self.cell_size)
        y = ((clicked_location[1]-self.margin) // self.cell_size)
        # if the click is outside the maze size, start from origin

        x = min(x, self.maze_width-1)
        y = min(y, self.maze_height-1)

        self.draw_maze(x, y)

    def draw_maze(self, x, y):
        self.game_window.fill((255, 255, 255))
        self.maze = Maze(self.maze_width, self.maze_height, (x,y),self.branching_method)

    def draw_walls_from_maze(self):
        # find all cells in the maze that are non-empty and need re-drawing
        for cell in [x for x in self.maze.maze.flat]:
            self.draw_walls_from_cell(cell)

    def draw_walls_from_cell(self, cell):
        exit_colour = (255, 255, 255)
        wall_colour = (0 , 0 , 0 )

        # find edges of our cell in window-space

        left = cell.position[0] * self.cell_size + self.margin
        right = left + self.cell_size
        top = cell.position[1] * self.cell_size+ self.margin
        bottom = top + self.cell_size

        if cell.start:
            pygame.draw.circle(self.game_window,wall_colour,(left+self.cell_size/2,top+self.cell_size/2),self.cell_size/4)
        if cell.end:
            pygame.draw.circle(self.game_window,wall_colour,(left+self.cell_size/2,top+self.cell_size/2),self.cell_size/4)

        # work out our lines based on our edges
        lines = {}
        lines["right"] = [(right, top), (right, bottom)]
        lines["left"] = [(left, top), (left, bottom)]
        lines["up"] = [(left, top), (right, top)]
        lines["down"] = [(left, bottom), (right, bottom)]

        # clear out any existing lines
        #pygame.draw.rect(self.game_window,exit_colour,(left,top,self.cell_size,self.cell_size))

        for side in lines.keys():
            if not cell.exits[side]:
                pygame.draw.line(self.game_window, wall_colour, lines[side][0], lines[side][1], 2)

    def setup_window(self):

        window_width = self.maze_width*self.cell_size+self.margin*2
        window_height = self.maze_height*self.cell_size+self.margin*2

        pygame.display.set_caption(self.args["difficulty"] + " maze")
        window = pygame.display.set_mode((window_width, window_height))
        window.fill((255, 255, 255))

        return window

    def close(self):
        pygame.display.quit()
        return self.next_scene(MazeScene, self.args)
