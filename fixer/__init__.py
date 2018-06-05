import logging
import sys

from . import shellcheck
from . import sc2006
from . import sc2086


def fix_all(path: str):
    fixers = [sc2006, sc2086]
    for fixer in fixers:
        try:
        fixer.fix(path)
        except Exception as e:
            logging.error(e)
    # fix 2016
    # fix 2046
