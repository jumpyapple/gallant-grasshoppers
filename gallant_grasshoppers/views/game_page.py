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
        self.term.clear()

        main = self.renderstate.get_prop("head_component")

        current_cash = self.state.getCash()
        c = Component(main, self.term.width // 2 - len(str(current_cash)) // 2,
                      self.term.height // 3, children=[current_cash], selectable=False)
        main.set_children([c])
        main.draw_component()

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.state.makeBox()
        elif key == "q":
            exit(0)
