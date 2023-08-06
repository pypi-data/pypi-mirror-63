from abc import ABC, abstractmethod
from urllib.request import urlopen


class Site(ABC):
    def __init__(self, url):
        self.url = url

    @property
    def events(self):
        html = urlopen(self.url).read()
        return self.parse_page(html)

    @abstractmethod
    def parse_page(self, html):
        raise NotImplementedError
