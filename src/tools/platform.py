from enum import Enum
from sys import platform as _platform


class Platform(Enum):
    LINUX, WINDOWS, OSX = range(3)

    if _platform == "linux":
        this = LINUX
    elif _platform == "win32":
        this = WINDOWS
    elif _platform == "darwin":
        this = OSX

