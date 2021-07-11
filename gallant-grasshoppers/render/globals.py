from blessed import Terminal

global terminal
terminal = Terminal()


def init_term() -> Terminal:
    """Initialize Terminal Object"""
    terminal = Terminal()
    return terminal


def get_terminal() -> Terminal:
    """Get Terminal Object"""
    return terminal


if __name__ == '__main__':
    term = init_term()
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear + term.move_y(term.height // 2))
            print(term.black_on_darkkhaki(term.center(str(get_terminal()))))
            term.inkey()
