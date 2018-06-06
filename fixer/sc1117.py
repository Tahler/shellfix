from typing import List

from . import rewrite


def _insert_backslash(line: str, cols: List[int]) -> str:
    zero_based_cols = [col - 1 for col in cols]
    return rewrite.insert(line, '\\', zero_based_cols)


def fix(path: str):
    rewrite.fix_rule_by_line(path, 1117, _insert_backslash)
