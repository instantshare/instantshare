"""
Take a cropped screenshot and share its public URL.

Usage: instantshare screen [options]

Options:
  -h, --help            Print this information
  -w, --whole           Take a screenshot of the whole screen instead
  --tool=<tool>         Overwrite the screenshot_tool config parameter
  --storage=<provider>  Overwrite the storage config parameter
"""
import logging
import os
from importlib import import_module

from docopt import docopt

import storage
from tools import dirs
from tools.config import config, general


def main(argv):
    args = docopt(__doc__, argv=argv)

    # import modules dynamically
    scrtool_str = args["--tool"] if args["--tool"] else config[general]["screenshot_tool"]
    scrtool = import_module("screenshot." + scrtool_str)

    # build filename
    file = dirs.build_filename(dirs.MediaTypes.SCREENSHOT)

    # take screenshot
    if args["--whole"]:
        scrtool.take_screenshot_whole(file)
    else:
        scrtool.take_screenshot_crop(file)

    if not os.path.isfile(file):
        # Capture screen cancelled
        logging.debug("Screen capture cancelled.")
        return

    if args["--storage"]:
        storage.upload_to(args["--storage"], file)
    else:
        storage.upload_screenshot(file)
