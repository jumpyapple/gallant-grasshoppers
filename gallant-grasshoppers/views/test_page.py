
from blessed import Terminal
from render import Component  # ignore this. it is correct syntax


def print_test_page(frame: int) -> None:
    """Creates start page, can be called from signal module and directly"""
    term = Terminal()
    c = Component(None, term.width // 2,
                  term.height // 3, data=[str(frame)])
    c.set_styles({"border": True})
    c.draw_component()
    print(term.move_y(int(term.height - 1)))
    print(term.white(term.center("[PRESS SPACE TO CONTINUE]")))
