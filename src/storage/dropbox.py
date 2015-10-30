from pip._vendor.distlib.compat import raw_input
from storage.storage import Storage
from tools.config import CONFIG
import dropbox
import ntpath
import webbrowser


class Dropbox(Storage):
    def initialize(self):
        # TODO: Add routine for safely stored app_key and app_secret
        app_key = CONFIG.get("dropbox", "app_key")
        app_secret = CONFIG.get("dropbox", "app_secret")

        if CONFIG.get("dropbox", "access_token") == "0":
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
            authorize_url = flow.start()

            webbrowser.open_new_tab(authorize_url)
            code = raw_input("Enter the authorization code here: ").strip()

            access_token, user_id = flow.finish(code)

            CONFIG.set("dropbox", "access_token", access_token)
            CONFIG.set("dropbox", "user_id", user_id)
            CONFIG.write()

        self.access_token = CONFIG.get("dropbox", "access_token")
        self.user_id = CONFIG.get("dropbox", "user_id")

    def upload(self, file: str) -> str:
        f = open(file, 'rb')
        # According to DropboxClient, this documentation is deprecated:
        # https://www.dropbox.com/developers-v1/core/start/python
        dropbox_client = dropbox.client.DropboxClient(self.access_token)
        dropbox_filepath = CONFIG.get("General", "screenshot_dir") + "/" + ntpath.basename(file)

        try:
            response = dropbox_client.put_file(dropbox_filepath, f)
        except dropbox.rest.ErrorResponse as e:
            print(e.error_msg)

        url = dropbox_client.media(dropbox_filepath)["url"]
        return url
