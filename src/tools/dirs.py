import appdirs
import os
import res as resources

appdirs.appname = "instantshare"
appdirs.appauthor = "instantshare"


def _mk(path):
    os.makedirs(path, exist_ok=True)
    return path


logs = _mk(appdirs.user_log_dir())
configs = _mk(appdirs.user_config_dir())
cache = _mk(appdirs.user_cache_dir())
data = _mk(appdirs.user_cache_dir())
res = str(os.path.dirname(resources.__file__))
