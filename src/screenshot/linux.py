from subprocess import call


def take_screenshot(self, path):
    call(["gnome-screenshot", "-a", "-f", path])
