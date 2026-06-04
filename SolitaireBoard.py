import tkinter as tk
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
        self.options_bar = Frame(self.gameframe)
        self.options_bar.pack()

        self.board = Canvas(self.gameframe, name='solitaire', bg='green')
        # expand to the size of the window.. **might need to change to accomodate dynamic sizing
        self.board.pack(expand=True, fill="both")
        self.board.update()

        # dict of piles on the board KEY = Canvas ObjectId or Pile Name
        self.pile_list = {}

        self.configureOptionsBar()
        self.configureGameBoard()
        self.winner = None
        self.deal_game()

        sid = self.pile_list.get('stock').get_id()
        self.board.tag_bind(sid, '<ButtonRelease-1>', self.stock_draw)
        #self.deck = Deck(self)

    def configureOptionsBar(self):
        # put in the New Game & Restart buttons
        self.new_button = tk.Button(self.options_bar, text='New Game', command=self.new_game)
        self.reset_button = tk.Button(self.options_bar, text='Fix Win', command=self.fix_win)

        self.new_button.pack(side='left', fill='both', expand=True)
        self.reset_button.pack(side='left', fill='both', expand=True)

    # build game board with no cards
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
        self.winner = None

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

                    if dealt < len(cards):
                        # get a card and add it to the pile.
                        card = cards[dealt]
                        # if this the last card in the pile we flip it to be readable
                        if t == d:
                            card.flip()
                            card.toggle_drag()
                        pile.deal(card)
                        dealt += 1

        # use dealt as an index to split cards and then populate the stock.
        stock = self.pile_list.get('stock')

        for card in cards[dealt:]:
            stock.deal(card)

    def reset_board(self):
        piles = set(self.pile_list.values())

        if self.winner:
            #destroy win screen
            self.board.delete(self.winner)
            self.winner = None
        for pile in piles:
            while not pile.isEmpty():
                card = pile.pop()
                self.board.delete(card.get_id())

    def new_game(self):
        self.reset_board()
        self.deal_game()

    def check_win(self):
        winner = True
        for i in [1,2,3,4]:
            foundation = self.pile_list.get('foundation-'+str(i))
            top = foundation.top()
            if top:
                if top.get_rank() != 13:
                    winner = False

        if winner:
            self.winner = self.board.create_text(Config.window_width/2, Config.window_height/2, text='WINNER!', font=('Helvetica',36))



    # function that is called from within a Card to ask the board to handle a card drop event
    # make sure its valid (isPile) + passes solitaire rules that have not been implemented yet
    # add to pile, observe it grows, then fix card placements
    def is_valid_move(self, event, card):
        # Pile class for the pile if it exists
        pile = self.is_pile_at(event.x,event.y)

        if pile:
            pname = pile.get_name()
            # check if the move is valid;
            # only 2 types of piles can accept a valid move
            if 'tableu' in pname:
                if self.is_valid_tableu_move(pile, card):
                    # do the move
                    self.valid_tableu_move(pile, card)
                    return True
            elif 'foundation' in pname:
                if self.is_valid_foundation_move(pile, card):
                    self.valid_foundation_move(pile, card)
                    self.check_win()
                    return True

        chain = self.get_card_chain(card)
        for c in chain:
            c.reset_position()
        #reset card positions
        return False

    # function for handling tableu drop rules
    # returns boolean
    def is_valid_tableu_move(self, pile, card):
        # check the top card of the pile
        crank = card.get_rank()
        top = pile.top()
        # if the card is the opposite color as the top
        #   return True
        if top:
            isColor = top.get_color() != card.get_color()
            # color is correct now we must check rank.
            if isColor:
                # rank must be one value higher.
                trank = top.get_rank()
                if (crank + 1) == trank:
                    return True
        # if king, it can be dropped on an open tableu
        elif crank == 13:
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

        # if the card comes from the waste then we make top card draggable
        if 'waste' in prev_pname:
            top = prev_pile.top()
            if top is not None:
                if not top.is_draggable():
                    top.toggle_drag()

        for c in chain:
            pile.add(c)

        return True

    # function for handling foundation moves
    # returns boolean
    def is_valid_foundation_move(self, pile, card):
        # card must NOT be a chain!!
        chain = self.get_card_chain(card)
        if len(chain) == 1:
            # check the top card of the pile
            top = pile.top()
            if top:
                if top.get_suit() == card.get_suit():
                    if (top.get_rank() + 1) == card.get_rank():
                        return True
            else:
                #if the pile is empty it can only accept an Ace
                if card.get_rank() == 1:
                    return True

        return False

    def valid_foundation_move(self, pile, card):

        prev_pname = card.get_pname()
        # remove card from the old pile
        prev_pile = self.pile_list.get(prev_pname)
        # we've already established this has to be a chain of 1
        pcard = prev_pile.split_chain(card)[0]

        # if the card comes from the waste then we make top card draggable
        if 'waste' in prev_pname:
            top = prev_pile.top()
            if top is not None:
                if not top.is_draggable():
                    top.toggle_drag()

        #sanity check lol
        if pcard != card:
            raise
        # add card to new pile
        pile.add(card)

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

    def get_board(self):
        return self.board

    def get_card_chain(self, card):

        prev_pile = card.get_pname()
        prev_pile = self.pile_list.get(prev_pile)

        return prev_pile.get_chain(card)

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

    def stock_draw(self, event=None):
        # pop (up to) top 3 cards from the pile and put them into a list
        stock = self.pile_list.get('stock')
        waste = self.pile_list.get('waste')
        w_coord = waste.get_coords()


        # prep the waste for the new draw
        w_cards = waste.get_cards()
        w_len = len(w_cards)

        #if click on em empty stock try repopulating with the waste.
        if stock.isEmpty():
            if w_len > 0:
                # grab the cards from waste pile
                w_cards = waste.split_chain(w_cards[0])
                for card in reversed(w_cards):
                    card.flip()
                    stock.add(card)
                    if card.is_draggable():
                        card.toggle_drag()
        else:
            if w_len >= 2:
                c1 = w_cards[w_len - 2]
                c2 = w_cards[w_len - 1]
                c1.update_position(w_coord['x'], w_coord['y'])
                c2.update_position(w_coord['x'], w_coord['y'])
                if c1.is_draggable():
                    c1.toggle_drag()
                if c2.is_draggable():
                    c2.toggle_drag()

            draw = []
            for i in [1,2,3]:
                if not stock.isEmpty():
                    card = stock.pop()
                    card.flip()
                    draw.append(card)

            # now toggle only the top card to be draggable
            dlen = len(draw)
            if dlen >= 1:
                for i in range(0, dlen):
                    card = draw[i]
                    card = draw[i]
                    if i == dlen - 1:
                        card.toggle_drag()
                    waste.add(card)
                    x_offset = w_coord["x"] + (i * Config.waste_window)
                    card.update_position(x_offset, w_coord["y"])

    def card_grab(self, card, event):
        # click event for cards

        # if stock pile then draw cards and put them in the waste
        if 'stock' in card.get_pname():
           self.stock_draw()
        else:
            pname = card.get_pname()
            pile = self.pile_list.get(pname)
            chain = pile.get_chain(card)
            for card in chain:
                card.chain_drag_start(event)

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

    # testing function to fix the game to be one move from winning
    def fix_win(self):

        self.reset_board()

        d = Deck(self)
        cards = d.get_cards()

        card_idx = 0
        for i in range(1,5):
            foundation = self.pile_list.get('foundation-'+str(i))
            for j in range(1, 14):
                card = cards[card_idx]

                # is card flipped and draggable? if not then we make it so
                if not card.is_draggable():
                    card.toggle_drag()

                if card.is_flipped():
                    card.flip()

                if i == 4 and j == 13:
                    #place the last card onto the first tableu
                    self.pile_list.get('tableu1').add(card)
                else:
                    foundation.add(card)
                card_idx += 1