from . import rewrite


def _append_return(line: str, *unused_args, **unused_kwargs) -> str:
    return line.rstrip() + ' || return\n'


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2164, _append_return)
