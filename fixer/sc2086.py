import itertools
import logging
import re
from typing import List, Tuple

from . import rewrite

WORD_BOUNDS = re.compile(r'[^${}\[\]\+\w:\-*_/.]')


def _log_line_cols(line: str, zero_based_cols: List[int]):
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        col_points = ''
        last_point = 0
        for col in zero_based_cols:
            spaces = ' ' * (col - last_point)
            col_points += spaces + '^'
            last_point = col + 1
        logging.debug('Quoting words:\n%s%s', line, col_points)


def _insert_quotes(s: str, positions: List[int]) -> str:
    return rewrite.insert(s, '"', positions)


def _find_left_word_bound(s: str, i: int) -> int:
    before_i = s[:i]
    reversed_before_i = before_i[::-1]
    before_match = WORD_BOUNDS.search(reversed_before_i)
    return (i - before_match.start()) if before_match else 0


def _find_right_word_bound(s: str, i: int) -> int:
    after_i = s[i:]
    after_match = WORD_BOUNDS.search(after_i)
    return (i + after_match.start()) if after_match else len(s)


def _find_word_bounds(s: str, i: int) -> Tuple[int, int]:
    left = _find_left_word_bound(s, i)
    right = _find_right_word_bound(s, i)
    return (left, right)


def _quote_words_at_columns(line: str, cols: List[int]) -> str:
    """Returns the line with the word at col surrounded by double quotes.

    Args:
        line: The original line. Should end with a newline.
        col: 1-based column numbers of the starts of the words.
    """
    zero_based_cols = [col - 1 for col in cols]
    _log_line_cols(line, zero_based_cols)

    word_bounds = [_find_word_bounds(line, col) for col in zero_based_cols]
    indices = list(itertools.chain(*word_bounds))
    return _insert_quotes(line, indices)


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2086, _quote_words_at_columns)
