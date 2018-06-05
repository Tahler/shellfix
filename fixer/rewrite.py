import fileinput
import itertools
import logging
from typing import Callable, Dict, List

from . import ignore
from . import shellcheck


def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def insert(s: str, to_insert: str, positions: List[int]) -> str:
    unique_ordered_positions = sorted(set(positions))
    positions_with_start_end = [None, *unique_ordered_positions, None]
    parts = [s[i:j] for i, j in _pairwise(positions_with_start_end)]
    return to_insert.join(parts)


def by_line(path: str, locations: Dict[int, List[int]],
            fix: Callable[[str, List[int]], str]):
    line_col_map = dict(locations)
    with fileinput.input(files=(path, ), inplace=True) as f:
        for i, line in enumerate(f):
            line_num = i + 1
            if line_num in line_col_map:
                cols = line_col_map[line_num]
                try:
                    line = fix(line, cols)
                except Exception as e:
                    logging.error(e)
            print(line, end='')


def fix_rule_by_line(path: str, rule_code: int,
                     fix: Callable[[str, List[int]], str]):
    errs = shellcheck.run_for_error(path, rule_code)
    by_line(path, errs, fix)


def fix_rule_by_ignore(path: str, rule_code: int):
    errs = shellcheck.run_for_error(path, rule_code)

    def add_ignore_directive_before_line(line: str, *unused_args) -> str:
        return ignore.add_ignore_directive_before_line(rule_code, line)

    by_line(path, errs, add_ignore_directive_before_line)
