import owncloud
from tools.config import CONFIG
import ntpath

_name = "owncloud"


def upload(file: str) -> str:
    owncloud_url = CONFIG.get(_name, "url")

    # TODO: prompt user for password using QT dialog
    user = CONFIG.get(_name, "username")
    pw = CONFIG.get(_name, "password")

    assert owncloud_url and user and pw
    oc = owncloud.Client(owncloud_url)
    oc.login(user, pw)

    # find or create screenshot directory
    dir = CONFIG.get(CONFIG.general, "screenshot_dir")
    try:
        oc.mkdir(dir)
    except:
        pass
    remotefile = "{}/{}".format(dir, ntpath.basename(file))

    # upload file
    oc.put_file(remotefile, file)
    return str(oc.share_file_with_link(remotefile).get_link())

