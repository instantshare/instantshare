#!/usr/bin/env python3

from time import strftime
from tools.config import CONFIG
from storage import *
from tools.screenshot import Screen
import webbrowser
import argparse

#parse arguments
parser = argparse.ArgumentParser(description="Take a screenshot and upload it.")
#dest defines the name of the key in the dictionary. The value will be true or false (action="store_true")
parser.add_argument("-w", "--whole", dest="whole", action="store_true", help="Takes a screenshot of the whole screen.")
parser.add_argument("-c", "--crop", dest="crop", action="store_true", help="Takes a screenshot and lets you crop it.")

args = vars(parser.parse_args())

# take screenshot
s = Screen()
file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))

if args.get("whole"):
    s.take_screenshot_whole(file)
else:
    s.take_screenshot_crop(file)

# initialize storage
storage_providers = {
     "dropbox": dropbox.Dropbox(),
     "googledrive": googledrive.GoogleDrive(),
     "test": test.Test()
}
sp = storage_providers[CONFIG.get("General", "storage")]
sp.initialize()
url = sp.upload(file)
print(url)
webbrowser.open_new_tab(url)
