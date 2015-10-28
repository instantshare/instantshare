from __future__ import print_function
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
import httplib2
import os
import ntpath

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from storage.storage import Storage
from tools.platform import Platform

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
DRIVE_SCREENSHOT_DIR = 'Screenshots'


class GoogleDrive(Storage):
    def __init__(self):
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None
        self.initialize()

    def initialize(self):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v2', http=self.http)

    def upload(self, file: str) -> str:
        results = self.service.files().list(q="'root' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and title='"+DRIVE_SCREENSHOT_DIR+"'", maxResults=100).execute()
        items = results.get('items',[])
        folder_id = None
        if not items:
            folder_body = {
                'title': DRIVE_SCREENSHOT_DIR,
                'parents': ['root'],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            try:
                returnFolder = self.service.files().insert(body=folder_body).execute()
            except errors.HttpError as e:
                print(e)
            folder_id = returnFolder.get("id")
        else:
            folder_id = items[0]['id']

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
            returnFile = self.service.files().insert(body=body, media_body=media_body).execute()
            print("Upload should be done now!")
            self.service.permissions().insert(fileId=returnFile['id'], body=new_permission).execute()
            print("Permissions should be set now!")
            retStr = "http://drive.google.com/uc?export=view&id=" + returnFile['selfLink'].split("/files/")[1]
            print(retStr)
            return retStr
        except errors.HttpError as e:
            print(e)
            return None

    def get_credentials(self):
        """Gets valid user credentials from storage.

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
        credentials = store.get()       # credentials is oauth2client.client.Credentials
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME

            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)

            #credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials