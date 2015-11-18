import logging
import ntpath
import sys
import storage
import paramiko
from tools.config import CONFIG


@storage.register
class Sftp(storage.Base):
    def __init__(self):
        super().__init__()
        self.username = CONFIG.get(self.name(), "username")
        self.password = CONFIG.get(self.name(), "password")
        self.hostname = CONFIG.get(self.name(), "hostname")
        self.port = CONFIG.getint(self.name(), "port")


    @staticmethod
    def name():
        return "sftp"

    def upload(self, file: str):
        try:
            transport = paramiko.Transport((self.hostname, self.port))
        except paramiko.ssh_exception.SSHException:
            logging.error("Connection to the host failed. Check hostname and port.")
            sys.exit(0)
        try:
            transport.connect(username=self.username, password=self.password)
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
        return self.hostname + "/" + web_path
