# from render.component import Component

import render as r
import views as v

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            v.start_page.print_start_page()
            key_press = term.inkey(timeout=.5)
        if key_press == " ":
            break


if __name__ == '__main__':
    main()
