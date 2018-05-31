import json
import logging
import subprocess
from typing import List, Dict


def run(path: str) -> List[Dict]:
    proc = subprocess.run(
        ['shellcheck', '--format=json', path], stdout=subprocess.PIPE)
    return json.loads(proc.stdout.decode('utf-8'))


def run_for_error(path: str, error_code: int) -> Dict[int, List[int]]:
    logging.info('Checking %s for SC%s errors', path, error_code)
    all_errors = run(path)
    errors_with_code = [err for err in all_errors if err['code'] == error_code]
    line_to_cols = {}
    for err in errors_with_code:
        line = err['line']
        col = err['column']

        if line not in line_to_cols:
            line_to_cols[line] = []

        line_to_cols[line].append(col)
    _log_reports(path, error_code, line_to_cols)
    return line_to_cols


def _log_reports(path: str, error_code: int, errs: Dict[int, List[int]]):
    if errs and logging.getLogger().isEnabledFor(logging.INFO):
        tuples = []
        for line, cols in errs.items():
            for col in cols:
                tuples.append((line, col))
        logging.info('Found SC%s errors in %s at %s', error_code, path, tuples)
