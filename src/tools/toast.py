from tools import dirs
from tools.toolbox import Platform


class Toast(Platform):
    def __init__(self):
        self.show = lambda title, message, icon, timeout: None
        super().__init__()

    def init_linux(self):
        def show(title, message, icon=dirs.res + "/instantshare.ico", timeout=0):
            from subprocess import Popen, PIPE
            import shlex
            cmd = shlex.split(
                "notify-send --icon={icon} --expire-time={timeout} \"{title}\" \"{message}\"".format(
                    icon=str(icon),
                    timeout=str(timeout * 1000),
                    title=title,
                    message=message
                )
            )
            Popen(cmd).communicate()

        self.show = show

    def init_windows(self):
        def s(title, message, icon=dirs.res + "/instantshare.ico", timeout=0):
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, icon, timeout)

        self.show = s

    def init_osx(self):
        # AppleScript language doesn't support specifying an icon or a timeout value
        def show(title, message):
            import os
            os.system("""
                          osascript -e 'display notification "{}" with title "{}"'
                          """.format(message, title))

        self.show = show
