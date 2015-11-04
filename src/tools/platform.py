from abc import ABCMeta, abstractmethod
from enum import Enum
from sys import platform as _platform


class Platform(metaclass=ABCMeta):
    LINUX, WINDOWS, OSX = range(3)

    if _platform == "linux":
        this = LINUX
    elif _platform == "win32":
        this = WINDOWS
    elif _platform == "darwin":
        this = OSX

    @abstractmethod
    def init_linux(self):
        pass

    @abstractmethod
    def init_windows(self):
        pass

    @abstractmethod
    def init_osx(self):
        pass

    def __init__(self):
        if Platform.this == Platform.LINUX:
            self.init_linux()
        elif Platform.this == Platform.WINDOWS:
            self.init_windows()
        elif Platform.this == Platform.OSX:
            self.init_osx()
        else:
            raise OSError("Platform not supported!")
