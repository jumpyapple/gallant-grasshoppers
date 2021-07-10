

class Component:
    """Components are the main way to draw to the screen of the application"""

    def __init__(
            self, window: object, height: int, width: int,
            begin_y: int, begin_x: int, data: any = None):
        self.window = window
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.data = data

    def __repr__(self):
        return self.window.move_y(self.begin_y) + self.window.move_x(self.begin_x) + str(self.data)

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
