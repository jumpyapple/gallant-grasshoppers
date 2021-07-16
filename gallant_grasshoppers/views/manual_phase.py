from . import BasePage
from .game_page import GamePage

class ManualPhasePage(BasePage):
    """A game page."""

    def render(self) -> None:
        """Render the game page."""
        print(
            self.term.home
            + self.term.clear
            + self.term.move_y(self.term.height // 2)
        )
        current_cash = self.state.getCash()
        if current_cash <= 1:
            if current_cash == 0:
                print(
                    self.term.black_on_darkkhaki(
                        self.term.center(f"There is no box D:")
                    )
                )
            else:
                print(
                    self.term.black_on_darkkhaki(
                        self.term.center(f"There is {current_cash} box")
                    )
                )
        else:
            print(
                self.term.black_on_darkkhaki(
                    self.term.center(f"There are {current_cash} boxes")
                )
            )
        print(self.term.move_y((self.term.height // 2) + 5) + self.term.center("Tap [Spacebar] to fold a box"))

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.state.makeBox()
            if self.state.getCash() > 50:
                # Process to next phase.
                self.state.phase = "game"
                self.renderstate.set_prop(("current_phase", "game"))
                self.renderstate.set_prop(("current_page", GamePage))
        elif key == "q":
            # Save the session.
            self.state.saveGame()
            self.renderstate.set_prop(("is_exiting", True))
            # TODO: jumpyapple - set is_in_game to False