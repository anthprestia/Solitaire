from tkinter import *
from Util import *
from BoardManager import *

class GameHUB:
    def __init__(self):
        self.name = 'GameHUB'
        self.author = 'Anthony Prestia'

        # Establish window and window settings
        self.root = Tk()

        # figure out window width and size cuz they're mismatched
        # i input 1000x800 but it says 200x200 so whats up with that?
        self.window_width = 800
        self.window_height = 800
        self.root.geometry(str(self.window_width) + "x" + str(self.window_height))
        self.root.resizable(width=False, height=False)

        self.root.title("GameHUB")
        self.root.bind("<Motion>", self.updateCoords)

        self.root.update()

        var = self.root.size()

        # Maybe replace with game chooser or something
        self.start_app()

        self.root.mainloop()

    def start_app(self):
        # Load a game
        # AKA load a solitare board
        # Create a Board Manager
        # Board Manager will create the Solitare board internally

        i_want_to_speak_to_the = BoardManager(self.root)



    def updateCoords(self,event):
        cords = Util.standardize_event_coords(event)

        if self.withinBounds([event.x, event.y]):
            self.root.title("GameHUB - Mouse pos x: " + str(cords['x']) + " y: " + str(cords['y']))

    # Check if [x,y] coordinates are within the bounds of the screen
    def withinBounds(self, cords):
        window_x,window_y = self.root.winfo_width(), self.root.winfo_height()

        if 0 <= cords[0] <= window_x and 0 <= cords[1] <= window_y:
            return True
        else:
            return False



def main():
    app = GameHUB()

if __name__ == '__main__':
    main()