from tools.toolbox import Platform


class Toast(Platform):
    def __init__(self):
        self.show = lambda title, message, icon, timeout: None
        super().__init__()

    def init_linux(self):
        pass

    def init_windows(self):
        def s(title, message, icon=None, timeout=0):
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, icon, timeout)

        self.show = s

    def init_osx(self):
        pass
