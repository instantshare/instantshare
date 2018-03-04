import logging
import getpass
from importlib import import_module

import keyring

from gui.dialogs import text_input
from tools import dirs
from tools.config import config, general
from tools.encryption import CryptoError
from tools.persistence import KVStore, PersistentDataEncryptedError
from tools.shorturl import get_url_shortener


def upload_generic_file(path: str):
    _upload(_hoster_for("files"), path)


def upload_text(path: str):
    _upload(_hoster_for("text"), path)


def upload_audio(path: str):
    _upload(_hoster_for("audio"), path)


def upload_screenshot(path: str):
    _upload(_hoster_for("screenshots"), path)


def upload_video(path: str):
    _upload(_hoster_for("videos"), path)


def upload_to(hoster: str, path: str):
    _upload(_hoster_called(hoster), path)


def _load_persistent_data(module: str):
    encryption = config[general]["encryption"]
    if encryption == "password":
        pw = text_input("Encryption password", "Please enter your encryption password:", hidden=True)
        while True:
            try:
                return KVStore(module, pw)
            except CryptoError:
                pw = text_input("Decryption Failure", "Please enter the correct password:", hidden=True)

    elif encryption == "keyring":
        # retrieve password from keyring or create one
        user = getpass.getuser()
        pw = keyring.get_password("instantshare", user)
        if pw is None:
            pw = text_input("Encryption password", "Please enter your encryption password:", hidden=True)
            keyring.set_password("instantshare", user, pw)

        while True:
            try:
                return KVStore(module, pw)
            except CryptoError:
                pw = text_input("Decryption Failure", "Please enter the correct password:", hidden=True)

    else:
        try:
            return KVStore(module)
        except PersistentDataEncryptedError:
            pw = text_input("Encryption Password",
                              "Please enter your previous encryption password (one last time):",
                              hidden=True)
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
                    pw = text_input("Decryption Failure", "Please enter the correct password:", hidden=True)


def _hoster_called(name: str):
    hoster = import_module("storage." + name)

    # get persistent data for storage provider
    hoster.kvstore = _load_persistent_data(name)
    return hoster


def _hoster_for(media_type: str):
    return _hoster_called(config[general]["storage_" + media_type])


def _upload(hoster, path):
    play_sounds = config[general]["notification_sound"]
    show_notifications = config[general]["notification_toast"]

    # upload to storage
    try:
        url = hoster.upload(path)
        if url is None:
            raise Exception
    except Exception as e:
        logging.error("Error occured while uploading file to hoster:\n" + str(e))
        if play_sounds:
            import tools.audio as a
            a.play_wave_file(dirs.res + "/error.wav")
        if show_notifications:
            from tools.toast import Toast
            t = Toast()
            t.show("Error", "Failed to upload media.")
        return
    logging.info("Uploaded file to: " + url)

    # shorten URL as defined in config
    url_shortener = get_url_shortener(config[general]["url_shortener"])
    url = url_shortener.shorten(url)

    # execute user defined action
    if config[general]["cb_autocopy"]:
        import tools.clipboard as c
        c.Clipboard().set(url)
    else:
        import webbrowser as w
        w.open_new_tab(url)

    # notify user if set
    if play_sounds:
        import tools.audio as a
        a.play_wave_file(dirs.res + "/notification.wav")
    if show_notifications:
        from tools.toast import Toast
        t = Toast()
        t.show("Upload Finished", "Media upload was successful.")
