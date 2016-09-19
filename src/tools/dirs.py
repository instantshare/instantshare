from appdirs import AppDirs
import os
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


if __name__ == "__main__":
    print("Log dir:      " + logs)
    print("Config dir:   " + configs)
    print("Cache dir:    " + cache)
    print("Userdata dir: " + data)
