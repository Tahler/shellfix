#!/usr/bin/env python3

import fileinput
import os
import json
import re
import subprocess
import sys
from typing import Any, Iterable, List, Tuple


def run_shellcheck(path: str) -> List[Any]:
    proc = subprocess.run(
        ['shellcheck', '--format=json', path], stdout=subprocess.PIPE)
    return json.loads(proc.stdout.decode('utf-8'))


def get_sc2086_locations(path: str) -> List[Tuple[int, int]]:
    json_errors = run_shellcheck(path)
    json_sc2086_errors = [err for err in json_errors if err['code'] == 2086]
    line_col_tuples = [(err['line'], err['column'])
                       for err in json_sc2086_errors]
    return line_col_tuples


def quote_at_col(line: str, col: int) -> str:
    """Returns the line with the word at col surrounded by double quotes.

    Args:
        line: The original line ending with a newline.
        col: 1-based column number of the start of the word.
    """
    zero_based_col = col - 1
    before_col = line[:zero_based_col]
    after_col = line[zero_based_col:]
    next_space_index = re.search(r'\s', after_col).start()
    word = after_col[:next_space_index]
    quoted_word = '"{}"'.format(word)
    after_word = after_col[next_space_index:]
    replaced_line = before_col + quoted_word + after_word
    return replaced_line


def rewrite_file_with_quotes(path: str, errs: List[Tuple[int, int]]):
    # TODO: What if there are multiple words to be quoted in the line?
    line_col_map = dict(errs)
    with fileinput.input(files=(path, ), inplace=True, backup='.bak') as f:
        for i, line in enumerate(f):
            line_num = i + 1
            if line_num in line_col_map:
                col = line_col_map[line_num]
                line = quote_at_col(line, col)
            print(line, end='')


def main():
    path = sys.argv[1]
    errs = get_sc2086_locations(path)
    rewrite_file_with_quotes(path, errs)


if __name__ == '__main__':
    main()
