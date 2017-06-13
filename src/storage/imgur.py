import logging
from time import time

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from tools.config import config, general
from tools.oauthtool import implicit_flow
from tools.persistence import KVStub

_name = "imgur"
kvstore = KVStub()


def upload(file: str) -> str:
    client_id = config[_name]["client_id"]
    if "access_token" not in kvstore.keys() or "refresh_token" not in kvstore.keys():
        if not _authorize():
            return None  # unable to authorize

    imgur_client = ImgurClient(client_id, None, kvstore["access_token"], kvstore["refresh_token"])
    file_metadata = None

    while True:
        try:
            file_metadata = imgur_client.upload_from_path(file, anon=False)
            break
        except ImgurClientError as e:
            if e.status_code == 400 and _authorize():
                imgur_client.set_user_auth(kvstore["access_token"], kvstore["refresh_token"])
            else:
                logging.error("Upload failed. Error message: {0}".format(e.error_message))
                return None

    url = file_metadata["link"] if file_metadata else None
    return url


def _authorize():
    authorization_endpoint = "https://api.imgur.com/oauth2/authorize"
    client_id = config[_name]["client_id"]

    # Start OAuth2 implicit flow
    auth_response = implicit_flow(authorization_endpoint, client_id)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    kvstore["access_token"] = auth_response["access_token"]
    kvstore["refresh_token"] = auth_response["refresh_token"]
    kvstore["expires"] = int(time()) + int(auth_response["expires_in"])
    kvstore.sync()

    return True
