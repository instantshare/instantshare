#!/usr/bin/env python3
from time import strftime
from tools.config import CONFIG
from storage import *
from tools.screenshot import Screen
import webbrowser


class InstantShare:
    def __init__(self):
        self.screen = Screen()
        # initialize storage
        storage_providers = {
            "dropbox": dropbox.Dropbox(),
            "googledrive": googledrive.GoogleDrive(),
            "test": test.Test()
        }
        self.storage = storage_providers[CONFIG.get("General", "storage")]
        self.storage.initialize()

    def take_screenshot(self, crop=True):
        file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
        if crop:
            self.screen.take_screenshot_crop(file)
        else:
            self.screen.take_screenshot_whole(file)
        url = self.storage.upload(file)
        print(url)
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    import argparse
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
        from tools.traymenu import Tray
        from tools.toolbox import delay_execution

        # define callbacks for menu items in system tray context menu
        tray_callbacks = (
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=False)),
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=True))
        )

        # create tray
        tm = Tray(*tray_callbacks)
        tm.show()
    elif args["whole"]:
        app.take_screenshot(crop=False)
    else:
        app.take_screenshot(crop=True)
