from tkinter import *
from Card import *
from Pile import *
from Util import *

# Data class representing the visual mapping of the board
#            and holding values of cards in each of the piles
class SolitaireBoard:
    def __init__(self, root):
        self.root = root
        # We want to work within a Frame for easier use
        self.board = Frame(self.root, name='solitare', bg='light blue')
        # expand to the size of the window.. **might need to change to accomodate dynamic sizing
        self.board.pack(expand=True, fill="both")

        self.configureGameBoard()

        deck = Deck(self.board)

        pile = Pile(self.board)
        pile.place_anchor()


    def configureGameBoard(self):
        # Build the game board
        # define the bounds of the game
        # - how big are cards
        # - Reserve space for different piles
        #   - Collection
        #   - Stock
        #   - Drawn
        #   - playable (find name)
        return True