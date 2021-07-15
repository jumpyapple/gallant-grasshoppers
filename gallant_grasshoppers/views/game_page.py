#!/usr/bin/env python3
import render as r  # ignore this. it is correct syntax
from blessed import Terminal

from . import BasePage

Component = r.Component


class GamePage(BasePage):
    """A game page."""

    def __init__(self, state: object, term: Terminal, renderstate: object):
        super().__init__(state, term, renderstate)
        self.comps = []
        self.current_cursor = None

    def render(self) -> None:
        """Render the game page."""
        main = self.renderstate.get_prop("head_component")
        left_half = Component(main, 0, 0)
        left_half.set_wh(main.width // 2, main.height-1)
        left_half.set_styles({"border": True})

        def component_constructor(data: any, location: tuple) -> Component:
            """Constructs components"""
            c = Component(left_half, location[0], location[1], children=[data])
            c.set_wh(10, 3)
            c.set_styles({"border": True})
            return c

        # placeholder info for map

        to_be_comps = ['red', 'green', 'black', 'black', 'red', 'black']
        loc_list = [(left_half.width // 2 - len(i) // 2, c*5+3) for c, i in enumerate(to_be_comps)]

        list_of_comps = map(component_constructor, to_be_comps, loc_list)
        left_half.set_children(list_of_comps)

        right_half = Component(main, main.width // 2, 0)
        right_half.set_wh(main.width // 2, main.height-1)
        right_half.set_styles({"border": True})

        current_cash = self.state.getCash()
        curr_string = f"Boxes Folded: {current_cash}"

        c = Component(right_half, right_half.width // 2 - len(str(curr_string)) // 2,
                      right_half.height // 5, children=[curr_string], selectable=False)
        update_box = Component(right_half, 1, right_half.height // 2, children=[""])
        update_box.set_wh(right_half.width-2, right_half.height // 2)
        update_box.set_styles({"border": True})
        right_half.set_children([c, update_box])
        main.set_children([left_half, right_half])

        main.draw_component()

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.state.makeBox()
        elif key == "q":
            exit(0)
