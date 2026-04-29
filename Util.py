class Util:

    @staticmethod
    def standardize_event_coords(event):
        widget = event.widget
        # STANDARDIZE TO PARENT CORDS, otherwise event are widget specific cords
        return {'x': widget.winfo_x() + event.x, 'y': widget.winfo_y() + event.y}