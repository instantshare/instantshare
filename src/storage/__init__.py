import logging

import getpass
from importlib import import_module

import keyring

from tools import dirs
from tools.config import CONFIG
from tools.encryption import CryptoError
from tools.persistence import KVStore, PersistentDataEncryptedError


def upload_generic_file(path: str):
    _upload(_hoster_for("files"), path)


def upload_text(text: str):
    # TODO come up with a strategy to make this elegant
    # some storage options want a path
    # text only hosters like pastebin probably only need a string -> always make a file in tempdir?
    # Syntax Highlighting for pastebin? -> should be handled by pastebin.py
    pass


def upload_audio(path: str):
    _upload(_hoster_for("audio"), path)


def upload_screenshot(path: str):
    _upload(_hoster_for("screenshots"), path)


def upload_video(path: str):
    _upload(_hoster_for("videos"), path)


def upload_to(hoster: str, path: str):
    _upload(_hoster_called(hoster), path)


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


def _hoster_called(name: str):
    hoster = import_module("storage." + name)

    # get persistent data for storage provider
    hoster.kvstore = _load_persistent_data(name)
    return hoster


def _hoster_for(media_type: str):
    return _hoster_called(CONFIG.get(CONFIG.general, "storage_" + media_type))


def _upload(hoster, path):
    play_sounds = CONFIG.getboolean(CONFIG.general, "notification_sound")

    # upload to storage
    try:
        url = hoster.upload(path)
        if url is None:
            raise RuntimeError
    except:
        if play_sounds:
            import tools.audio as a
            a.play_wave_file(dirs.res + "/error.wav")
        return
    logging.info("Uploaded file to: " + url)

    # execute user defined action
    if CONFIG.getboolean(CONFIG.general, "cb_autocopy"):
        import tools.clipboard as c
        c.Clipboard().set(url)
    else:
        import webbrowser as w
        w.open_new_tab(url)

    # notify user if set
    if play_sounds:
        import tools.audio as a
        a.play_wave_file(dirs.res + "/notification.wav")
