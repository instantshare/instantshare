import re
from abc import ABCMeta, abstractmethod
from sys import platform as _platform
from time import sleep


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

typemap = {
    re.compile(r"True|true|yes|on|False|false|no|off"):
        lambda x: True if x in ("True", "true", "yes", "on") else False,
    re.compile(r"(?:\+|-)?[0-9]+"):
        lambda x: int(x),
    re.compile(r"(?:\+|-)?[0-9]*\.[0-9]+"):
        lambda x: float(x),
}


def deserialize(text: str):
    for rx in typemap.keys():
        if rx.fullmatch(text):
            return typemap[rx](text)
    return text
