import re
from typing import List

from . import rewrite

_PATTERN = re.compile(r'(\s*)(local|export)\s+(.*?)(=.*)')


def _split_line_decl_and_assign(line: str, unused_cols: List[int]) -> str:
    matches = _PATTERN.search(line)
    leading_spaces = matches.group(1)

    qual = matches.group(2)  # 'local' | 'export'

    ident = matches.group(3)
    decl_line = leading_spaces + qual + ' ' + ident + '\n'

    assign_pred = matches.group(4)
    assign_line = leading_spaces + ident + assign_pred + '\n'

    if qual == 'local':
        lines = decl_line + assign_line
    elif qual == 'export':
        lines = assign_line + decl_line
    else:
        raise Exception('unexpected qualifier {}'.format(qual))
    return lines


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2155, _split_line_decl_and_assign)
