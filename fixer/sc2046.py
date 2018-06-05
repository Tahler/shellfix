from typing import List

from . import rewrite


def _find_closing_paren_index(s: str, start_index: int) -> int:
    """Returns the index of the first symmetrical closing parenthesis in s."""
    closing_paren_index = None
    num_open = 0
    sub = s[start_index:]
    for i, c in enumerate(sub):
        if c == '(':
            num_open += 1
        elif c == ')':
            num_open -= 1
            if num_open == 0:
                closing_paren_index = i
                break
    return closing_paren_index + start_index


def _wrap_command_expansion_with_double_quotes(line: str,
                                               cols: List[int]) -> str:
    start_ends = [(col - 1, _find_closing_paren_index(line, col) + 1)
                  for col in cols]
    flattened_tuple = sum(start_ends, ())
    positions = list(flattened_tuple)
    return rewrite.insert(line, '"', positions)


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2046,
                             _wrap_command_expansion_with_double_quotes)
