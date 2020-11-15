import pygame
import mazehandling as mh
import numpy as np
import random
import sys


def draw_walls_from_maze(maze_array):
    maze_array[0][0].exits["up"] = True
    maze_array[maze_width - 1][maze_height - 1].exits["right"] = True

    for x in range(0, maze_width):
        for y in range(0, maze_height):
            cell = maze_array[x][y]

            left = x * cell_size + 5
            right = left + cell_size
            top = y * cell_size
            bottom = top + cell_size

            corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
            if not cell.exits["right"]:
                pygame.draw.line(game_window, (0, 0, 0), (right, top), (right, bottom), 2)
            if not cell.exits["left"]:
                pygame.draw.line(game_window, (0, 0, 0), (left, top), (left, bottom), 2)
            if not cell.exits["up"]:
                pygame.draw.line(game_window, (0, 0, 0), (left, top), (right, top), 2)
            if not cell.exits["down"]:
                pygame.draw.line(game_window, (0, 0, 0), (left, bottom), (right, bottom), 2)


def setup_window(cell_size, maze_width, maze_height):
    pygame.init()

    window_width = cell_size * maze_width + 15
    window_height = cell_size * maze_height + 15

    pygame.display.set_caption("Maze Window")
    window = pygame.display.set_mode((window_width, window_height))
    window.fill((0, 0, 0))

    return window


if __name__ == '__main__':
    cell_size = 20
    maze_height = 1000 // cell_size
    maze_width = 1500 // cell_size

    game_window = setup_window(cell_size, maze_width, maze_height)
    game_running = True

    maze = mh.setup_maze(cell_size, maze_width, maze_height)

    next_cell = None

    while game_running:

        # Loop through all active events
        for event in pygame.event.get():
            # Close the program if the user presses the 'X'
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_cell is None:
                    maze = mh.setup_maze(cell_size, maze_width, maze_height)
                    route = []

                    clicked_location = pygame.mouse.get_pos()
                    x = clicked_location[0] // cell_size
                    y = clicked_location[1] // cell_size
                    print(clicked_location, x, y)
                    route = mh.initialise_route(maze,x,y )
                    next_cell = route[0]

        if next_cell:

            next_cell = next_cell.add_to_route(route, maze)
            if not next_cell:
                next_cell = mh.backtrack(route,random_branch=True)

            route.append(next_cell)

        game_window.fill((255, 255, 255))
        draw_walls_from_maze(maze)

        pygame.display.update()
