from . import term


def check_window_size() -> None:
    """Checks that window size meets or exceeds minimum"""
    if term.height < 20 or term.width < 80:
        while True:
            with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.location(
                y=term.height // 2
            ):
                print(
                    term.black_on_rosybrown(
                        term.center("Please adjust your terminal to at least 80 x 20")
                    )
                )
                term.inkey(timeout=0.5)
                if term.height >= 20 and term.width >= 80:
                    break


def get_selectables(c: object) -> list[object]:
    """Gets selectable components"""
    try:
        if c.selectables:
            selects = c.selectables
            for i in c.selectables:
                selects += get_selectables(c.selectables)
            return selects
    except AttributeError:
        return []
    return []


def longest(comp: object) -> int:
    """Returns longest line in Component object"""
    len_of_longest = 0
    for line in comp.get_children():
        line = str(line)
        if len(line) > len_of_longest:
            len_of_longest = len(line)
    return len_of_longest
