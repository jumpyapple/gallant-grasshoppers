#!/usr/bin/env python3
from . import BasePage


class GamePage(BasePage):
    """A game page."""

    def render(self) -> None:
        """Render the game page."""
        print(
            self.term.home
            # + self.term.clear, I don't think this is needed
            + self.term.move_y(self.term.height // 2)
        )
        current_cash = self.state.getCash()
        print(
            self.term.black_on_darkkhaki(
                self.term.center("Create a box")
            )
        )
        print(
            self.term.black_on_darkkhaki(
                self.term.center(f"[{current_cash}]")
            )
        )

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.state.makeBox()
        elif key == "q":
            exit(0)
