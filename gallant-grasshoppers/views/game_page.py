#!/usr/bin/env python3

from blessed import Terminal

from lib.gamestate import CASH
from . import BasePage


class GamePage(BasePage):
    def render(self):

        with self.term.cbreak(), self.term.hidden_cursor():
            input_key = ""
            print(
                self.term.home
                + self.term.clear
                + self.term.move_y(self.term.height // 2)
            )
            current_cash = self.state.getCash()
            print(
                self.term.black_on_darkkhaki(
                    self.term.center(f"Create a box [{current_cash}]")
                )
            )

    def handle_input(self, key: str) -> None:
        if key == " ":
            self.state.makeBox()
