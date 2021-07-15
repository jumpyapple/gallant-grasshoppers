#!/usr/bin/env python3
from . import BasePage


class GamePage(BasePage):
    """A game page."""

    def render(self) -> None:
        """Render the game page."""
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
        """Handle input while in the game page."""
        if key == " ":
            self.state.makeBox()
        elif key == "q":
            exit(0)
