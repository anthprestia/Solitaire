import random
from tkinter import *
from Config import *


class Card:
    def __init__(self, board, suit, rank):
        self.SolitaireBoard = board
        self.board = self.SolitaireBoard.get_board()

        self.suit = suit
        self.rank = rank
        if self.suit == "hearts" or self.suit == "diamonds":
            self.color = "red"
        else:
            self.color = "black"

        self.name = f"{self.rank}_of_{self.suit}"

        # create card object and maybe disable the visual until deal
        self.id = self.board.create_rectangle(0, 0, Config.card_width, Config.card_height, fill=self.color)

        self.draggable = False
        self.start_position = {"x":0,"y":0}
        self.drag_position = {"x":0,"y":0}

        self.toggle_drag()

    # Overwrite print function to show Suit/Rank
    def __str__(self):
        return self.name

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
        isPile = self.SolitaireBoard.is_pile(event)
        if isPile:
            self.start_position = {"x":isPile[0],"y":isPile[1]}
        self.board.moveto(self.id, self.start_position['x'], self.start_position['y'])


class Deck:
    def __init__(self, board):
        self.deck = []
        self.board = board
        self.suits = ["hearts", "clubs", "spades", "diamonds"]
        self.ranks = list(range(1,14))

        self.deckT()


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
    def deal(self):
        self.deck[0].place(x=10,y=10)
        #self.deck[1].place(x=100,y=80)

    def shuffle_deck(self):
        print("Shuffling deck...")
        random.shuffle(self.deck)

    def show_deck(self):
        for card in self.deck:
            print(card)