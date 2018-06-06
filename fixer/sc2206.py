from . import rewrite
from . import sc2086


def fix(path: str):
    rewrite.fix_rule_by_line(path, 2206, sc2086._quote_words_at_columns)
