"""
Take a cropped screenshot and share its public URL.

Usage: instantshare screen [options]

Options:
  -h, --help            Print this information
  -w, --whole           Take a screenshot of the whole screen instead
  --tool=<tool>         Overwrite the screenshot_tool config parameter
  --storage=<provider>  Overwrite the storage config parameter
"""
import os
import logging
import keyring
import getpass

from docopt import docopt
from tools.config import CONFIG
from tools.encryption import CryptoError
from tools.persistence import KVStore, PersistentDataEncryptedError
from importlib import import_module
from tempfile import gettempdir
from time import strftime


def _load_persistent_data(module: str):
    encryption = CONFIG.get(CONFIG.general, "encryption")
    if encryption == "password":
        pass

    elif encryption == "keyring":
        # retrieve password from keyring or create one
        user = getpass.getuser()
        pw = keyring.get_password("instantshare", user)
        if pw is None:
            pw = getpass.getpass("Please enter your encryption password:")
            keyring.set_password("instantshare", user, pw)

        while True:
            try:
                return KVStore(module, pw)
            except CryptoError:
                pw = getpass.getpass("[Decryption Failure] Enter password:")

    else:
        try:
            return KVStore(module)
        except PersistentDataEncryptedError:
            pw = getpass.getpass("Previous encryption password (one last time):")

            while True:
                try:
                    kvs = KVStore(module, pw, unlock=True)
                    try:  # if the above succeeded, try to remove password from keyring
                        user = getpass.getuser()
                        keyring.delete_password("instantshare", user)
                    except:
                        # keyring backend spec does not include exception type
                        pass  # password did not exist, so we don't need to remove it
                    return kvs
                except CryptoError:
                    pw = getpass.getpass("[Decryption Failure] Enter password:")


def main(argv):
    args = docopt(__doc__, argv=argv)

    # import modules dynamically
    scrtool_str = args["--tool"] if args["--tool"] else CONFIG.get(CONFIG.general, "screenshot_tool")
    storage_str = args["--storage"] if args["--storage"] else CONFIG.get(CONFIG.general, "storage")
    scrtool = import_module("screenshot." + scrtool_str)
    storage = import_module("storage." + storage_str)

    # get persistent data for storage provider
    storage.kvstore = _load_persistent_data(storage_str)

    # build filename
    file = "{}/instantscreen_{}.png".format(gettempdir(), strftime("%Y-%m-%d_%H-%I-%S"))

    # take screenshot
    if args["--whole"]:
        scrtool.take_screenshot_whole(file)
    else:
        scrtool.take_screenshot_crop(file)

    if not os.path.isfile(file):
        # Capture screen cancelled
        logging.debug("Screen capture cancelled.")
        return

    # upload to storage
    url = storage.upload(file)
    logging.info("Uploaded screenshot to: " + url)

    # execute user defined action
    if CONFIG.getboolean(CONFIG.general, "cb_autocopy"):
        import tools.clipboard as c
        c.Clipboard().set(url)
    else:
        import webbrowser as w
        w.open_new_tab(url)

    # notify user if set
    if CONFIG.getboolean(CONFIG.general, "notification_sound"):
        import tools.audio as a
        a.play_wave_file("res/notification.wav")
