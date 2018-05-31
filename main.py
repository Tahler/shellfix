#!/usr/bin/env python3

import fileinput
import logging
import os
import json
import re
import subprocess
import sys
from typing import Dict, Iterable, List, Tuple

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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


def quote_words_at_columns(line: str, cols: List[int]) -> str:
    """Returns the line with the word at col surrounded by double quotes.

    Args:
        line: The original line. Should end with a newline.
        col: 1-based column numbers of the starts of the words.
    """
    zero_based_cols = [col - 1 for col in cols]
    log_line_cols(line, zero_based_cols)
    new_line = ''
    remaining = line[:]
    offset = 0
    for col in zero_based_cols:
        offset_col = col - offset
        before_col = remaining[:offset_col]
        after_col = remaining[offset_col:]
        logging.debug('Inserting at col %s', col)
        logging.debug('before_col: "%s"', before_col)
        logging.debug('after_col: "%s"', after_col)

        # Find next character which is not a letter, '$', '{', or '}'.
        word_end = re.search(r'[^${}\w]', after_col).start()
        word = after_col[:word_end]
        logging.debug('word: "%s"', word)
        quoted_word = '"{}"'.format(word)
        new_line += before_col + quoted_word

        remaining = after_col[word_end:]
        # offset is the start of `after_col` in `line`.
        offset = col + len(word)
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
