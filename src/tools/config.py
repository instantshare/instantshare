from configparser import ConfigParser
import logging
from os import path


class Config(ConfigParser):
    """
    Wrapper Class for ConfigParser, includes default config, automated read on create, etc.
    Usage:
        1. get config object from module, get config parameters using type safe methods:
            - get() (str)
            - getint()
            - getboolean()
            - getfloat()
        2. Only call read if you want it to read the file again
        3. Only call write if you made configuration changes and want to save them
    """
    general = "General"
    _file = "instantshare.conf"
    _default = "res/instantshare.default"

    def __init__(self):
        super().__init__()
        self.read()

    def __dynamic_defaults(self):
        """
        Used to get all elements for the default configuration that can only
        be determined at runtime, for example platform-specific options.
        :return: Dictionary with config variables to replace.
        """
        from sys import platform
        if platform == "linux":
            return {"$SCREENSHOT_TOOL": "gnome_screenshot"}
        elif platform == "win32":
            return {"$SCREENSHOT_TOOL": "windows_tk"}

    def __default_config(self):
        """
        Creates a new instantshare.conf file from res/instantshare.default,
        replacing all config variables like $SCREENSHOT_TOOL.
        """
        with open(Config._default) as _in, open(Config._file, "w") as _out:
            content = _in.read()
            replace = self.__dynamic_defaults()
            for key in replace.keys():
                content = content.replace(key, replace[key])
            _out.write(content)
        self.read()

    def read(self):
        try:
            if not path.isfile(self._file) or path.getsize(self._file) == 0:
                raise IOError
            super().read([self._file])
        except IOError as e:
            logging.error(e)
            # No config file, create one with default values
            self.__default_config()

    def write(self):
        with open(self._file, mode='w') as fp:
            super().write(fp)

CONFIG = Config()
