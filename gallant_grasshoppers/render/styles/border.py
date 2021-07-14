
from blessed import Terminal


def draw(terminal: Terminal, window: object) -> str:
    """Draws border around component"""
    border = ""
    for i in range(window.height):
        border += terminal.move_xy(window.begin_x, window.begin_y+i) + "│"
        border += terminal.move_xy(window.begin_x + window.width-1, window.begin_y+i) + "│"
    border += terminal.move_xy(window.begin_x, window.begin_y) + "─" * window.width
    border += terminal.move_xy(window.begin_x, window.begin_y + window.height-1) + "─" * window.width

    border += terminal.move_xy(window.begin_x + window.width-1, window.begin_y) + "┐"
    border += terminal.move_xy(window.begin_x, window.begin_y) + "┌"
    border += terminal.move_xy(window.begin_x, window.begin_y + window.height-1) + "└"
    border += terminal.move_xy(window.begin_x + window.width-1, window.begin_y + window.height-1) + "┘"

    return border
