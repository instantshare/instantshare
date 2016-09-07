"""
Usage: instantshare.py <command> [<args>...]
       instantshare.py [-h | --help | -v | --version]
       instantshare.py help <command>

Commands:
  screen         Share a screenshot of your desktop
  text           Share text from stdin or your clipboard
  video          Record and share a video of your desktop
  audio          Record and share a short audio clip
  file           Share any file from stdin or your clipboard
  gui            Display GUI

See 'instantshare.py help <command>' for more detailed information.

Options:
  -h, --help     Print this information
  -v, --version  Print the instantshare version
"""
from docopt import docopt, printable_usage
from importlib import import_module

import os
import sys
import logging


__commands__ = ["screen", "text", "video", "audio", "file", "gui"]


def _setup_logging(level=logging.INFO, filename=None):
    fmtstr = "%(asctime)s\t%(levelname)s:\t%(message)s"
    if filename:
        logging.basicConfig(filename=filename, level=level, format=fmtstr)
    else:
        logging.basicConfig(level=level, format=fmtstr)


def _get_module(cmd):

    if cmd is None:
        print(printable_usage(__doc__))
        sys.exit(1)
    elif cmd not in __commands__:
        print("Command not found. Available commands: " + ", ".join(__commands__))
        sys.exit(1)
    else:
        return import_module(cmd, ".")


def main():
    # TODO: Issue #20
    project_home = os.path.dirname(os.path.abspath(__file__)) + "/.."
    os.chdir(project_home)

    _setup_logging()

    args = docopt(__doc__, options_first=True)
    if args["--help"]:
        print(__doc__)
    elif args["--version"]:
        # TODO access centralized version information
        print("instantshare version 0.1")
    elif args["<command>"] == "help":
        cmd = args["<args>"][0]
        print(_get_module(cmd).__doc__)
    else:
        cmd = args['<command>']
        argv = [cmd] + args['<args>']
        _get_module(args["<command>"]).main(argv)


def execute_command(cmd, argv=None, *args, **kwargs):
    if not argv:
        argv = list(args) + ["--{}={}".format(k, v) for k, v in kwargs]
    _get_module(cmd).main(argv)

if __name__ == "__main__":
    main()
