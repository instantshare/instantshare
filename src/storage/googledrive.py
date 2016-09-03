from argparse import Namespace
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
import httplib2
import os
import ntpath

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import logging
from tools.config import CONFIG
from tools.persistence import KVStore

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Instantshare'

_name = "googledrive"
# TODO: encryption
kvstore = KVStore(_name)

# FIXME: There is several problems with this:
# - does not use the common oauthtool
# - does not use the implicit flow
# - saves data in arbitrary locations


def upload(file: str) -> str:
    flags = Namespace(auth_host_name='localhost',
                           auth_host_port=[8080, 8090],
                           logging_level='ERROR',
                           noauth_local_webserver=False)
    credentials = _get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    # Returns a list of folders in the root directory with a title equaling the screenshot_dir
    results = service.files().list(
        q="'root' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and title='" + CONFIG.get(
            CONFIG.general, "screenshot_dir") + "'", maxResults=100).execute()
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


def _get_credentials(flags):
    """
    Taken from: https://developers.google.com/drive/web/quickstart/python
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
        Type: oauth2client.client.Credentials
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()  # credentials is oauth2client.client.Credentials
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        logging.info("Storing credentials to: %s", credential_path)
    return credentials
