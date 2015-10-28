from tools.platform import Platform
from time import strftime
from tools.config import CONFIG

if Platform.this == Platform.LINUX:
    import screenshot.linux
    take_screenshot = screenshot.linux.take_screenshot
elif Platform.this == Platform.WINDOWS:
    import screenshot.win
    take_screenshot = screenshot.win.take_screenshot

file = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
take_screenshot(file)

