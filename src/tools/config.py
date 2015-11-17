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

    def __default_config(self):
        # sane default configuration
        with open(Config._default) as _in, open(Config._file, "w") as _out:
            _out.write(_in.read())
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
