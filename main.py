#!/usr/bin/env python3

import fileinput
import logging
import os
import itertools
import json
import re
import subprocess
import sys
from typing import Dict, Iterable, List, Tuple

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

WORD_BOUNDS = re.compile(r'[^${}\w:\-_/.]')


def run_shellcheck(path: str) -> List[Dict]:
    proc = subprocess.run(
        ['shellcheck', '--format=json', path], stdout=subprocess.PIPE)
    return json.loads(proc.stdout.decode('utf-8'))


def get_sc2086_locations(path: str) -> Dict[int, List[int]]:
    json_errors = run_shellcheck(path)
    json_sc2086_errors = [err for err in json_errors if err['code'] == 2086]
    line_to_cols = {}
    for err in json_sc2086_errors:
        line = err['line']
        col = err['column']

        if line not in line_to_cols:
            line_to_cols[line] = []

        line_to_cols[line].append(col)
    return line_to_cols


def log_line_cols(line: str, zero_based_cols: List[int]):
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        col_points = ''
        last_point = 0
        for col in zero_based_cols:
            spaces = ' ' * (col - last_point)
            col_points += spaces + '^'
            last_point = col + 1
        logging.debug('Quoting words:\n%s%s', line, col_points)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def insert_quotes(s: str, positions: List[int]) -> str:
    unique_ordered_positions = sorted(set(positions))
    positions_with_start_end = [None, *unique_ordered_positions, None]
    parts = [s[i:j] for i, j in pairwise(positions_with_start_end)]
    return '"'.join(parts)


def find_left_word_bound(s: str, i: int) -> int:
    before_i = s[:i]
    reversed_before_i = before_i[::-1]
    before_match = WORD_BOUNDS.search(reversed_before_i)
    return (i - before_match.start()) if before_match else None


def find_right_word_bound(s: str, i: int) -> int:
    after_i = s[i:]
    after_match = WORD_BOUNDS.search(after_i)
    return (i + after_match.start()) if after_match else None


def find_word_bounds(s: str, i: int) -> Tuple[int, int]:
    left = find_left_word_bound(s, i)
    right = find_right_word_bound(s, i)
    return (left, right)


def quote_words_at_columns(line: str, cols: List[int]) -> str:
    """Returns the line with the word at col surrounded by double quotes.

    Args:
        line: The original line. Should end with a newline.
        col: 1-based column numbers of the starts of the words.
    """
    zero_based_cols = [col - 1 for col in cols]
    log_line_cols(line, zero_based_cols)

    word_bounds = [find_word_bounds(line, col) for col in zero_based_cols]
    indices = list(itertools.chain(*word_bounds))
    return insert_quotes(line, indices)


def rewrite_file_with_quotes(path: str, errs: Dict[int, List[int]]):
    line_col_map = dict(errs)
    with fileinput.input(files=(path, ), inplace=True) as f:
        for i, line in enumerate(f):
            line_num = i + 1
            if line_num in line_col_map:
                cols = line_col_map[line_num]
                line = quote_words_at_columns(line, cols)
            print(line, end='')


def log_sc2086_errors(errs: Dict[int, List[int]]):
    if errs and logging.getLogger().isEnabledFor(logging.INFO):
        tuples = []
        for line, cols in errs.items():
            for col in cols:
                tuples.append((line, col))
        logging.info('Found SC2086 errors at %s', tuples)


def main():
    paths = sys.argv[1:]
    for path in paths:
        logging.info('Checking %s', path)
        errs = get_sc2086_locations(path)
        log_sc2086_errors(errs)
        rewrite_file_with_quotes(path, errs)


if __name__ == '__main__':
    main()
