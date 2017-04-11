"""
Take a cropped screenshot and share its public URL.

Usage: instantshare file [options] <filename>

Options:
  -h, --help            Print this information
  --storage=<provider>  Overwrite the storage config parameter
"""
from docopt import docopt

import storage


def main(argv):
    args = docopt(__doc__, argv=argv)

    hoster = args["--storage"]
    file = args["<filename>"]

    if hoster:
        storage.upload_to(hoster, file)
    else:
        storage.upload_generic_file(file)
