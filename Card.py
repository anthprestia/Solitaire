import random
from tkinter import *

class Card:
    def __init__(self, board, suit, rank):
        self.board = board

        self.suit = suit
        self.rank = rank
        if self.suit == "hearts" or self.suit == "diamonds":
            self.color = "red"
        else:
            self.color = "black"

        self.name = f"{self.rank}_of_{self.suit}"
        self.card = Label(board, name=self.name, state='disabled', width=0, height=0, bg=self.color)
        self.draggable = False
        self.drag_data = {"x":0,"y":0}

        self.card.bind("<Double-Button-1>", self.toggle_drag)
        self.toggle_drag()

    # Overwrite print function to show Suit/Rank
    def __str__(self):
        return self.name

    def place(self, x, y):
        self.card.place(x=x,y=y)

    def toggle_drag(self, e=None):
        if not self.draggable:
            # establish events for grab and drag
            self.card.bind("<Button-1>", self.on_grab)
            self.card.bind("<B1-Motion>", self.on_drag)
            self.card.bind("<ButtonRelease>", self.on_drop)
            self.draggable = True
        else:
            self.card.unbind("<Button-1>")
            self.card.unbind("<B1-Motion>")
            self.card.unbind("<ButtonRelease>")
            self.draggable = False

    def on_grab(self, event):
        self.drag_data = {"x":event.x,"y":event.y}
        self.card.lift()

    def on_drag(self, event):
        widget = event.widget
        x = widget.winfo_x() - self.drag_data["x"] + event.x
        y = widget.winfo_y() - self.drag_data["y"] + event.y
        widget.place(x=x, y=y)

        #check what elements, if any, we are hovering over
        # sooooo that means pulling the board element from the event and then checking if at position theres another element?
        # once we find the element we send an event directly to it?




    def on_drop(self, event):
        self.get_child_at(event)



        print("DROP EVENT: " + str(event))
        print("    " + str(event.widget))
        print("    ")


    def get_child_at(self, event):
        name = event.widget.winfo_name()
        cords = self.standardize_event_cords(event)
        print(name + str(cords['x']) + str(cords['y']))
        # now

    def standardize_event_cords(self, event):
        widget = event.widget
        # STANDARDIZE TO PARENT CORDS, otherwise event are widget specific cords
        return {'x': widget.winfo_x() + event.x, 'y': widget.winfo_y() + event.y}



class Deck:
    def __init__(self, board):
        self.deck = []
        self.board = board
        self.suits = ["hearts", "clubs", "spades", "diamonds"]
        self.ranks = list(range(1,14))

        self.deck2()
        self.deal()


    def deck2(self):
        self.deck.append(Card(self.board, self.suits[0], self.ranks[0]))
        self.deck.append(Card(self.board, self.suits[1], self.ranks[1]))

    def deck1(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(self.board, suit, rank))

        self.shuffle_deck()


    # TODO - Deal cards piles
    def deal(self):
        self.deck[0].place(x=10,y=10)
        self.deck[1].place(x=100,y=80)

    def shuffle_deck(self):
        print("Shuffling deck...")
        random.shuffle(self.deck)

    def show_deck(self):
        for card in self.deck:
            print(card)