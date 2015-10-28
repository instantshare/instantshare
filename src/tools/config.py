from configparser import ConfigParser
from tempfile import gettempdir
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

    _file = "instantshare.conf"

    def __init__(self):
        super().__init__()
        self.read()

    def __default_config(self):
        # sane default configuration
        params = {
            "General": {
                "tmpdir": gettempdir() + "/",
                "screenshot_dir": "Screenshots",
                "audio_dir": "AudioSnippets",
                "storage": "googledrive"
            },
            "dropbox": {
                "access_token": "0",
                "user_id": "0"
            },
            "googledrive": {

            }
        }
        # write configuration to file
        for section in params:
            self.add_section(section)
            for option in params[section]:
                self.set(section, option, params[section][option])
        self.write()

    def read(self):
        try:
            if not path.isfile(self._file) or path.getsize(self._file) == 0:
                raise IOError
            super().read([self._file])
        except IOError as e:
            print(e)
            # No config file, create one with default values
            self.__default_config()

    def write(self):
        with open(self._file, mode='w') as fp:
            super().write(fp)

CONFIG = Config()
