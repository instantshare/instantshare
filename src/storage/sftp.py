import logging
import ntpath
import sys

import paramiko

from tools.config import config, general
from tools.persistence import KVStub

_name = "sftp"
kvstore = KVStub()

# Load SFTP server info from config file
HOSTNAME = config[_name]["hostname"]
PORT = config[_name]["port"]
AUTHENTICATION_TYPE = config[_name]["authentication_type"]
SFTP_BASE_DIR = config[_name]["base_dir"]


# The provided user for SFTP upload must have read and write permissions in the SFTP_BASE_DIR
# (The SFTP_BASE_DIR has to exist, the user doesn't need permissions in the parent directory).
# A lack of permissions in SFTP_BASE_DIR will break the SFTP upload functionality.


def upload(file: str):
    # Upload preparations
    transport, sftp_client = _connect()
    try:
        sftp_client.chdir(SFTP_BASE_DIR)
    except IOError:
        logging.error(
            "Can not change into base directory. Please provide a working base directory in your SFTP configuration.")
        sys.exit(0)

    screenshot_dir = config[general]["screenshot_dir"]
    sftp_filepath = screenshot_dir + "/" + ntpath.basename(file)

    _create_dir_if_not_exists(screenshot_dir, sftp_client)

    # Upload
    try:
        sftp_client.put(file, sftp_filepath)
    except IOError:
        # State reason for failue without exposing Traceback? Is IOError the correct exception?
        # Documentation: http://docs.paramiko.org/en/2.0/api/sftp.html
        logging.error("Upload failed.")

    # Close
    sftp_client.close()
    transport.close()

    return "http://" + HOSTNAME + "/" + sftp_filepath


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

    kvstore_dirty = False

    # initial case: no username or password present
    if AUTHENTICATION_TYPE == "password":
        if "username" not in kvstore.keys() or "password" not in kvstore.keys():
            kvstore["username"], kvstore["password"] = _get_credentials("password")
            kvstore_dirty = True
    elif AUTHENTICATION_TYPE == "key":
        if "username" not in kvstore.keys() or "key passphrase" not in kvstore.keys():
            kvstore["username"], kvstore["key passphrase"] = _get_credentials("key passphrase")
            kvstore_dirty = True
    else:
        logging.error("Unknown authentication type")

    while True:
        try:
            if AUTHENTICATION_TYPE == "password":
                transport.connect(username=kvstore["username"], password=kvstore["password"])
                break
            elif AUTHENTICATION_TYPE == "key":
                key_filepath = config[_name]["key_filepath"]
                private_key = paramiko.RSAKey.from_private_key_file(key_filepath, kvstore["key passphrase"])
                transport.connect(username=kvstore["username"], pkey=private_key)
                break
            else:
                logging.error("Unknown authentication type")
        except paramiko.ssh_exception.AuthenticationException:
            logging.info("Authentication failed, prompting the user again.")
            prompt = "password" if AUTHENTICATION_TYPE == "password" else "key passphrase"
            kvstore["username"], kvstore[prompt] = _get_credentials(prompt)
            kvstore_dirty = True

    if kvstore_dirty:
        kvstore.sync()

    return transport, paramiko.SFTPClient.from_transport(transport)


def _get_credentials(prompt):
    from gui.dialogs import text_input

    user = text_input("SFTP username", "Enter your SFTP username, please!")
    password = text_input("SFTP {}".format(prompt), "Enter your SFTP {} please!".format(prompt), hidden=True)

    return user, password