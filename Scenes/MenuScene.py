from Scenes.IScene import IScene
import tkinter as tk
from tkinter import ttk
import maze

EASY={"difficulty":"easy","cell_size":25,"maze_width":15,"maze_height":15,"branching_method":maze.BranchingMethod.LAST}
MEDIUM={"difficulty":"medium","cell_size":25,"maze_width":25,"maze_height":25,"branching_method":maze.BranchingMethod.FIRST}
HARD={"difficulty":"hard","cell_size":10,"maze_width":50,"maze_height":50,"branching_method":maze.BranchingMethod.RANDOM}
MONSTER={"difficulty":"MONSTER","cell_size":5,"maze_width":250,"maze_height":150,"branching_method":maze.BranchingMethod.FIRST}

TEXT_BOX = 0
CHECK_BUTTON=1
DROPDOWN = 2
BUTTON = 3

difficulty = {"easy":EASY,"medium":MEDIUM,"hard":HARD,"MONSTER":MONSTER}


class MenuScene(IScene):
    def __init__(self, next_scene, args=difficulty["medium"]):

        self.next_scene = next_scene
        self.quit = False

        self.args = args

        self.root = tk.Tk()

        self.difficulty_selected = tk.StringVar()
        self.difficulty_selected.set(self.args["difficulty"])

        self.cell_size = tk.StringVar()
        self.cell_size.set(self.args["cell_size"])

        self.width = tk.StringVar()
        self.width.set(self.args["maze_width"])

        self.height = tk.StringVar()
        self.height.set(self.args["maze_height"])

        self.branching_method = tk.StringVar()
        self.branching_method.set(self.args["branching_method"].name)

    def initialise(self):

        self.root.title("Maze Menu")
        self.root.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        row = 0

        row = create_label_and_control(self.mainframe, 'Difficulty', DROPDOWN, self.difficulty_selected, row, list(difficulty.keys())
                                       , self.set_difficulty)

        options = [method.name for method in maze.BranchingMethod]
        row = create_label_and_control(self.mainframe, 'Branching Method:', DROPDOWN, self.branching_method, row,
                                       options)

        row = create_label_and_control(self.mainframe,'Cell Size (Pixels', TEXT_BOX,self.cell_size,row)
        row = create_label_and_control(self.mainframe, 'Maze Width:', TEXT_BOX, self.width, row)
        row = create_label_and_control(self.mainframe, 'Maze Height:', TEXT_BOX, self.height, row)
        row = create_label_and_control(self.mainframe, '', BUTTON, 'Create Maze', row,None,self.load_maze)

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
        args["branching_method"] = maze.BranchingMethod[self.branching_method.get()]
        args["difficulty"] = self.difficulty_selected.get()

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
        self.branching_method.set(args["branching_method"].name)

    def load_maze(self, closed = False):

        self.quit = True


def create_label_and_control(main,label,control_type,variable, row, options=[], command=None):

    label = ttk.Label(main, text=label)
    label.grid(column=1, row=row, sticky=(tk.W, tk.E))

    if control_type == CHECK_BUTTON:
        control = ttk.Checkbutton(main, width=7, variable=variable)

    elif control_type == DROPDOWN:
        control = tk.OptionMenu(main, variable, *options, command=command)

    elif control_type == BUTTON:
        control = tk.Button(main, text=variable, command=command)

    else:
        control = ttk.Entry(main, width=7, textvariable=variable)

    control.grid(column=2, row=row, sticky=(tk.W, tk.E))
    return row+1

