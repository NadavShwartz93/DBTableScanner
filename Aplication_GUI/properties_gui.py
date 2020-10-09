import tkinter.font as tk_font

WIDTH_SIZE = '400'
HEIGHT_SIZE = '600'
WINDOW_SIZE = HEIGHT_SIZE + 'x' + WIDTH_SIZE


class GuiProperties:
    def __init__(self):
        self.title("Table Scanner")
        self.geometry(WINDOW_SIZE)

        self.font_style1 = tk_font.Font(family="Helvetica", size=20)
        self.font_style2 = tk_font.Font(family="Helvetica", size=20, weight=tk_font.BOLD,
                                        slant=tk_font.ITALIC)
        self.font_style3 = tk_font.Font(family="Helvetica", size=10, weight=tk_font.BOLD)
