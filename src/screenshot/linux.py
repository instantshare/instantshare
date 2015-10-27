from subprocess import call


def take_screenshot(path):
    call(["gnome-screenshot", "-a", "-f", path])
