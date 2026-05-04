from tkinter import *
from Card import *
from Pile import *
from Util import *
from Config import *

# Data class representing the visual mapping of the board
#            and holding values of cards in each of the piles
class SolitaireBoard:
    def __init__(self, gameframe):
        self.gameframe = gameframe
        # We want to work within a Frame for easier use
        self.board = Canvas(self.gameframe, name='solitaire', bg='green')
        # expand to the size of the window.. **might need to change to accomodate dynamic sizing
        self.board.pack(expand=True, fill="both")
        self.board.update()

        self.board.bind('<1>', self.under)

        # dict of piles on the board KEY = Canvas ObjectId
        self.pile_list = {}

        self.configureGameBoard()

        #deck = Deck(self.board)

    def configureGameBoard(self):
        # Build the game board
        # define the bounds of the game
        # - how big are cards
        # - Reserve space for different piles
        #   - Collection
        #   - Stock
        #   - Drawn

        # top row
        stock_x = Config.outer_padding
        stock_y = Config.outer_padding
        stock = Pile(self, stock_x, stock_y, 'stock')
        self.pile_list[stock.get_id()] = stock

        waste_x = stock_x + Config.card_width + Config.inner_padding
        waste_y = Config.outer_padding
        waste = Pile(self, waste_x, waste_y, 'waste')
        self.pile_list[waste.get_id()] = waste

        w = self.board.winfo_width()

        # Setup foundation piles
        for f in range(1,5):
            x_cord = w - (Config.outer_padding + (Config.card_width * f) + (Config.inner_padding * (f-1)))
            y_cord = Config.outer_padding

            pile = Pile(self, x_cord, y_cord, 'foundation'+str(f - 5))
            self.pile_list[pile.get_id()] = pile

        # Setup tableu piles
        for p in range(1, 8):
            x_cord = ((Config.card_width + Config.inner_padding) * (p-1)) + Config.outer_padding
            y_cord = Config.outer_padding + Config.card_height + Config.inner_padding

            pile = Pile(self, x_cord, y_cord, 'tableu'+str(p))
            self.pile_list[pile.get_id()] = pile

    def under(self, event):
        print(str(event))
        #what pile, if any, was clicked on?
        # get the objects at point (e.x,e.y), sorted by lowest to highest (number-wise or focus? idk)
        object_list = self.board.find_overlapping(event.x, event.y,
                                                  event.x, event.y,)

        if (len(object_list) > 0) and self.pile_list.__contains__(object_list[0]):
            print(self.pile_list.get(object_list[0]).get_name())
        else:
            print("NO PILE")

    def on_drag(self, event):
        widget = event.widget
        x = widget.winfo_x() - self.drag_data["x"] + event.x
        y = widget.winfo_y() - self.drag_data["y"] + event.y
        widget.place(x=x, y=y)

    def get_board(self):
        return self.board

    def refresh_sizeing(self):
        # Math for dynamic sizing:
        # Piles should be the same size as cards. Cards should be ~10% of total canvas width
        # Outer padding should each be about 5%
        # Inner padding should each be about 3-4%
        # Height can be negotiable depending on how we handle going off screen.
        # Card ratio should be about w:h; 1.2 -> 1.5
        return True