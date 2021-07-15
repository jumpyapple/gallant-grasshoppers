
import render as r
import views as v

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    c = r.utils.StateManager({
        "current_page": v.test_page.print_test_page
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
