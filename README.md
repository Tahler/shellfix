# Shellfix

Make shell scripts more robust by following advice from the
[Shellcheck](https://github.com/koalaman/shellcheck) linter.

Automatically fixes:

- [SC2006](https://github.com/koalaman/shellcheck/wiki/SC2006)
- [SC2086](https://github.com/koalaman/shellcheck/wiki/SC2086)

## Running

1. Install [Shellcheck](https://github.com/koalaman/shellcheck#installing).
1. Run `find . -name '*.sh' | xargs /path/to/main.py`.
