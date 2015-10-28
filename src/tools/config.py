from configparser import ConfigParser
from tempfile import gettempdir


class Config(ConfigParser):

    _file = open("instantshare.conf", mode='w', encoding="UTF-8")

    def __init__(self):
        super().__init__()
        self.read()


    def __default_config(self):
        # sane default configuration

        params = {
            "General": {
                "tmpdir": gettempdir() + "/",
                "screenshot_dir": "screenshot",
                "audio_dir": "audio"
            },
            "Dropbox": {

            },
            "Google Drive": {

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
            super().read(self._file, "UTF-8")
            if "General" not in self.sections():
                raise IOError
        except IOError:
            # No config file, create one with default values
            self.__default_config()

    def write(self):
        super().write(self._file)

CONFIG = Config()
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