"""
Take a cropped screenshot and share its public URL.

Usage: instantshare.py screen [options]

Options:
  -w, --whole           Take a screenshot of the whole screen instead
  --tool=<tool>         Overwrite the screenshot_tool config parameter
  --storage=<provider>  Overwrite the storage config parameter
"""
from docopt import docopt
from tools.config import CONFIG
from importlib import import_module
from tempfile import gettempdir
from time import strftime
import logging


def main(argv):
    args = docopt(__doc__, argv=argv)

    # import modules dynamically
    scrtool = args["--tool"] if args["--tool"] else CONFIG.get(CONFIG.general, "screenshot_tool")
    storage = args["--storage"] if args["--storage"] else CONFIG.get(CONFIG.general, "storage")
    scrtool = import_module("screenshot." + scrtool)
    storage = import_module("storage." + storage)

    # build filename
    file = "{}/instantscreen_{}.png".format(gettempdir(), strftime("%Y-%m-%d_%H-%I-%S"))

    # take screenshot
    if args["--whole"]:
        scrtool.take_screenshot_whole(file)
    else:
        scrtool.take_screenshot_crop(file)

    # upload to storage
    url = storage.upload(file)
    logging.info("Uploaded screenshot to: " + url)

    # execute user defined action
    if CONFIG.getboolean(CONFIG.general, "cb_autocopy"):
        import tools.clipboard as c
        c.Clipboard().set(url)
    else:
        import webbrowser as w
        w.open_new_tab(url)

    # notify user if set
    if CONFIG.getboolean(CONFIG.general, "notification_sound"):
        import tools.audio as a
        a.play_notification()
