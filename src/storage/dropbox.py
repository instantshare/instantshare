import storage
from tools.config import CONFIG
import dropbox
import ntpath
import webbrowser
import logging


@storage.register
class Dropbox(storage.Base):

    def __init__(self):
        super().__init__()
        # TODO: Add routine for safely stored app_key and app_secret
        app_key = CONFIG.get(self.name(), "app_key")
        app_secret = CONFIG.get(self.name(), "app_secret")

        # TODO: Use another way to find out if the access token is valid
        if CONFIG.get(self.name(), "access_token") == "0":
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
            authorize_url = flow.start()

            webbrowser.open_new_tab(authorize_url)
            code = input("Enter the authorization code here: ").strip()

            access_token, user_id = flow.finish(code)

            CONFIG.set(self.name(), "access_token", access_token)
            CONFIG.set(self.name(), "user_id", user_id)
            CONFIG.write()

        self.access_token = CONFIG.get(self.name(), "access_token")
        self.user_id = CONFIG.get(self.name(), "user_id")

    @staticmethod
    def name() -> str:
        return "dropbox"

    def upload(self, file: str) -> str:
        f = open(file, 'rb')
        # According to DropboxClient, this documentation is deprecated:
        # https://www.dropbox.com/developers-v1/core/start/python
        dropbox_client = dropbox.client.DropboxClient(self.access_token)
        dropbox_filepath = CONFIG.get(CONFIG.general, "screenshot_dir") + "/" + ntpath.basename(file)

        try:
            response = dropbox_client.put_file(dropbox_filepath, f)
        except dropbox.rest.ErrorResponse as e:
            logging.error(e.error_msg)

        url = dropbox_client.media(dropbox_filepath)["url"]
        return url
