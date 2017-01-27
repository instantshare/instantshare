import threading

from tools.toolbox import Platform
from tools import dirs


class Tray(Platform):
    def __init__(self, event_queue, screenshot_whole, screenshot_crop):
        self.show = lambda: None
        self.event_queue = event_queue
        self.scr_whole = screenshot_whole
        self.scr_crop = screenshot_crop
        super().__init__()

    def init_windows(self):
        from libraries.systrayicon import SysTrayIcon

        # build tray, register callbacks
        menu_options = (
            ("Capture Desktop", None, lambda _: self.scr_whole()),
            ("Capture Area", None, lambda _: self.scr_crop())
        )

        def show():
            thread = threading.Thread(
                target=lambda: SysTrayIcon(dirs.res + "/instantshare.ico", "InstantShare", menu_options, self.event_queue),
                daemon=True)
            thread.start()

        self.show = show

    def init_linux(self):
        # TODO: Implement Linux variant or redo this module using QT
        pass

    def init_osx(self):
        pass
