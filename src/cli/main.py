"""
Usage: instantshare <command> [<args>...]
       instantshare [-h | --help | -v | --version]
       instantshare help <command>

Commands:
  screen         Share a screenshot of your desktop
  text           Share text from stdin or your clipboard
  video          Record and share a video of your desktop
  audio          Record and share a short audio clip
  file           Share any file from stdin or your clipboard
  gui            Display GUI

See 'instantshare help <command>' for more detailed information.

Options:
  -h, --help     Print this information
  -v, --version  Print the instantshare version
"""
from docopt import docopt, printable_usage
from importlib import import_module
from tools import dirs

import sys
import shlex
import logging


__commands__ = ["screen", "text", "video", "audio", "file", "gui"]


def _setup_config():
    # TODO Error handling
    import tools.config
    tools.config.read()


def _setup_logging(level=logging.INFO, file=False):
    fmtstr = "%(asctime)s\t%(levelname)s:\t%(message)s"
    if file:
        filename = dirs.logs + "/logfile.log"
        logging.basicConfig(filename=filename, level=level, format=fmtstr)
    else:
        logging.basicConfig(level=level, format=fmtstr)


def _get_module(cmd):
    if cmd is None:
        print(printable_usage(__doc__), file=sys.stderr)
        sys.exit(1)
    elif cmd not in __commands__:
        print("Command not found. Available commands: " + ", ".join(__commands__), file=sys.stderr)
        sys.exit(1)
    else:
        return import_module(__package__ + "." + cmd)


def _execute_command(argv: list):
    _get_module(argv[0]).main(argv)


def execute_command(cmd: str):
    _execute_command(shlex.split(cmd))


def main():
    _setup_config()
    _setup_logging(file=False)

    # TODO access centralized version information
    args = docopt(__doc__, options_first=True, version="instantshare version 0.1")
    if args["<command>"] == "help":
        if len(args["<args>"]) == 0:
            print(printable_usage(__doc__), file=sys.stderr)
            sys.exit(1)
        cmd = args["<args>"][0]
        _execute_command([cmd, "--help"])
    else:
        argv = [args['<command>']] + args['<args>']
        _execute_command(argv)


if __name__ == "__main__":
    main()
