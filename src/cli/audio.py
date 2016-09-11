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
import logging

from docopt import docopt
from importlib import import_module
from time import sleep, strftime
from tempfile import gettempdir

from tools.audio import WaveRecorder
from tools.config import CONFIG


# TODO this command shares a lot of code with screen.py
# Somewhere, we need a file containing our generic program flows,
# like build_filename(schema), upload(file), upload_done(url)
def main(argv):
    args = docopt(__doc__, argv=argv)

    # dynamic imports
    storage = args["--storage"] if args["--storage"] else CONFIG.get(CONFIG.general, "storage")
    storage = import_module("storage." + storage)

    # build filename
    path = "{}/recording_{}.wav".format(gettempdir(), strftime("%Y-%m-%d_%H-%I-%S"))

    with WaveRecorder() as rec:

        # record audio
        if args["--stdin"] or len(argv) == 1:  # TODO redo when GUI implemented
            rec.start_record()
            input()
            rec.stop_record()
        elif args["--seconds"]:
            rec.start_record()
            sleep(int(args["--seconds"]))
            rec.stop_record()

        # TODO preview recording to user before upload

        # save recording
        rec.save(path)

    # upload to storage
    url = storage.upload(path)
    logging.info("Uploaded recording to: " + url)

    # execute user defined action
    if CONFIG.getboolean(CONFIG.general, "cb_autocopy"):
        import tools.clipboard as c
        c.Clipboard().set(url)
    else:
        import webbrowser as w
        w.open_new_tab(url)

    # notify user if set
    if CONFIG.getboolean(CONFIG.general, "notification_sound"):
        import tools.audio as a
        a.play_wave_file("res/notification.wav")
