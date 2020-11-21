from Scenes.IScene import IScene
from Scenes.MazeScene import MazeScene

from tkinter import *
from tkinter import ttk

class MenuScene(IScene):
    def __init__(self):
        pass

    def initialise(self):
        self.root = Tk()
        self.root.title("Feet to Meters")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.cell_size = StringVar()


        size_label = ttk.Label(self.mainframe, text="Cell Size (pixels)")
        size_label.grid(column=1, row=1, sticky=(W, E))

        size_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.cell_size)
        size_entry.grid(column=2, row=1, sticky=(W, E))

        self.width = StringVar()


        width_label = ttk.Label(self.mainframe,text="Maze Width:")
        width_label.grid(column=1, row=2, sticky=(W, E))

        width_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.width)
        width_entry.grid(column=2, row=2, sticky=(W, E))

        self.height = StringVar()

        height_label = ttk.Label(self.mainframe, text="Maze Height")
        height_label.grid(column=1, row=3, sticky=(W, E))

        height_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.height)
        height_entry.grid(column=2, row=3, sticky=(W, E))

        ttk.Button(self.mainframe, text="Generate Maze", command=self.quit).grid(column=2, row=4, sticky=W)
        self.quit = False

        self.cell_size.set(10)
        self.width.set(100)
        self.height.set(50)

        return True

    def update(self):
        if not self.quit:
            self.mainframe.update()

            return True
        return False

    def close(self):
        args = {}
        args["cell_size"] = int(self.cell_size.get())
        args["maze_width"] = int(self.width.get())
        args["maze_height"] = int(self.height.get())
        # print (args)
        scene = MazeScene(args)
        self.root.destroy()
        return scene

    def quit(self):

        self.quit =True
