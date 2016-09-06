import threading

from tools.config import CONFIG
from tools.toolbox import Platform

_name = "hotkeys"


class Hotkey(Platform):
    HOTKEY_WHOLE = set(CONFIG.get(_name, "screenshot_whole").split("+"))
    HOTKEY_CROP = set(CONFIG.get(_name, "screenshot_crop").split("+"))

    def __init__(self, event_queue, screenshot_whole, screenshot_crop):
        self.event_queue = event_queue
        self.screenshot_whole = screenshot_whole
        self.screenshot_crop = screenshot_crop
        self.listen = lambda: None

        super().__init__()

    def init_osx(self):
        pass

    def init_linux(self):
        pass

    def init_windows(self):
        from pyhooked import KeyboardEvent, Hook

        def handle_events(args):
            if isinstance(args, KeyboardEvent):
                if self.HOTKEY_WHOLE.issubset(args.pressed_key) and args.event_type == "key down":
                    self.event_queue.put(self.screenshot_whole)

                if self.HOTKEY_CROP.issubset(args.pressed_key) and args.event_type == 'key down':
                    self.event_queue.put(self.screenshot_crop)

        def listen():
            hk = Hook()  # make a new instance of PyHooked
            hk.handler = handle_events  # add callback for occuring events
            thread = threading.Thread(target=hk.hook)
            thread.start()  # start listening on new thread

        self.listen = listen
