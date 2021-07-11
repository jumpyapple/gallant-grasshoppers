from blessed import Terminal
from render.render import Component as Comp

term = Terminal()


def main() -> None:
    """Starts up main function"""
    while True:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear + term.move_y(term.height // 2))
            print(term.black_on_darkkhaki(term.center('hello world')))
            c = Comp(term, None, 20, 10, 5, 5)
            c.set_data("Box boys: 15" + str(Comp(term, c, 12, 6, 2, 3, "Buy More?"
                                                 + str(Comp(term, c, 3, 3, 3, 5, ">")))))
            c.draw_component()
            term.inkey()


if __name__ == '__main__':
    main()
