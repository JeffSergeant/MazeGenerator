
class IScene:
    def __init__(self,args):
        pass

    def initialise(self):
        """Initialises the scene, returns whether or not the scene should play"""
        return False

    def update(self):
        """Runs during the main game loop, returns false on completion."""
        return False

    def close(self):
        """closes the scene, returns next scene to play, or None"""
        pass
