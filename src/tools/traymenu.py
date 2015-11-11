from time import strftime, sleep
import webbrowser
from tools.config import CONFIG
from tools.platform import Platform
from tools.screenshot import Screen
from tools.systrayicon import SysTrayIcon


class Tray(Platform):
    def __init__(self, storage_provider):
        super(self.__class__, self).__init__()
        self.storage_provider = storage_provider

    def show_traymenu(self):
        pass

    def init_windows(self):
        s = Screen()

        def upload(path):
            url = self.storage_provider.upload(path)
            print(url)
            webbrowser.open_new_tab(url)

        def whole(_):
            sleep(0.3)  # Needed to let the context menu disappear completely before taking a screenshot
            path = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
            s.take_screenshot_whole(path)
            upload(path)

        def crop(_):
            sleep(0.3)  # Needed to let the context menu disappear completely before taking a screenshot
            path = CONFIG.get("General", "tmpdir") + "instantscreen_{}.png".format(strftime("%Y-%m-%d_%H-%I-%S"))
            s.take_screenshot_crop(path)
            upload(path)

        hover_text = "InstantScreen"

        menu_options = (("Capture Desktop", None, whole),
                        ("Capture Area", None, crop))

        self.show_traymenu = lambda: SysTrayIcon("InstantScreen.ico", hover_text, menu_options)

    def init_linux(self):
        pass

    def init_osx(self):
        pass
