import os

class Config:
    theme = 'red'
    window_width = 1000
    window_height = 900

    outer_padding = 50
    inner_padding = 33

    card_width = 100
    card_height = 150
    tableu_window = card_height / 5
    tableu_shift = card_height - tableu_window

    waste_window = card_width / 4
    waste_shift = card_width - waste_window

    assets = os.getcwd() + "/assets/"

    # pile_spacing perhaps
    # available_space = window_width - (7*card_width)

    # 8 total pads; 2 outside pads, 6 inside pads
    # outside pads ideally slightly larger than inside.
    # ex 300 available space
    # 300/8 = 37.5
    # outside

    # 300 = 6x + 2y
    # x = 33
    # y = 50