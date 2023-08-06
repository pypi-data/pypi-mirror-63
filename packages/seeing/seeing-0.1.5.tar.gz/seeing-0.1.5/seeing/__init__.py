#!/usr/local/bin/python3.7
"""
monitor file modify then execute it.
support go, python, c++, c.
filename endswith .py .c .cpp .go
"""

__author__ = 'Mikele'
__version__ = '0.1.5'

import os, time, logging
import argparse

logging.basicConfig(level=logging.INFO)

help_text = 'monitor execute file every seconds.'
parser = argparse.ArgumentParser(description=help_text + " support go cpp c py")
parser.add_argument(dest='filename', metavar='filename')
parser.add_argument(
    '-s', '--seconds', metavar='seconds', action='store',
    default=1.0, help=help_text)
parser.add_argument(
    '-c', '--cmd', metavar='cmd', action='store', default='',
    help="command to execute script, eg: seeing -c bash hello.sh")

commands = ['go', 'python', 'py', 'python3', 'g++', 'gcc']

def monitor_file_modify_every(seconds, filename, command):
    st = os.stat(filename).st_mtime
    while True:
        f = os.stat(filename)
        if st != f.st_mtime and command not in commands:
            st = f.st_mtime
            if filename.endswith('.cpp'):
                cmd = "g++ {} && ./a.out"
            elif filename.endswith('.c'):
                cmd = "gcc {} && ./a.out"
            elif filename.endswith('.py'):
                cmd = "python {}"
            elif filename.endswith('.go'):
                cmd = "go run {}"
            else:
                cmd = command + " {}"
            os.system(cmd.format(filename))
            logging.info(cmd.format(filename))
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            os._exit(0)
