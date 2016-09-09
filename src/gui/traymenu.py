from tools.toolbox import Platform


class Tray(Platform):

    def __init__(self, screenshot_whole, screenshot_crop):
        self.show = lambda: None
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
        self.show = lambda: SysTrayIcon("res/instantshare.ico", "InstantShare", menu_options)

    def init_linux(self):
        # TODO: Implement Linux variant or redo this module using QT
        pass

    def init_osx(self):
        pass
