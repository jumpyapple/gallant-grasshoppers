from blessed import Terminal

term = Terminal()


def main() -> None:
    """
    Starts up main function

    :return:
    """
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear + term.move_y(term.height // 2))
            print(term.black_on_darkkhaki(term.center("hello world")))
            term.inkey()


if __name__ == "__main__":
    main()
