#!/usr/bin/env python
import sys

if __name__ == "__main__":
    from psistats import cli
    cli.main(sys.argv)
else:
    raise RuntimeError("This file should not be imported")
