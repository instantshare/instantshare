import logging
import ntpath

import owncloud

from tools.config import CONFIG
from tools.persistence import KVStub

_name = "owncloud"
kvstore = KVStub()


def upload(file: str) -> str:
    owncloud_url = CONFIG.get(_name, "url")
    oc = owncloud.Client(owncloud_url)

    if not _login(oc):
        return

    # find or create screenshot directory
    dir = CONFIG.get(CONFIG.general, "screenshot_dir")
    try:
        oc.mkdir(dir)
    except:
        pass
    remotefile = "{}/{}".format(dir, ntpath.basename(file))

    # upload file
    oc.put_file(remotefile, file)
    return str(oc.share_file_with_link(remotefile).get_link())


def _login(oc: owncloud.Client):
    kvstore_dirty = False

    # initial case: no username or password present
    if "username" not in kvstore.keys() or "password" not in kvstore.keys():
        kvstore["username"], kvstore["password"] = _get_credentials()
        kvstore_dirty = True

    while True:
        try:
            # try to log in with given credentials
            oc.login(kvstore["username"], kvstore["password"])

            # login worked: save credentials if they're new, break loop
            if kvstore_dirty:
                kvstore.sync()
            return True
        except owncloud.HTTPResponseError as e:
            if e.status_code == 401:  # auth failure: read credentials again
                print("Authentication Failure.")
                kvstore["username"], kvstore["password"] = _get_credentials()
                kvstore_dirty = True
            else:  # other owncloud error
                logging.error("Upload failed. Owncloud Server reply: {}".format(e.status_code))
                return False
        except RuntimeError as e:  # any other error
            logging.error("Upload failed. Error details: {}".format(e))
            return False


def _get_credentials():
    from gui.dialogs import text_input

    user = text_input("OwnCloud Account", "OwnCloud Username:")
    password = text_input("OwnCloud Account", "OwnCloud password:", True)

    return user, password

