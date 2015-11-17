#!/usr/bin/env python3
from time import strftime
import webbrowser
from tools.config import CONFIG
from tools.screenshot import Screen
from storage import *


class InstantShare:
    def __init__(self):
        self.screen = Screen()
        self.storage_provider = storage_providers[CONFIG.get(CONFIG.general, "storage")]()

    def take_screenshot(self, crop=True):
        file = CONFIG.get(CONFIG.general, "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
        if crop:
            self.screen.take_screenshot_crop(file)
        else:
            self.screen.take_screenshot_whole(file)
        url = self.storage_provider.upload(file)
        logging.info("Uploaded file to: %s", url)
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    import argparse
    import logging
    # logging.basicConfig(filename="instantshare.log", level=logging.INFO, format="%(asctime)s\t%(levelname)s:\t%(message)s")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s:\t%(message)s")

    # parse arguments
    parser = argparse.ArgumentParser(description="Take a screenshot and upload it.")
    # dest defines the name of the key in the dictionary.
    # The value will be true (arg present) or false (arg absent)
    # This is behaviour defined using action="store_true"
    parser.add_argument("-w", "--whole", dest="whole", action="store_true",
                        help="Takes a screenshot of the whole screen.")
    parser.add_argument("-c", "--crop", dest="crop", action="store_true",
                        help="Takes a screenshot and lets you crop it.")
    parser.add_argument("-t", "--tray", dest="tray", action="store_true",
                        help="Starts tray mode. Currently only available on Windows.")

    args = vars(parser.parse_args())
    app = InstantShare()

    if args["tray"]:
        from gui.traymenu import Tray
        from tools.toolbox import delay_execution
        logging.info("InstantShare started in \"tray\" mode")

        # define callbacks for menu items in system tray context menu
        tray_callbacks = (
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=False)),
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=True))
        )

        # create tray
        tm = Tray(*tray_callbacks)
        tm.show()
    elif args["whole"]:
        logging.info("InstantShare started in \"whole screen\" mode")
        app.take_screenshot(crop=False)
    else:
        logging.info("InstantShare started in \"crop\" mode")
        app.take_screenshot(crop=True)
