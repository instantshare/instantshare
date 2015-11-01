#!/usr/bin/env python3
from tools.platform import Platform
from time import strftime
from tools.config import CONFIG
from storage import *
import webbrowser

# take screenshot
if Platform.this == Platform.LINUX:
    import screenshot.linux
    take_screenshot_crop = screenshot.linux.take_screenshot_crop
    take_screenshot_whole = screenshot.linux.take_screenshot_whole
elif Platform.this == Platform.WINDOWS:
    import screenshot.win
    take_screenshot_crop = screenshot.win.take_screenshot_crop
    take_screenshot_whole = screenshot.win.take_screenshot_whole

file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
take_screenshot_crop(file)

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
