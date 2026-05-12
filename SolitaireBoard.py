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

        # dict of piles on the board KEY = Canvas ObjectId or Pile Name
        self.pile_list = {}

        self.configureGameBoard()
        self.deal_game()
        #self.deck = Deck(self)



    def get_board(self):
        return self.board

    def configureGameBoard(self):
        # Build the game board

        # top row
        stock_x = Config.outer_padding
        stock_y = Config.outer_padding
        stock = Pile(self, stock_x, stock_y, 'stock')
        self.pile_list[stock.get_id()] = stock
        self.pile_list[stock.get_name()] = stock

        waste_x = stock_x + Config.card_width + Config.inner_padding
        waste_y = Config.outer_padding
        waste = Pile(self, waste_x, waste_y, 'waste')
        self.pile_list[waste.get_id()] = waste
        self.pile_list[waste.get_name()] = waste

        w = self.board.winfo_width()

        # Setup foundation piles
        for f in range(1,5):
            x_cord = w - (Config.outer_padding + (Config.card_width * f) + (Config.inner_padding * (f-1)))
            y_cord = Config.outer_padding

            pile = Pile(self, x_cord, y_cord, 'foundation'+str(f - 5))
            self.pile_list[pile.get_id()] = pile
            self.pile_list[pile.get_name()] = pile

        # Setup tableu piles
        for p in range(1, 8):
            x_cord = ((Config.card_width + Config.inner_padding) * (p-1)) + Config.outer_padding
            y_cord = Config.outer_padding + Config.card_height + Config.inner_padding

            pile = Pile(self, x_cord, y_cord, 'tableu'+str(p))
            self.pile_list[pile.get_id()] = pile
            self.pile_list[pile.get_name()] = pile

    # Deal the deck of cards
    def deal_game(self):

        d = Deck(self)
        d.shuffle_deck()
        cards = d.get_cards()

        dealt = 0
        # d = card depth (1 for first card, 2 for 2nd card, etc)
        for d in range (1,8):
            # t = tableu number
            for t in range (1,8):
                # Solitaire dealing rules creates a triangle
                if t >= d:
                    # get the pile by its name
                    pname = 'tableu'+str(t)
                    pile = self.pile_list.get(pname)
                    # get a card and add it to the pile.
                    card = cards[dealt]
                    pile.deal(card)
                    dealt += 1


    def add_card_to_pile(self, card, pile):
        return


    # function that is called from within a Card to ask the board to handle a card drop event
    # make sure its valid (isPile) + passes solitaire rules that have not been implemented yet
    # add to pile, observe it grows, then fix card placements
    def is_valid_move(self, event, card):

        # if drop on a pile
        #   get the name of that pile
        #   if name NOT tableu or foundation
        #       return False
        #   else
        #       check with that pile to see if the pile can accept this card validly
        #       if pile can accept
        #           add card to pile
        #


        # Pile class for the pile if it exists
        pile = self.is_pile_at(event.x,event.y)

        if pile:
            pname = pile.get_name()
            isValid = False
            # check if the move is valid;
            # only 2 types of piles can accept a valid move
            if 'tableu' in pname:
                if self.is_valid_tableu_move(pile, card):
                    # do the move
                    self.valid_tableu_move(pile, card)
                    return True
            elif 'foundation' in pname:
                if self.is_valid_foundation_move(pile, card):
                    return True

            #pile.add(card)
            #self.board.moveto(card.get_id(), event.x, event.y)
        return False

    # function for handling tableu drop rules
    # returns boolean
    def is_valid_tableu_move(self, pile, card):
        # check the top card of the pile
        top = pile.top()
        # if the card is the opposite color as the top
        #   return True
        if top:
            isColor = top.get_color() != card.get_color()
            if isColor:
                return True

        return False

    def valid_tableu_move(self, pile, card):
        # remove the card from its current pile
        # add the card to its new pile

        # remove the card from current pile
        prev_pname = card.get_pname()
        # card's prev Pile instance
        prev_pile = self.pile_list.get(prev_pname)

        # chain of cards to move (all cards under the top most card grabbed will have to move)
        # chain = [card, .. , bottom of chain]
        chain = prev_pile.split_chain(card)

        for c in chain:
            pile.add(c)

        return True


    # function for handling foundation moves
    # returns boolean
    def is_valid_foundation_move(self, pile, card):
        # check the top card of the pile
        top = pile.top()
        # if the card is the same color as the top then
        # return True

        if top:
            isColor = top.get_color() == card.get_color()
            if isColor:
                return True

        return False

    # determines if an event happened over a pile
    # if True, return the Pile
    # if False, return False
    def is_pile_at(self, x, y):
        object_list = self.board.find_overlapping(x, y,
                                                  x, y)

        if (len(object_list) > 0) and self.pile_list.__contains__(object_list[0]):
            return self.pile_list.get(object_list[0])
        else:
            return False

    def card_chain_dragging(self, card, event):
        pname = card.get_pname()
        pile = self.pile_list.get(pname)
        chain = pile.get_chain(card)
        for card in chain:
            cid = card.get_id()
            dp = card.get_drag_position()
            dx = event.x - dp["x"]
            dy = event.y - dp["y"]
            card.set_drag_position({"x": event.x, "y": event.y})
            self.board.move(cid, dx, dy)
            self.board.tag_raise(cid)


        # board needs to update the cards at their new positions starting with 0
        # and offset with window on the y

    def card_chain_grabbing(self, card, event):
        pname = card.get_pname()
        pile = self.pile_list.get(pname)
        chain = pile.get_chain(card)
        for card in chain:
            card.drag_start(event)


    # testing function
    def under(self, event):
        print(str(event))
        #what pile, if any, was clicked on?
        # get the objects at point (e.x,e.y), sorted by lowest to highest based on focus. basically a 3rd dimension
        object_list = self.board.find_overlapping(event.x, event.y,
                                                  event.x, event.y,)
        print(str(object_list))

        if (len(object_list) > 0) and self.pile_list.__contains__(object_list[0]):
            print(self.pile_list.get(object_list[0]).get_name())
        else:
            print("NO PILE")