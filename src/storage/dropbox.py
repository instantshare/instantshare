import logging
import ntpath

import dropbox
from dropbox.files import WriteMode

from tools.config import CONFIG
from tools.oauthtool import implicit_flow
from tools.persistence import KVStore

_name = "dropbox"
# TODO: encryption
kvstore = KVStore(_name)


def upload(file: str) -> str:
    # TODO: Use another way to find out if the access token is valid
    # FIXME: Check for authorization failure
    if "access_token" not in kvstore.keys():
        authorization_successful = _authorize()
        if not authorization_successful:
            return None  # unable to upload without successful authorization

    token = kvstore["access_token"]
    dropbox_client = dropbox.Dropbox(token)
    dropbox_filepath = "/" + CONFIG.get(CONFIG.general, "screenshot_dir") + "/" + ntpath.basename(file)
    file_object = open(file, 'rb')

    try:
        file_metadata = dropbox_client.files_upload(file_object, dropbox_filepath, mode=WriteMode("overwrite", None),
                                                    client_modified=None, mute=False)
    except dropbox.exceptions.ApiError as e:
        logging.error("Upload failed. Error message: {0}".format(e.error_msg))
        return None

    try:
        url = dropbox_client.sharing_create_shared_link_with_settings(dropbox_filepath, None).url
    except dropbox.exceptions.ApiError as e:
        logging.error("Could not create shared link. Error message: {0}".format(e.error_msg))
        return None

    return _change_url_suffix(url)


def _authorize():
    authorization_endpoint = "https://www.dropbox.com/oauth2/authorize"
    app_key = CONFIG.get(_name, "app_key")

    # Start OAuth2 implicit flow
    auth_response = implicit_flow(authorization_endpoint, app_key)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    kvstore["access_token"] = auth_response["access_token"]
    kvstore.sync()

    return True


def _change_url_suffix(url):
    # Modifies URL that it directly refers to the uploaded file.
    suffix = "dl=0"
    raw_suffix = "raw=1"

    if url.endswith(suffix):
        url = url.replace(suffix, raw_suffix)

    return url
