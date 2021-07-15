def longest(comp: object) -> int:
    """Returns longest line in Component object"""
    len_of_longest = 0
    for line in comp.data:
        if len(line) > len_of_longest:
            len_of_longest = len(line)
    return len_of_longest
