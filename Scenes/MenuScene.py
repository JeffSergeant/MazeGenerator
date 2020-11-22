from Scenes.IScene import IScene


from tkinter import *
from tkinter import ttk

EASY={"difficulty":"easy","cell_size":25,"maze_width":15,"maze_height":15}
MEDIUM={"difficulty":"medium","cell_size":25,"maze_width":25,"maze_height":25}
HARD={"difficulty":"hard","cell_size":10,"maze_width":50,"maze_height":50}
MONSTER={"difficulty":"MONSTER","cell_size":5,"maze_width":250,"maze_height":150}

difficulty = {"easy":EASY,"medium":MEDIUM,"hard":HARD,"MONSTER":MONSTER}


class MenuScene(IScene):
    def __init__(self, next_scene,args=None):
        self.args = args
        self.next_scene = next_scene
        self.quit = False

    def initialise(self):
        self.root = Tk()
        self.root.title("Maze")

        self.root.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)


        self.difficulty_selected = StringVar()
        self.difficulty_selected.set(list(difficulty.keys())[0])

        self.dropdown = OptionMenu(self.mainframe,self.difficulty_selected, *list(difficulty.keys()),command=self.set_difficulty)
        self.dropdown.grid(row=0, column=1)

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

        ttk.Button(self.mainframe, text="Generate Maze", command=self.load_maze).grid(column=2, row=4, sticky=W)

        self.args = difficulty["medium"] if not self.args else self.args
        self.difficulty_selected.set(self.args["difficulty"])
        self.cell_size.set(self.args["cell_size"])
        self.width.set(self.args["maze_width"] )
        self.height.set(self.args["maze_height"])

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
        args["difficulty"] = self.difficulty_selected.get()

        # print (args)
        self.root.destroy()
        if self.next_scene:
            return self.next_scene(args, MenuScene)

    def window_closed(self):
        self.next_scene=None
        self.quit =True

    def set_difficulty(self,value):
        args = difficulty[value]
        self.cell_size.set(args["cell_size"])
        self.width.set(args["maze_width"])
        self.height.set(args["maze_height"])

    def load_maze(self, closed = False):

        self.quit = True

