import logging

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from tools.config import CONFIG
from tools.oauthtool import implicit_flow
from tools.persistence import KVStore

_name = "imgur"
# TODO: encryption
kvstore = KVStore(_name)


def upload(file: str) -> str:
    # Anonymous upload.
    # TODO: Upload to a specific user account. See #8.
    client_id = CONFIG.get(_name, "client_id")

    # access_token = kvstore["access_token"]
    # refresh_token = kvstore["refresh_token"]

    imgur_client = ImgurClient(client_id, None, None, None)

    try:
        file_metadata = imgur_client.upload_from_path(file)
    except ImgurClientError as e:
        logging.error("Upload failed. Error message: {0}".format(e.error_message))

    url = file_metadata["link"]
    return url


def _authorize():
    # For issue #8
    authorization_endpoint = "https://api.imgur.com/oauth2/authorize"
    client_id = CONFIG.get(_name, "client_id")

    # Start OAuth2 implicit flow
    auth_response = implicit_flow(authorization_endpoint, client_id)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    kvstore["access_token"] = auth_response["access_token"]
    kvstore["refresh_token"] = auth_response["refresh_token"]
    kvstore["expires_in"] = auth_response["expires_in"]
    kvstore.sync()

    return True
