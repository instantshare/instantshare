import enum
import os
from tempfile import gettempdir
from time import strftime

from appdirs import AppDirs

import res as resources

appdirs = AppDirs(
    appname="instantshare",
    appauthor="instantshare",
    version=None
)


def _mk(path):
    os.makedirs(path, exist_ok=True)
    return path


logs = _mk(appdirs.user_log_dir)
configs = _mk(appdirs.user_config_dir)
cache = _mk(appdirs.user_cache_dir)
data = _mk(appdirs.user_cache_dir)
res = str(os.path.dirname(resources.__file__))
temp = gettempdir()


class MediaTypes(enum.Enum):
    SCREENSHOT = "screenshot"
    AUDIO = "audio"
    TEXT = "text"
    VIDEO = "video"


def build_filename(media_type: MediaTypes) -> str:
    """
    Builds a filename for a shared file of the given type.
    
    :param media_type: a media type to build the filename for
    
    :return: a full path including the name
    """
    file_extension = {
        MediaTypes.SCREENSHOT: ".png",
        MediaTypes.AUDIO: ".wav",
        MediaTypes.TEXT: ".txt",
        MediaTypes.VIDEO: ".webm"
    }.get(media_type, "")

    return "{0}/instantshare_{1}_{2}{3}".format(
        gettempdir(),
        media_type,
        strftime("%Y-%m-%d_%H-%I-%S"),
        file_extension
    )


if __name__ == "__main__":
    print("Log dir:      " + logs)
    print("Config dir:   " + configs)
    print("Cache dir:    " + cache)
    print("Userdata dir: " + data)
