"""
Record an audio clip from your default audio input device and share it.
By default, records until there is input via stdin. Use the --seconds=<sec>
option to record for a set duration.

In the future, there will be a small GUI where you can control the recording
manually.

Usage:
  instantshare audio [-h | --help]
  instantshare audio [--stdin | --seconds=<sec>] [--storage=<storage>]

Options:
  -h, --help           Display this information.
  --stdin              Record until there is input from stdin
  --seconds=<sec>      Record for <sec> seconds
  --storage=<storage>  Overwrite the storage config parameter
"""

from time import sleep

from docopt import docopt

import storage
from tools import dirs
from tools.audio import WaveRecorder


def main(argv):
    args = docopt(__doc__, argv=argv)

    file_path = dirs.build_filename(dirs.MediaTypes.AUDIO)

    with WaveRecorder() as rec:

        # record audio
        if args["--stdin"]:
            rec.start_record()
            input()
            rec.stop_record()
        elif args["--seconds"]:
            rec.start_record()
            sleep(int(args["--seconds"]))
            rec.stop_record()
        else:  # default: GUI
            import gui.dialogs as d
            rec.start_record()
            do_upload = d.ok_cancel("Recording...", "Hit [Ok] to upload, [Cancel] to abort.")
            rec.stop_record()
            if not do_upload:
                return None

        # save recording
        rec.save(file_path)

    # upload to storage
    hoster = args["--storage"]
    if hoster:
        storage.upload_to(hoster, file_path)
    else:
        storage.upload_audio(file_path)
