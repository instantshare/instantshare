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
from docopt import docopt
from cli.main import execute_command

import logging


def main(argv):
    args = docopt(__doc__, argv)
    from gui.traymenu import Tray
    from tools.toolbox import delay_execution

    # define callbacks for menu items in system tray context menu
    tray_callbacks = (
        lambda: delay_execution(0.3, lambda: execute_command("screen --whole")),
        lambda: delay_execution(0.3, lambda: execute_command("screen"))
    )

    # create tray
    logging.info("Creating tray icon for instantshare")
    tm = Tray(*tray_callbacks)
    tm.show()
