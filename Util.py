class Util:

    @staticmethod
    def standardize_event_coords(event):
        widget = event.widget
        # STANDARDIZE TO PARENT CORDS, otherwise event are widget specific cords
        return {'x': widget.winfo_x() + event.x, 'y': widget.winfo_y() + event.y}


    # Probably just trash idk
    @staticmethod
    def get_child_at(event, board):
        name = event.widget.winfo_name()
        cords = Util.standardize_event_coords(event)
        print(name + str(cords['x']) + str(cords['y']))
        # now get the children

        children = board.winfo_children()

        board.master.update_idletasks()
        children = board.winfo_containing(cords['x'], cords['y'])
        print(children)