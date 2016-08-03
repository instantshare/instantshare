import logging
import ntpath
import sys
import paramiko
from tools.config import CONFIG

_name = "sftp"


def upload(file: str):
    username = CONFIG.get(_name, "username")
    password = CONFIG.get(_name, "password")
    hostname = CONFIG.get(_name, "hostname")
    port = CONFIG.getint(_name, "port")
    try:
        transport = paramiko.Transport((hostname, port))
    except paramiko.ssh_exception.SSHException:
        logging.error("Connection to the host failed. Check hostname and port.")
        sys.exit(0)
    try:
        transport.connect(username=username, password=password)
    except paramiko.ssh_exception.AuthenticationException:
        logging.error("Login failed. Check username and password.")
        sys.exit(0)
    sftp = paramiko.SFTPClient.from_transport(transport)
    screenshot_dir = CONFIG.get(CONFIG.general, "screenshot_dir")
    web_path = screenshot_dir + "/" + ntpath.basename(file)
    dirs = sftp.listdir()
    if screenshot_dir not in dirs:
        sftp.mkdir(screenshot_dir)
        logging.info("Screenshot directory did not exist and was created.")

    sftp.put(file, web_path)
    sftp.close()
    transport.close()
    return hostname + "/" + web_path
