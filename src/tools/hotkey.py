import threading

from pyhooked import KeyboardEvent, Hook

from tools.platform import Platform

_name = "hotkeys"


class Hotkey(Platform):
    def __init__(self, screenshot_whole, screenshot_crop):
        self.screenshot_whole = screenshot_whole
        self.screenshot_crop = screenshot_crop
        super().__init__()

    def init_osx(self):
        pass

    def init_linux(self):
        pass

    def init_windows(self):
        def handle_events(args):
            if isinstance(args, KeyboardEvent):
                if 'F7' in args.pressed_key and args.event_type == 'key down':
                    thread = threading.Thread(target=self.screenshot_crop)
                    thread.start()

        hk = Hook()  # make a new instance of PyHooked
        hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
        thread = threading.Thread(target=hk.hook)
        thread.start()
