from Scenes.MenuScene import MenuScene
from Scenes.MazeScene import MazeScene

if __name__ == '__main__':

    scene = MenuScene(MazeScene)
    game_running = scene.initialise()

    while game_running:
        game_running = scene.update()
        if not game_running:
            scene = scene.close()
            if scene:
                game_running = scene.initialise()

