from tools.platform import Platform
import screenshot.win
import screenshot.linux
from time import strftime
from tempfile import gettempdir


tmpdir = gettempdir()
if Platform.this == Platform.LINUX:
    take_screenshot = screenshot.linux.take_screenshot
    tmpdir += '/'
elif Platform.this == Platform.WINDOWS:
    take_screenshot = screenshot.win.take_screenshot
    tmpdir += '\\'

file = tmpdir + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
take_screenshot(file)

