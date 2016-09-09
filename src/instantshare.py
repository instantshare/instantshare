#!/usr/bin/env python3

# do prep work before importing other modules
import os
from queue import Queue

os.chdir(os.path.dirname(__file__))
from tempfile import gettempdir
from time import strftime
from tools.config import CONFIG
from tools import audio


class InstantShare:
    def __init__(self):
        import importlib
        self.screen = importlib.import_module("screenshot.%s" % CONFIG.get(CONFIG.general, "screenshot_tool"))
        self.storage_provider = importlib.import_module("storage.%s" % CONFIG.get(CONFIG.general, "storage"))

    def take_screenshot(self, crop=True):
        file = "{}/instantscreen_{}.png".format(gettempdir(), strftime("%Y-%m-%d_%H-%I-%S"))
        if crop:
            self.screen.take_screenshot_crop(file)
        else:
            self.screen.take_screenshot_whole(file)

        if not os.path.isfile(file):
            # Capture screen cancelled
            logging.debug("Screen capture cancelled.")
            return

        url = self.storage_provider.upload(file)
        logging.info("Uploaded file to: %s", url)
        if CONFIG.getboolean(CONFIG.general, "cb_autocopy"):
            import tools.clipboard
            tools.clipboard.Clipboard().set(url)
        else:
            import webbrowser
            webbrowser.open_new_tab(url)
        if CONFIG.getboolean(CONFIG.general, "notification_sound"):
            audio.play_notification()



if __name__ == "__main__":
    import argparse
    import logging
    # logging.basicConfig(filename="instantshare.log", level=logging.INFO, format="%(asctime)s\t%(levelname)s:\t%(message)s")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s:\t%(message)s")

    # parse arguments
    parser = argparse.ArgumentParser(description="Take a screenshot and upload it.")
    # dest defines the name of the key in the dictionary.
    # The value will be true (arg present) or false (arg absent)
    # This is behaviour defined using action="store_true"
    parser.add_argument("-w", "--whole", dest="whole", action="store_true",
                        help="Takes a screenshot of the whole screen.")
    parser.add_argument("-c", "--crop", dest="crop", action="store_true",
                        help="Takes a screenshot and lets you crop it.")
    parser.add_argument("-t", "--tray", dest="tray", action="store_true",
                        help="Starts tray mode. Currently only available on Windows.")

    args = vars(parser.parse_args())
    app = InstantShare()

    if args["tray"]:
        from gui.traymenu import Tray
        from tools.hotkey import Hotkey, HotkeyInUseError
        from tools.toolbox import delay_execution
        logging.info("InstantShare started in \"tray\" mode")

        # Event Queue for main thread
        event_queue = Queue()

        # define function callback for tray context menu functionality
        function_callbacks = (
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=False)),
            lambda: delay_execution(0.3, lambda: app.take_screenshot(crop=True))
        )

        # parse hotkeys from config file
        HOTKEY_WHOLE = CONFIG.get("hotkeys", "screenshot_whole").split("+")
        HOTKEY_CROP = CONFIG.get("hotkeys", "screenshot_crop").split("+")

        # enable hotkey functionality
        hotkey_daemon = Hotkey(event_queue)
        try:
            hotkey_daemon.add_hotkey(HOTKEY_WHOLE, lambda: app.take_screenshot(crop=False))
            hotkey_daemon.add_hotkey(HOTKEY_CROP, lambda: app.take_screenshot(crop=True))
        except HotkeyInUseError as e:
            logging.warning(e.error_msg)

        hotkey_daemon.listen()

        # create tray
        traymenu_daemon = Tray(event_queue, *function_callbacks)
        traymenu_daemon.show()

        while True:
            event = event_queue.get()
            event()

    elif args["whole"]:
        logging.info("InstantShare started in \"whole screen\" mode")
        app.take_screenshot(crop=False)
    else:
        logging.info("InstantShare started in \"crop\" mode")
        app.take_screenshot(crop=True)
