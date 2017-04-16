from time import sleep
from abc import ABCMeta, abstractmethod
from sys import platform as _platform


def delay_execution(t, fn):
    sleep(t)
    return fn()


class Platform(metaclass=ABCMeta):

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
        init_functions = {
            "linux": self.init_linux,
            "win32": self.init_windows,
            "darwin": self.init_osx
        }
        if _platform not in init_functions.keys():
            raise OSError("Platform not supported!")
        else:
            init_functions[_platform]()
