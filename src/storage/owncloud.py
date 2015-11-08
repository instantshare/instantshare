import owncloud
from storage.storage import Storage
from tools.config import CONFIG
import ntpath


class Owncloud(Storage):

    def initialize(self):
        owncloud_url = CONFIG.get("Owncloud", "url")
        # TODO: prompt user for password using QT dialog
        user = CONFIG.get("Owncloud", "username")
        pw = CONFIG.get("Owncloud", "password")

        assert owncloud_url and user and pw
        self.oc = owncloud.Client(owncloud_url)
        self.oc.login(user, pw)

    def upload(self, file: str) -> str:
        dir = CONFIG.get("General", "screenshot_dir")
        try:
            self.oc.mkdir(dir)
        except:
            pass
        remotefile = "{}/{}".format(dir, ntpath.basename(file))
        self.oc.put_file(remotefile, file)
        link = self.oc.share_file_with_link(remotefile)
        return link
