from subprocess import call


def take_screenshot_crop(path):
    call(["screencapture", "-i", path])


def take_screenshot_whole(path):
    call(["screencapture", path])
