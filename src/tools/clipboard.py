import shlex
from subprocess import call, Popen, PIPE
import tools.platform


class Clipboard(tools.platform.Platform):

    def __init__(self):
        self.set = lambda data: None
        self.get = lambda: None
        super().__init__()

    def init_linux(self):
        def set(data):
            cmd = shlex.split("xclip -selection clipboard")
            p = Popen(cmd, stdin=PIPE)
            p.communicate(input=bytes(data, encoding="utf-8"))

        def get():
            cmd = shlex.split("xclip -o -selection clipboard")
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            if out is None:
                raise OSError(err)
            else:
                return str(out, encoding="utf-8")

        self.set = set
        self.get = get

    def init_windows(self):
        pass

    def init_osx(self):
        pass
