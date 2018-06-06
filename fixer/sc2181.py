import logging
import fileinput
import re
from typing import Callable, Dict, List

from . import shellcheck

_WHITESPACE_PATTERN = re.compile(r'^(\s*)')


def fix(path: str):
    errs = shellcheck.run_for_error(path, 2181)
    _rewrite_for_2181(path, errs)


def _rewrite_for_2181(path: str, locations: Dict[int, List[int]]):
    line_col_map = dict(locations)
    with fileinput.input(files=(path, ), inplace=True) as f:
        prev_line = ''
        for i, line in enumerate(f):
            line_num = i + 1
            next_line_num = line_num + 1
            if line_num in line_col_map:
                if '-ne 0' not in line and '-eq 0' not in line:
                    logging.error('unsupported line: %s', line)
                should_put_bang = '-ne 0' in line
                bang = '! ' if should_put_bang else ''
                match = _WHITESPACE_PATTERN.search(line)
                leading_whitespace = match.group(1) if match else ''
                line = '{}if {}{}; then\n'.format(leading_whitespace, bang,
                                                  prev_line)
                print(line, end='')
            elif next_line_num in line_col_map:
                prev_line = line.strip()
            else:
                print(line, end='')
