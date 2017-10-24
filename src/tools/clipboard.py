from tools.toolbox import Platform
from subprocess import Popen, PIPE


class Clipboard(Platform):
    def __init__(self):
        self.set = lambda data: None
        self.get = lambda: None
        super().__init__()

    def init_linux(self):
        import shlex

        def s(data):
            cmd = shlex.split("xclip -selection clipboard")
            p = Popen(cmd, stdin=PIPE)
            p.communicate(input=bytes(data, encoding="utf-8"))

        def g():
            cmd = shlex.split("xclip -o -selection clipboard")
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            if out is None:
                raise OSError(err)
            else:
                return str(out, encoding="utf-8")

        self.set = s
        self.get = g

    def init_windows(self):
        from tkinter import Tk

        def s(data):
            Popen("clip", stdin=PIPE).communicate(input=bytes(data, encoding="utf-8"))

        def g():
            r = Tk()
            r.withdraw()
            data = r.clipboard_get()
            r.destroy()
            return data

        self.set = s
        self.get = g

    def init_osx(self):
        def s(data):
            p = Popen("pbcopy", stdin=PIPE).communicate(input=bytes(data, encoding="utf-8"))

        def g():
            p = Popen("pbpaste", stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            if out is None:
                raise OSError(err)
            else:
                return str(out, encoding="utf-8")

        self.set = s
        self.get = g
