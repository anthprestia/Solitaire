# This class is responsible for establishing the bounds of the elements on the board
# This includes keeping track dynamically of how large the game piles get
# AKA Dealer

# The 'Board' is a map that the manager uses to decide what to do with cards
from SolitaireBoard import *

class BoardManager:
    def __init__(self, root):
        self.root = root
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        self.gameframe = Frame(self.root, name='gameframe')
        self.gameframe.pack(expand=True, fill="both")
        self.gameframe.update()

        # board created
        self.board = SolitaireBoard(self.gameframe)

        # create a deck
        self.deck = Deck(self.board)

        # deal the cards from the deck to the board


# Deal the cards
    def deal_deck(self):
        return True
