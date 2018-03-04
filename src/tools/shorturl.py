import logging
from abc import abstractmethod, ABCMeta
from urllib import request


class UrlShortener(metaclass=ABCMeta):
    @abstractmethod
    def shorten(self, url: str) -> str:
        pass

    def log(self, url):
        logging.info("Short URL: {}".format(url))


class Off(UrlShortener):
    def shorten(self, url: str):
        return url


class TinyURL(UrlShortener):
    def shorten(self, url: str) -> str:
        response = request.urlopen("http://tinyurl.com/api-create.php?url={}".format(url))
        url = str(response.read(), encoding="ascii")
        self.log(url)
        return url


def get_url_shortener(name: str) -> UrlShortener:
    if name == "tinyurl":
        return TinyURL()
    return Off()
