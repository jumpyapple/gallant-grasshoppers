
import render as r
import views as v

term = r.terminal()


class StateManager:
    """Controls current page data"""

    def __init__(self, state: dict) -> None:
        """Inits page"""
        self.state = state

    def set_state(self, state: dict) -> None:
        """Sets current page"""
        self.state = state

    def get_state(self) -> any:
        """Returns current page"""
        return self.state

    def get_prop(self, prop: str) -> any:
        """Gets property information"""
        try:
            return self.state[prop]
        except KeyError:
            return False

    def set_prop(self, d: tuple) -> None:
        """Sets Property information"""
        self.state[d[0]] = d[1]


def main() -> None:
    """Starts up main function"""
    c = StateManager({
        "current_page": v.print_test_page
    })
    frame = 0
    key_press = None
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            c.get_prop("current_page")(frame=frame, main=c, keypress=key_press)

            frame += 1
            key_press = term.inkey(timeout=.5)

        if key_press == "q":
            break


if __name__ == '__main__':
    main()
