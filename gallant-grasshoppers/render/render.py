from blessed import Terminal

from .styles.border import draw


class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(
            self, terminal: Terminal, window: object, width: int, height: int,
            begin_x: int, begin_y: int, data: any = None):
        self.terminal = terminal
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.data = data
        if window:
            self.window = window
            self.begin_x += window.begin_x
            self.begin_y += window.begin_y

    def __repr__(self):
        return draw(self.terminal, self) + (self.terminal.move_xy(self.begin_x + 1, self.begin_y + 1)
                                            + str(self.data))

    def set_data(self, data: any = None) -> bool:
        """Sets data for to be displayed in component"""
        self.data = data
        return True

    def draw_component(self) -> bool:
        """Draws component"""
        print(self)
        return True


if __name__ == '__main__':
    win = Component(None, 1, 2, 3, 4)
    print(win)
