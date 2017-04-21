"""
Upload text from the clipboard or from stdin and share its public URL.

Usage: instantshare text [options]

Options:
  -h, --help            Print this information
  --stdin               Receive text from stdin instead of the clipboard
  --storage=<provider>  Overwrite the storage config parameter
"""
from docopt import docopt

import storage
from tools import dirs


def main(argv):
    args = docopt(__doc__, argv)

    # read data from clipboard or stdin
    if args["--stdin"]:
        import sys
        data = sys.stdin.read()
    else:
        from tools.clipboard import Clipboard
        c = Clipboard()
        data = c.get()

    # save to file
    file_path = dirs.build_filename(dirs.MediaTypes.TEXT)
    with open(file_path, "w") as text_file:
        text_file.writelines(data)

    # upload
    hoster = args["--storage"]
    if hoster:
        storage.upload_to(hoster, file_path)
    else:
        storage.upload_text(file_path)