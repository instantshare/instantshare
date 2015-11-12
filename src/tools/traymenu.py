from time import sleep
from tools.platform import Platform
from tools.systrayicon import SysTrayIcon
from instantshare import InstantShare


class Tray(Platform):
    def show_traymenu(self):
        pass

    def init_windows(self):
        def cap_whole_click(_):
            sleep(0.3)  # Needed to let the context menu disappear completely before taking a screenshot
            InstantShare.take_screenshot_whole()

        def cap_crop_click(_):
            sleep(0.3)  # Needed to let the context menu disappear completely before taking a screenshot
            InstantShare.take_screenshot_crop()

        hover_text = "InstantScreen"

        menu_options = (("Capture Desktop", None, cap_whole_click),
                        ("Capture Area", None, cap_crop_click))

        self.show_traymenu = lambda: SysTrayIcon("InstantScreen.ico", hover_text, menu_options)

    def init_linux(self):
        pass

    def init_osx(self):
        pass
