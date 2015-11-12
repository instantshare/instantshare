from tools.platform import Platform
from tools.systrayicon import SysTrayIcon


class Tray(Platform):

    def __init__(self, screenshot_whole, screenshot_crop):
        self.scr_whole = screenshot_whole
        self.scr_crop = screenshot_crop
        super().__init__()

    def show(self):
        pass

    def init_windows(self):
        hover_text = "InstantScreen"

        menu_options = (("Capture Desktop", None, lambda _: self.scr_whole()),
                        ("Capture Area", None, lambda _: self.scr_crop()))

        self.show = lambda: SysTrayIcon("InstantScreen.ico", hover_text, menu_options)

    def init_linux(self):
        pass

    def init_osx(self):
        pass
