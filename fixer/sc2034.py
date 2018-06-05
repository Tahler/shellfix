from . import rewrite


def _delete_line(*unused_args, **unused_kwargs):
    return ''

def fix(path: str):
    rewrite.fix_rule_by_line(path, 2034, _delete_line)

