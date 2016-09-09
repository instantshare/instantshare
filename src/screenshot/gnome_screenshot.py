from subprocess import call


def take_screenshot_crop(path):
    call(["gnome-screenshot", "-a", "-f", path])


def take_screenshot_whole(path):
    call(["gnome-screenshot", "-f", path])
