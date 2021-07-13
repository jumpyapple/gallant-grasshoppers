
import render as r
import views as v

term = r.terminal()


def main() -> None:
    """Starts up main function"""
    frame = 0
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            v.print_test_page(frame)
            key_press = term.inkey(timeout=.5)
            frame += 1
        if key_press == " ":
            break


if __name__ == '__main__':
    main()
