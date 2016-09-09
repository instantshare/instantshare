"""
Start the GUI. A small tray icon will be displayed. Right click on that to
access instantshare's functionality.

The GUI is also required for native hotkey support (which uses the hotkeys
set in instantshare.conf). You can most likely also directly map hotkeys
to commands using your operating system or desktop environment settings.

Usage:  instantshare gui [options]

Options:
  -h, --help  Display this information
"""
import logging
from queue import Queue

from docopt import docopt

from cli.main import execute_command
from gui.traymenu import Tray
from tools.config import CONFIG
from tools.hotkey import Hotkey, HotkeyInUseError, InvalidHotkeyError
from tools.toolbox import delay_execution


def main(argv):
    args = docopt(__doc__, argv)

    # Event Queue for main thread
    event_queue = Queue()

    # define callbacks for menu items in system tray context menu
    tray_callbacks = (
        lambda: delay_execution(0.3, lambda: execute_command("screen --whole")),
        lambda: delay_execution(0.3, lambda: execute_command("screen"))
    )

    # assign callbacks to hotkey options of config file
    hotkey_options_with_callbacks = {
        "screenshot_whole": lambda: execute_command("screen --whole"),
        "screenshot_crop": lambda: execute_command("screen")
    }

    # parse hotkeys from config file and add them to hotkey daemon
    hotkey_daemon = Hotkey(event_queue)
    for hotkey_option, callback in hotkey_options_with_callbacks.items():
        try:
            hotkey = CONFIG.get("hotkeys", hotkey_option).split("+")
            hotkey_daemon.add_hotkey(hotkey, callback)
        except (HotkeyInUseError, InvalidHotkeyError) as e:
            logging.warning(e.error_msg)

    # enable hotkey functionality
    hotkey_daemon.listen()

    # create tray
    logging.info("Creating tray icon for instantshare")
    traymenu_daemon = Tray(event_queue, *tray_callbacks)
    traymenu_daemon.show()

    while True:
        event = event_queue.get()
        event()
