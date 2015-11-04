#!/usr/bin/env python3
from time import strftime
from tools.config import CONFIG
from storage import *
from tools.screenshot import Screen
import webbrowser

# take screenshot
s = Screen()
file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
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
