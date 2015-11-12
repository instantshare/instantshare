#!/usr/bin/env python3
from time import strftime
from tools.config import CONFIG
from storage import *
from tools.screenshot import Screen
import webbrowser


class InstantShare:
    s = Screen()

    # initialize storage
    storage_providers = {
        "dropbox": dropbox.Dropbox(),
        "googledrive": googledrive.GoogleDrive(),
        "test": test.Test()
    }
    sp = storage_providers[CONFIG.get("General", "storage")]
    sp.initialize()

    @staticmethod
    def take_screenshot_whole():
        file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
        InstantShare.s.take_screenshot_whole(file)
        InstantShare.upload_file(file)

    @staticmethod
    def take_screenshot_crop():
        file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
        InstantShare.s.take_screenshot_crop(file)
        InstantShare.upload_file(file)

    @staticmethod
    def upload_file(path):
        url = InstantShare.sp.upload(path)
        print(url)
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    import argparse
    from tools.traymenu import Tray
    # parse arguments
    parser = argparse.ArgumentParser(description="Take a screenshot and upload it.")
    # dest defines the name of the key in the dictionary. The value will be true or false (action="store_true")
    parser.add_argument("-w", "--whole", dest="whole", action="store_true",
                        help="Takes a screenshot of the whole screen.")
    parser.add_argument("-c", "--crop", dest="crop", action="store_true",
                        help="Takes a screenshot and lets you crop it.")
    parser.add_argument("-t", "--tray", dest="tray", action="store_true",
                        help="Starts tray mode. Currently only available on Windows.")

    args = vars(parser.parse_args())

    if args.get("tray"):
        tm = Tray()
        tm.show_traymenu()
    elif args.get("whole"):
        InstantShare.take_screenshot_whole()
    else:
        InstantShare.take_screenshot_crop()
