from .terminal import get_term as terminal

term = terminal()


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
