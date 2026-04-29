from tkinter import *
from Util import *

class Pile:
    def __init__(self, board):
        self.board = board
        self.pile = []


    def size(self):
        return len(self.pile)

    def top(self):
        # Assert pile not empty?
        return self.pile[-1]

    def add(self, card):
        self.pile.append(card)

    def pop(self):
        # Assert pile not empty?
        self.pile.pop()

    def place_anchor(self):
        self.anchor = Label(self.board, name="anchor", text="Anchor", width=10, height=10,bg='grey')
        self.anchor.place(x=500, y=100)
        self.anchor.bind("<Enter>", self.hover)
        self.anchor.bind("<Leave>", self.unhover)


    def hover(self, event):
        self.get_child_at(event)
        print("Anchor:" + str(event))

    def get_child_at(self, event):
        name = event.widget.winfo_name()
        cords = Util.standardize_event_coords(event)
        print(name + str(cords['x']) + str(cords['y']))
        # now get the children

        children = self.board.winfo_children()

        self.board.master.update_idletasks()
        children = self.board.winfo_containing(cords['x'], cords['y'])
        print(children)

    def unhover(self, event):
        print("Anchor:" + str(event))