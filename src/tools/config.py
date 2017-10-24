from configparser import ConfigParser
from os import path

import tools.dirs as dirs
from tools.toolbox import deserialize

config = {}
general = "General"

__config_file = dirs.configs + "/instantshare.conf"
__default_file = dirs.res + "/instantshare.default"


def __dynamic_defaults():
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
    elif platform == "darwin":
        return {"$SCREENSHOT_TOOL": "macos_screenshot"}


def read(file: str=__config_file) -> dict:
    """
    Read config file and initialize this module.
    :raises IOError: when config file does not exist.
    :raises configparser.Error: when the file exists, but there are parsing errors.
    """
    global config

    if not path.isfile(file) or path.getsize(file) == 0:
        raise IOError

    parser = ConfigParser()
    parser.read(file)
    for section in parser.sections():
        config[section] = dict(parser.items(section))
        for key in config[section].keys():
            config[section][key] = deserialize(config[section][key])
    return config


def write(configuration: dict=config, file: str=__default_file):
    global config

    with open(file, "w") as fp:
        config = configuration
        parser = ConfigParser()
        for section in config.keys():
            for key in config[section].keys():
                parser.set(section, key, config[section][key])
        parser.write(fp)


def create_instantshare_default_config():
    with open(__default_file) as _in, open(__config_file, "w") as _out:
        content = _in.read()
        replace = __dynamic_defaults()
        for key in replace.keys():
            content = content.replace(key, replace[key])
        _out.write(content)
    read()
