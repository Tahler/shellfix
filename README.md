# Shellfix

Make shell scripts more robust by following advice from the
[Shellcheck](https://github.com/koalaman/shellcheck) linter.

Automatically fixes:

- [SC2006](https://github.com/koalaman/shellcheck/wiki/SC2006)
- [SC2086](https://github.com/koalaman/shellcheck/wiki/SC2086)

## Running

1. Install [Shellcheck](https://github.com/koalaman/shellcheck#installing).
1. Run `find . -name '*.sh' | xargs /path/to/main.py`.

## Implementation

This program uses a naive approach of rewriting the file for each rule.

It does, however, take advantage of the fact that rules can appear in cascading
fashion. For example, with the expression `x=$(ls)`,
[SC2034](https://github.com/koalaman/shellcheck/wiki/SC2034) suggests exporting
the variable. However, after the fix (now `export x=$(ls)`), on a second run
it'll suggest declaring and assigning separately
[SC2155](https://github.com/koalaman/shellcheck/wiki/SC2155). Fixing rules
iteratively in the same respective order avoids this issue.
