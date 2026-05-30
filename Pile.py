from tkinter import *
from Util import *
from Config import *

# A Pile is a Stack of Cards
class Pile:
    def __init__(self, board, w_offset, h_offset, name):
        self.SolitaireBoard = board
        self.board = board.get_board()
        self.name = name
        # also x,y on canvas
        self.w_offset = w_offset
        self.h_offset = h_offset
        self.height = Config.card_height
        self.width = Config.card_width
        self.window = Config.tableu_window
        # Create rectangle element on the screen and store its
        self.id = self.board.create_rectangle(self.w_offset, self.h_offset,
                                              self.w_offset + self.width, self.h_offset + self.height,
                                              fill='grey')

        # Stack of cards
        self.pile = []

        self.next_card = {'x':self.w_offset, 'y':self.h_offset}

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_coords(self):
        return {'x':self.w_offset, 'y':self.h_offset}

    def size(self):
        return len(self.pile)

    def isEmpty(self):
        return len(self.pile) == 0

    def top(self):
        # Assert pile not empty?
        if len(self.pile) > 0:
            return self.pile[-1]
        else:
            return None

    def pop(self):
        card = self.pile.pop()
        self.resize()
        return card

    def get_cards(self):
        return self.pile

    # add an element to the
    def add(self, card):
        self.pile.append(card)
        card.set_pname(self.name)

        # set to vertical/horizontal pile addition logic

        spos_x = self.w_offset
        spos_y = self.h_offset
        if 'tableu' in self.name:
            spos_y = self.h_offset + ((len(self.pile)-1) * self.window)

        card.update_position(spos_x, spos_y)
        self.resize()

    def add_chain(self, chain):
        for card in chain:
            self.add(card)

    def get_chain(self, chainCard):
        chain = []
        # Assert pile not empty?
        if len(self.pile) > 0:
            base = []
            found = False
            for card in self.pile:
                if card == chainCard:
                    found = True
                if found:
                    chain.append(card)
        return chain

    # grab a chain of piles from card to the top
    # aka [0.. card.. n] -> [0, card-1] + [card, n]
    # chainCard is the Card object being grabbed
    # returns a list of cards
    def split_chain(self, chainCard):
        chain = self.get_chain(chainCard)
        base = self.pile[:self.pile.index(chainCard)]

        self.pile = base
        self.resize()

        # check the end of the base and if its not flipped, then we flip and toggle drag
        if len(self.pile) > 0:
            top = self.pile[-1]

            if (not top.is_draggable()) and ('tableu' in self.name):
                top.flip()
                top.toggle_drag()

        return chain

    def deal(self, card):
        self.pile.append(card)
        if 'tableu' in self.name:
            h_offset = self.h_offset + ((len(self.pile)-1) * self.window)
        else:
            h_offset = self.h_offset

        card.deal(self.name, self.w_offset, h_offset)
        self.resize()

    # update the UI element for pile to expand to exist under every laid card
    def resize(self):
        # if pile size == 0 or 1 then card size
        # upper left will be (w_offset, h_offset)
        # bottom right will be (w_offset + card_width, h_offset + card_window*size)

        if 'tableu' in self.name:
            size = len(self.pile)
            if size < 2:
                self.board.coords(self.id, self.w_offset, self.h_offset, self.w_offset + self.width, self.h_offset + self.height)
            else:
                self.board.coords(self.id, self.w_offset, self.h_offset, self.w_offset + self.width, self.h_offset + self.height + (self.window*(size-1)))


    # get top left coordinate position of the pile
    def get_coordinate(self):
        return [self.w_offset, self.h_offset]