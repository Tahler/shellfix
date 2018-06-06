import re

from . import rewrite


def _replace_which_with_command_v(line: str, *unused_args) -> str:
    return line.replace('which', 'command -v')


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2230, _replace_which_with_command_v)
