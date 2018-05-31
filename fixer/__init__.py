import logging
import sys

from . import shellcheck
from . import sc2006
from . import sc2086

def fix_all(path: str):
    sc2006.fix(path)
    sc2086.fix(path)
    # fix 2016
    # fix 2046
