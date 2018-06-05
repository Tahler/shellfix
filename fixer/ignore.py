import re

_LEADING_WHITESPACE_PATTERN = re.compile(r'^(\s*)')


def add_ignore_directive_before_line(rule_code: int, line: str) -> str:
    match = _LEADING_WHITESPACE_PATTERN.search(line)
    leading_whitespace = match.group(1) if match else ''
    directive_line = '{}# shellcheck disable=SC{}\n'.format(
        leading_whitespace, rule_code)
    lines = directive_line + line
    return lines
