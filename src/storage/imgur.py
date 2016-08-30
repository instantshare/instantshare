import logging

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from tools.config import CONFIG
from tools.oauthtool import implicit_flow

_name = "imgur"


def upload(file: str) -> str:
    # Anonymous upload.
    # TODO: Upload to a specific user account. See #8.
    client_id = CONFIG.get(_name, "client_id")

    # access_token = CONFIG.get(_name, "access_token")
    # refresh_token = CONFIG.get(_name, "refresh_token")

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

    # FIXME: Don't save access token in unencrypted config file
    CONFIG.set(_name, "access_token", auth_response["access_token"])
    CONFIG.set(_name, "refresh_token", auth_response["refresh_token"])
    CONFIG.set(_name, "expires_in", auth_response["expires_in"])
    CONFIG.write()

    return True
