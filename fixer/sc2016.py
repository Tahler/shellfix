from . import rewrite


def fix(path: str):
    rewrite.fix_rule_by_ignore(path, 2016)
