#!/usr/local/bin/python3.7
"""
monitor file modify then execute it.
support go, python, c++, c.
filename endswith .py .c .cpp .go
"""

__author__ = 'Mikele'
__version__ = '0.1.3'

import os, time
import argparse

help_text = 'monitor execute file every seconds.'
parser = argparse.ArgumentParser(description=help_text + " support go cpp c py")
parser.add_argument(dest='filename', metavar='filename')
parser.add_argument(
    '-s', '--seconds', metavar='seconds', action='store',
    default=1.0, help=help_text)

def monitor_file_modify_every(seconds, filename):
    st = os.stat(filename).st_mtime
    while True:
        f = os.stat(filename)
        if st != f.st_mtime:
            st = f.st_mtime
            if filename.endswith('.cpp'):
                cmd = "g++ {} && ./a.out"
            elif filename.endswith('.c'):
                cmd = "gcc {} && ./a.out"
            elif filename.endswith('.py'):
                cmd = "python {}"
            elif filename.endswith('.go'):
                cmd = "go run {}"
            os.system(cmd.format(filename))
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            os._exit(0)
