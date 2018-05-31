import logging
import sys

from . import shellcheck
from . import sc2086

def fix_all(path: str):
    sc2086.fix(path)
    # fix 2006
    # fix 2046
