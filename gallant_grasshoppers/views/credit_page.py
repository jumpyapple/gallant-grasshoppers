from . import BasePage
from .start_page import StartPage


class CreditPage(BasePage):
    """The credit page."""

    def render(self) -> None:
        """Render the credit page."""
        print(self.term.home + self.term.clear)
        # TODO: Make it pretty :D.
        with self.term.location(0, 0):
            print("Boxer" + self.term.move_down)
            print("Developed by")
            print("Burned with [to be added]")
            print("Breno Cabral with [to be added]")
            print("jumpyapple with anxiety, caffeine, and love (but mainly the first two)")
            print("KnoxZingVille with [to be added]")
            print("zachkaupp with [to be added]")
            print("Zix with [to be added]" + self.term.move_down)
            print("Python Discord's Summer Code Jam 2021")

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.renderstate.set_prop(("current_page", StartPage))
