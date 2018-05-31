import fileinput
from typing import Callable, Dict, List


def by_line(path: str, locations: Dict[int, List[int]],
            fix: Callable[[str, List[int]], str]):
    line_col_map = dict(locations)
    with fileinput.input(files=(path, ), inplace=True) as f:
        for i, line in enumerate(f):
            line_num = i + 1
            if line_num in line_col_map:
                cols = line_col_map[line_num]
                line = fix(line, cols)
            print(line, end='')
