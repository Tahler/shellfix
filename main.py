#!/usr/bin/env python3

import fileinput
import os
import json
import re
import subprocess
import sys
from typing import Dict, Iterable, List, Tuple


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


def quote_words_at_columns(line: str, cols: List[int]) -> str:
    """Returns the line with the word at col surrounded by double quotes.

    Args:
        line: The original line. Should end with a newline.
        col: 1-based column numbers of the starts of the words.
    """
    zero_based_cols = [col - 1 for col in cols]

    new_line = ''
    remaining = line[:]
    for col in zero_based_cols:
        before_col = remaining[:col]
        after_col = remaining[col:]

        next_space_index = re.search(r'\s', after_col).start()
        word = after_col[:next_space_index]
        quoted_word = '"{}"'.format(word)
        new_line += before_col + quoted_word

        remaining = after_col[next_space_index:]
    new_line += remaining
    return new_line


def rewrite_file_with_quotes(path: str, errs: Dict[int, List[int]]):
    line_col_map = dict(errs)
    with fileinput.input(files=(path, ), inplace=True) as f:
        for i, line in enumerate(f):
            line_num = i + 1
            if line_num in line_col_map:
                cols = line_col_map[line_num]
                line = quote_words_at_columns(line, cols)
            print(line, end='')


def main():
    paths = sys.argv[1:]
    for path in paths:
        errs = get_sc2086_locations(path)
        rewrite_file_with_quotes(path, errs)


if __name__ == '__main__':
    main()
