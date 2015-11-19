import shlex
from subprocess import Popen, PIPE
import tools.platform


class Clipboard(tools.platform.Platform):

    def __init__(self):
        self.set = lambda data: None
        self.get = lambda: None
        super().__init__()

    def init_linux(self):
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
        pass

    def init_osx(self):
        pass
