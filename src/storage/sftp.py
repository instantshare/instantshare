import logging
import ntpath
import sys

import paramiko

from tools.config import CONFIG

_name = "sftp"

# Load SFTP server info from config file
HOSTNAME = CONFIG.get(_name, "hostname")
PORT = CONFIG.getint(_name, "port")
USERNAME = CONFIG.get(_name, "username")
AUTHENTICATION_TYPE = CONFIG.get(_name, "authentication_type")


def upload(file: str):
    # Upload preparations
    transport, sftp_client = _connect()
    screenshot_dir = CONFIG.get(CONFIG.general, "screenshot_dir")
    sftp_filepath = screenshot_dir + "/" + ntpath.basename(file)

    _create_dir_if_not_exists(screenshot_dir, sftp_client)

    # Upload
    try:
        sftp_client.put(file, sftp_filepath)
    except IOError as e:
        # State reason for failue without exposing Traceback? Is IOError the correct exception?
        # Documentation: http://docs.paramiko.org/en/2.0/api/sftp.html
        logging.error("Upload failed.")

    # Close
    sftp_client.close()
    transport.close()

    return HOSTNAME + "/" + sftp_filepath


def _create_dir_if_not_exists(directory_name, sftp_client):
    dirs = sftp_client.listdir()
    if directory_name not in dirs:
        sftp_client.mkdir(directory_name)
        logging.info("Directory '{0}' did not exist and was created.".format(directory_name))


def _connect():
    # Create transport object
    try:
        transport = paramiko.Transport((HOSTNAME, PORT))
    except paramiko.ssh_exception.SSHException:
        logging.error("Connection to the host failed. Check hostname and port.")
        sys.exit(0)

    # Start SSH session based on authentication type
    try:
        if AUTHENTICATION_TYPE == "password":
            # FIXME: Don't save password in unencrypted config file
            password = CONFIG.get(_name, "password")
            transport.connect(username=USERNAME, password=password)

        elif AUTHENTICATION_TYPE == "key":
            # FIXME: Don't save key passphrase in unencrypted config file
            key_filepath = CONFIG.get(_name, "key_filepath")
            key_passphrase = CONFIG.get(_name, "key_passphrase")
            private_key = paramiko.RSAKey.from_private_key_file(key_filepath, key_passphrase)
            transport.connect(username=USERNAME, pkey=private_key)

        else:
            logging.error("Unknown authentication type.")

    except paramiko.ssh_exception.AuthenticationException:
        logging.error("Login failed. Check username and password or private key and passphrase.")
        sys.exit(0)

    return transport, paramiko.SFTPClient.from_transport(transport)
