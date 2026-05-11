import random
from tkinter import *
from Config import *


class Card:
    def __init__(self, board, suit, rank):
        self.gameBoard = board
        self.board = self.gameBoard.get_board()

        self.suit = suit
        self.rank = rank
        self.pname = ''

        if self.suit == "hearts" or self.suit == "diamonds":
            self.color = "red"
        else:
            self.color = "black"

        self.name = f"{self.rank}_of_{self.suit}"

        # create card object and maybe disable the visual until deal
        self.id = self.board.create_rectangle(0, 0, Config.card_width, Config.card_height,
                                              fill=self.color, state='hidden', outline='white')

        self.draggable = False
        self.start_position = {"x":0,"y":0}
        self.drag_position = {"x":0,"y":0}

        self.toggle_drag()

    # Overwrite print function to show Suit/Rank
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_rank(self):
        return self.rank

    def get_color(self):
        return self.color

    def get_pname(self):
        return self.pname

    def set_pname(self, pname):
        self.pname = pname

    def update_position(self, x, y):
        self.start_position = {"x":x,"y":y}

    def deal(self, pname, x, y):
        self.pname = pname
        self.update_position(x,y)
        self.board.itemconfig(self.id, state='normal')
        self.board.moveto(self.id, x, y)
        self.board.tag_raise(self.id)

    def toggle_drag(self, e=None):
        if not self.draggable:
            # establish events for grab and drag
            self.board.tag_bind(self.id, "<Button-1>", self.on_grab)
            self.board.tag_bind(self.id, "<B1-Motion>", self.on_drag)
            self.board.tag_bind(self.id, "<ButtonRelease-1>", self.on_drop)
            self.draggable = True
        else:
            self.board.tag_unbind(self.id, "<Button-1>")
            self.board.tag_unbind(self.id, "<B1-Motion>")
            self.board.tag_unbind(self.id, "<ButtonRelease-1>")
            self.draggable = False

    def on_grab(self, event):
        self.drag_position = {"x":event.x,"y":event.y}
        self.board.tag_raise(self.id)

    def on_drag(self, event):
        dx = event.x - self.drag_position["x"]
        dy = event.y - self.drag_position["y"]
        self.drag_position = {"x":event.x,"y":event.y}
        self.board.move(self.id, dx,dy)

    def on_drop(self, event):
        # deals with on drop event of card
        # ask board if we've dropped over a pile

        # When I drop a card check with the board if it is a valid move
        #   If it is NOT a valid move
        #       reset start position
        #   If it IS a valid move
        #       move to new coordinate and update start_position
        # ---------- IDEA 2 -----------
        # ask the board if its a valid move, pass in the event and this card
        # we then reset the position to start_position assuming the board would handle moving piles if needed

        isValid = self.gameBoard.is_valid_move(event, self)
        self.board.moveto(self.id, self.start_position['x'], self.start_position['y'])

        """
        isPile = self.board.is_pile(event)
        if isPile:
            isPile = isPile.get_coordinate()
            self.start_position = {"x":isPile[0],"y":isPile[1]}
        self.board.moveto(self.id, self.start_position['x'], self.start_position['y'])
        """


class Deck:
    def __init__(self, board):
        self.deck = []
        self.board = board
        self.suits = ["hearts", "clubs", "spades", "diamonds"]
        self.ranks = list(range(1,14))

        self.deck1()
        #self.deal()


    def deck2(self):
        self.deck.append(Card(self.board, self.suits[0], self.ranks[0]))
        self.deck.append(Card(self.board, self.suits[1], self.ranks[1]))

    def deck1(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(self.board, suit, rank))
        self.shuffle_deck()

    def deckT(self):
        self.deck.append(Card(self.board, self.suits[0], self.ranks[0]))

    # TODO - Deal cards piles
    def get_cards(self):
        return self.deck

    def shuffle_deck(self):
        print("Shuffling deck...")
        random.shuffle(self.deck)

    def show_deck(self):
        for card in self.deck:
            print(card)