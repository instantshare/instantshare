import logging
import ntpath

import httplib2
from apiclient import discovery
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from oauth2client.client import AccessTokenCredentials

from tools.config import CONFIG
from tools.oauthtool import implicit_flow
from tools.persistence import KVStub

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Instantshare'
_name = "googledrive"

kvstore = KVStub()


def upload(file: str) -> str:
    # TODO: Use another way to find out if the access token is valid
    # FIXME: Check for authorization failure
    if "access_token" not in kvstore.keys():
        authorization_successful = _authorize()
        if not authorization_successful:
            return None  # unable to upload without successful authorization

    credentials = AccessTokenCredentials(kvstore["access_token"], "test")
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('drive', 'v2', http=http, cache_discovery=False)

    # Returns a list of folders in the root directory with a title equaling the screenshot_dir
    results = service.files().list(
        q="'root' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"
          " and title='" + CONFIG.get(CONFIG.general, "screenshot_dir") + "'",
        maxResults=100
    ).execute()
    items = results.get('items', [])

    # Checks if the directory already exists and if not it will create it
    if not items:
        folder_body = {
            'title': CONFIG.get(CONFIG.general, "screenshot_dir"),
            'parents': ['root'],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        try:
            return_folder = service.files().insert(body=folder_body).execute()
            folder_id = return_folder.get("id")
        except errors.HttpError as e:
            logging.error(e)
            return None
    else:
        folder_id = items[0]['id']

    # Defines some bodies for communicating with Google Drive
    media_body = MediaFileUpload(file, resumable=True)
    body = {
        'title': ntpath.basename(file),
        'description': 'Screenshot',
        'parents': [{'id': folder_id}],
        'writersCanShare': True
    }

    new_permission = {
        'role': 'reader',
        'type': 'anyone'
    }

    try:
        # Uploads the file to Drive
        return_file = service.files().insert(body=body, media_body=media_body).execute()
        logging.info("Google Drive upload done")
        # Shares the file so everybody with the link can read it
        service.permissions().insert(fileId=return_file['id'], body=new_permission).execute()
        logging.info("Google Drive permissions set")
        # Inserts the file ID into another URL for a better image view in the browser
        ret_str = "http://drive.google.com/uc?export=view&id=" + return_file['selfLink'].split("/files/")[1]
        return ret_str
    except errors.HttpError as e:
        logging.info(e)
        return None


def _authorize():
    authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    app_key = CONFIG.get(_name, "app_key")

    # Start OAuth2 implicit flow
    auth_response = implicit_flow(authorization_endpoint, app_key, scope=[SCOPES])

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    kvstore["access_token"] = auth_response["access_token"]
    kvstore.sync()

    return True
