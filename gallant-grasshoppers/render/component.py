
from .styles.border import draw
from .utils.terminal import get_term as terminal


class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(
            self, window: object = terminal(), width: int = 5, height: int = 5,
            begin_x: int = 0, begin_y: int = 0, data: any = None):
        """
        Parameters

        window : obj
            A component object or terminal object
        width : int
            How wide the component is.
            (Default is 5 spaces wide)
        height : int
            How tall the component is.
            (Default is 5 spaces high)
        begin_x : int
            Where the top left starts on the X axis
            (Default is 0)
        begin_y : int
            Where the top left starts on the Y axis
            (Default is 0)
        data : any
            Whatever you want the data to be inside. Could be components, text, ints, etc
            (Default is None)
        """
        self.terminal = terminal()
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
