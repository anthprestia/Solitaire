import random
import tkinter
from tkinter import *
from Config import *
from PIL import Image, ImageTk


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

        trank = self.rank

        if self.rank == 1:
            trank = 'A'
        elif self.rank == 11:
            trank = 'J'
        elif self.rank == 12:
            trank = 'Q'
        elif self.rank == 13:
            trank = 'K'

        self.name = f"{trank}_of_{self.suit}"

        # create card object and maybe disable the visual until deal
        #self.id = self.board.create_rectangle(0, 0, Config.card_width, Config.card_height,
        #                                      fill=self.color, state='hidden', outline='white')

        fname = Config.assets + self.name + '.png'
        card = Image.open(fname)
        card = card.resize((Config.card_width, Config.card_height))

        fname = Config.assets + Config.theme + '.png'
        cback = Image.open(fname)
        cback = cback.resize((Config.card_width, Config.card_height))

        self.card = ImageTk.PhotoImage(card)
        self.cback = ImageTk.PhotoImage(cback)
        # indicates which side of the card is showing front/T; back/F
        self.front = False


        #draggable corresponds to side of card being shown..?
        self.id = self.board.create_image(0,0, image=self.cback, state=HIDDEN)
        self.draggable = False
        self.start_position = {"x":0,"y":0}
        self.drag_position = {"x":0,"y":0}

        self.board.tag_bind(self.id, "<ButtonRelease-1>", self.on_grab)
        #self.board.tag_bind(self.id, "<Button-1>", self.on_grab)

        #self.toggle_drag()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def get_color(self):
        return self.color

    def is_draggable(self):
        return self.draggable

    def get_drag_position(self):
        return self.drag_position

    def set_drag_position(self, position):
        self.drag_position = position

    def get_pname(self):
        return self.pname

    def set_pname(self, pname):
        self.pname = pname

    def is_flipped(self):
        return not self.front

    def flip(self):
        if self.front:
            self.board.itemconfig(self.id, image=self.cback)
            self.front = False
            #self.toggle_drag()
        else:
            self.board.itemconfig(self.id, image=self.card)
            self.front = True
            #self.toggle_drag()

    def update_position(self, x, y):
        self.start_position = {"x":x,"y":y}
        self.board.itemconfig(self.id, state='normal')
        self.board.moveto(self.id, x, y)
        self.board.tag_raise(self.id)

    def reset_position(self):
        self.board.moveto(self.id, self.start_position['x'], self.start_position['y'])

    def deal(self, pname, x, y):
        self.pname = pname
        self.update_position(x,y)

    def toggle_drag(self, e=None):
        if not self.draggable:
            # establish events for grab and drag
            self.board.tag_bind(self.id, "<Button-1>", self.on_grab)
            self.board.tag_bind(self.id, "<B1-Motion>", self.on_drag)
            self.board.tag_bind(self.id, "<ButtonRelease-1>", self.on_drop)
            self.draggable = True
        else:
            #self.board.tag_unbind(self.id, "<Button-1>")
            self.board.tag_unbind(self.id, "<B1-Motion>")
            self.board.tag_unbind(self.id, "<ButtonRelease-1>")
            self.draggable = False

    def on_grab(self, event):
        # ask the board to handle chain grabbing
        self.gameBoard.card_grab(self, event)

    def on_drag(self, event):
        self.gameBoard.card_chain_dragging(self, event)

    def on_drop(self, event):
        isValid = self.gameBoard.is_valid_move(event, self)

    def chain_drag_start(self, event):
        self.drag_position = {"x":event.x,"y":event.y}

    # Overwrite print function to show Suit/Rank
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

class Deck:
    def __init__(self, board):
        self.deck = []
        self.board = board
        self.suits = ["hearts", "clubs", "spades", "diamonds"]
        self.ranks = list(range(1,14))
        #self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        self.deck1()
        #self.deck2()


    def deck2(self):
        self.deck.append(Card(self.board, self.suits[0], self.ranks[0]))
        self.deck.append(Card(self.board, self.suits[0], self.ranks[1]))
        self.deck.append(Card(self.board, self.suits[0], self.ranks[2]))
        self.deck.append(Card(self.board, self.suits[0], self.ranks[3]))
        self.deck.append(Card(self.board, self.suits[0], self.ranks[-1]))

    def deck1(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(self.board, suit, rank))
        #self.shuffle_deck()

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