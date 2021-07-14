
import render as r
import views as v

term = r.terminal()


class CurrentPage:
    """Controls current page data"""

    def __init__(self, page: any) -> None:
        """Inits page"""
        self.page = page

    def set_page(self, page: any) -> None:
        """Sets current page"""
        self.page = page

    def get_page(self) -> any:
        """Returns current page"""
        return self.page


def main() -> None:
    """Starts up main function"""
    c = CurrentPage(v.print_test_page)
    frame = 0
    key_press = None
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            c.get_page()(frame=frame, current_page=c.set_page, keypress=key_press)
            key_press = term.inkey(timeout=.5)
            frame += 1
        if key_press == " ":
            key_press = None
            break


if __name__ == '__main__':
    main()
