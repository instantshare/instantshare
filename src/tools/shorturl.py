from abc import abstractmethod, ABCMeta
from urllib import request


class UrlShortener(metaclass=ABCMeta):
    @abstractmethod
    def shorten(self, url: str) -> str:
        pass


class Off(UrlShortener):
    def shorten(self, url: str):
        return url


class TinyURL(UrlShortener):
    def shorten(self, url: str) -> str:
        response = request.urlopen("http://tinyurl.com/api-create.php?url={}".format(url))
        return str(response.read(), encoding="ascii")


def get_url_shortener(name: str) -> UrlShortener:
    if name == "tinyurl":
        return TinyURL()
    return Off()
