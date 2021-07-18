from . import BasePage
from .start_page import StartPage, boxer_logo


class CreditPage(BasePage):
    """The credit page."""

    def render(self) -> None:
        """Render the credit page."""
        print(self.term.home + self.term.clear)
        # TODO: Make it pretty :D.
        with self.term.location(0, 4):
            for line in boxer_logo:
                print(self.term.center(line))
            print(self.term.move_down + self.term.center("Developed by"))
            print("Burned with anger and caffeine")
            print("Breno Cabral with [to be added]")
            print(
                "jumpyapple with anxiety, caffeine, and love (but mainly the first two)"
            )
            print("KnoxZingVille with [to be added]")
            print("zachkaupp with [to be added]")
            print("Zix with [to be added]")
            print(self.term.move_down + self.term.center("for"))
            print("Python Discord's Summer Code Jam 2021")

    def handle_input(self, key: str) -> None:
        """Handle input while in the game page."""
        if key == " ":
            self.renderstate["current_page"] = StartPage
