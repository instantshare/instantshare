import threading
import webbrowser
from urllib.parse import quote


def upload(file: str) -> str:
    data = open(file, "r").read()
    url = "https://twitter.com/intent/tweet?text=" + quote(data, safe="")
    threading.Thread(target=lambda: webbrowser.open(url)).start()
    return data
