from Scenes.IScene import IScene
import pygame
import mazehandling as mh

class MazeScene(IScene):
    def __init__(self,args):
        self.cell_size = args["cell_size"]
        self.maze_height = args["maze_height"]
        self.maze_width = args["maze_width"]
        self.game_window = self.setup_window(self.cell_size, self.maze_width, self.maze_height)
        self.maze = mh.setup_maze(self.cell_size, self.maze_width, self.maze_height)
        self.next_cell = None
        self.counter = 0

    def initialise(self):
        pygame.init()
        self.game_window.fill((255, 255, 255))

        return True

    def update(self):
        # Loop through all active events

        for event in pygame.event.get():
            # Close the program if the user presses the 'X'
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_cell is None:  # If we're not currently drawing a maze, draw a new one where the user clicked
                    self.maze = mh.setup_maze(self.cell_size, self.maze_width, self.maze_height)
                    self.route = []
                    self.game_window.fill((225, 225, 225))

                    clicked_location = pygame.mouse.get_pos()
                    x = (clicked_location[0] // self.cell_size)-1
                    y = (clicked_location[1] // self.cell_size)-1

                    if x < self.maze_width and y < self.maze_height:
                        route = mh.initialise_route(self.maze, x, y)
                        self.next_cell = route[0]
#
        if self.next_cell:

            self.next_cell = self.next_cell.add_to_route(self.maze, self.route)

            if not self.next_cell:
                self.next_cell = mh.backtrack(self.route, random_branch=False)

            self.route.append(self.next_cell)

        #self.game_window.fill((255, 255, 255))
        self.counter += 1
        if not self.counter % int((self.maze_width*self.maze_height)*0.01):
            self.draw_walls_from_maze()
            self.counter =0

        pygame.display.update()
        return True

    def draw_walls_from_maze(self):
        self.maze[0][0].exits["up"] = True
        self.maze[self.maze_width - 1][self.maze_height - 1].exits["right"] = True

        for cell in [x for x in self.maze.flat if not x.empty and x.stale]:
            self.draw_walls_from_cell(cell)
            cell.stale = False

    def draw_walls_from_cell(self, cell):

        left = cell.position[0] * self.cell_size + self.cell_size
        right = left + self.cell_size
        top = cell.position[1] * self.cell_size+self.cell_size
        bottom = top + self.cell_size

        exit_colour = (245  ,245, 245)
        wall_colour = (25   ,25 , 25 )

        corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
        lines = {}
        lines["right"]= [(right, top), (right, bottom)]
        lines["left"] = [(left, top), (left, bottom)]
        lines["up"] = [(left, top), (right, top)]
        lines["down"] = [(left, bottom), (right, bottom)]

        pygame.draw.rect(self.game_window,exit_colour,(left,top,self.cell_size,self.cell_size))

        for side in lines.keys():
            if not cell.exits[side]:
                pygame.draw.line(self.game_window, wall_colour, lines[side][0], lines[side][1], 2)

        #pygame.draw.rect(self.game_window,colour,(left,top,self.cell_size,self.cell_size))

    def setup_window(self,cell_size, maze_width, maze_height):
        pygame.init()

        window_width = maze_width*cell_size+cell_size*2
        window_height = maze_height *cell_size+cell_size*2

        pygame.display.set_caption("Maze Window")
        window = pygame.display.set_mode((window_width, window_height))
        window.fill((255, 123, 69))

        return window

    def close(self):
        pygame.display.quit()
        return None