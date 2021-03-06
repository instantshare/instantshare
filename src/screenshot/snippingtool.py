from subprocess import call
from PIL import ImageGrab
from libraries.pyrobot import Robot

_r = Robot()


def take_screenshot_whole(path):
    image = _r.take_screenshot()
    image.save(path, "png")


def take_screenshot_crop(path):
    call(["snippingtool", "/clip"])
    image = ImageGrab.grabclipboard()
    if image is not None:
        image.save(path, "png")
