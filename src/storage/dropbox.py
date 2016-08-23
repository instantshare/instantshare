import logging
import ntpath

import dropbox
from dropbox.files import WriteMode

from tools.config import CONFIG
from tools.oauthtool import implicit_flow

_name = "dropbox"


def upload(file: str) -> str:
    # TODO: Use another way to find out if the access token is valid
    # FIXME: Check for authorization failure
    if CONFIG.get(_name, "access_token") == "0":
        __authorize()

    access_token = CONFIG.get(_name, "access_token")
    account_id = CONFIG.get(_name, "user_id")

    dropbox_client = dropbox.Dropbox(access_token)
    dropbox_filepath = "/" + CONFIG.get(CONFIG.general, "screenshot_dir") + "/" + ntpath.basename(file)
    file_object = open(file, 'rb')

    try:
        file_metadata = dropbox_client.files_upload(file_object, dropbox_filepath, mode=WriteMode("overwrite", None),
                                                    client_modified=None, mute=False)
    except dropbox.exceptions.ApiError as e:
        logging.error("Upload failed. Error message: {0}".format(e.error_msg))

    try:
        url = dropbox_client.sharing_create_shared_link_with_settings(dropbox_filepath, None).url
    except dropbox.exceptions.ApiError as e:
        logging.error("Could not create shared link. Error message: {0}".format(e.error_msg))

    return __validate_url(url)


def __authorize():
    authorization_endpoint = "https://www.dropbox.com/oauth2/authorize"
    app_key = CONFIG.get(_name, "app_key")
    app_secret = CONFIG.get(_name, "app_secret")

    # Start OAuth2 implicit flow
    auth_response = implicit_flow(authorization_endpoint, app_key)

    # Check if authorization was successful
    if auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    # FIXME: Don't save access token in unencrypted config file
    CONFIG.set(_name, "access_token", auth_response["access_token"])
    CONFIG.set(_name, "account_id", auth_response["account_id"])
    CONFIG.write()

    return True


def __validate_url(url):
    suffix = "dl=0"
    raw_suffix = "raw=1"

    if url.endswith(suffix):
        url = url.replace(suffix, raw_suffix)

    return url
