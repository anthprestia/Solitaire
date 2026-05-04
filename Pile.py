from tkinter import *
from Util import *
from Config import *

# A Pile is a Stack of Cards
class Pile:
    def __init__(self, board, w_offset, h_offset, name=''):
        self.SolitaireBoard = board
        self.board = board.get_board()
        self.name = name
        # also x,y on canvas
        self.w_offset = w_offset
        self.h_offset = h_offset
        self.height = Config.card_height
        self.width = Config.card_width
        # Create rectangle element on the screen and store its
        self.id = self.board.create_rectangle(self.w_offset, self.h_offset,
                                              self.w_offset + self.width, self.h_offset + self.height,
                                              fill='grey')

        # Stack of cards
        self.pile = []

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

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

    # get top left coordinate position of the pile
    def get_coordinate(self):
        return [self.w_offset, self.h_offset]