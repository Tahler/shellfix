import re
from typing import List

from . import rewrite


def _replace_backticks_with_shell_expansion(line: str, cols: List[int]) -> str:
    # TODO: Handle multiple columns by handling the split in chunks of 3.
    if len(cols) == 1:
        parts = line.split('`')
        # assert len(parts) == 3
        line = parts[0] + '$(' + parts[1] + ')' + parts[2]
    return line


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2006,
                             _replace_backticks_with_shell_expansion)
