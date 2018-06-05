import logging
import sys

from . import shellcheck
from . import sc2006
from . import sc2034
from . import sc2086
from . import sc2155


def fix_all(path: str):
    fixers = [sc2006, sc2034, sc2086, sc2155]
    for fixer in fixers:
        try:
            fixer.fix(path)
        except Exception as e:
            logging.error(e)
    # fix 2016
    # fix 2046
