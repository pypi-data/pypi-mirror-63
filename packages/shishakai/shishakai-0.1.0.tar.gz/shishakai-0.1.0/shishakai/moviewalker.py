from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import Site


class MovieWalker(Site):
    def __init__(self):
        super().__init__("https://movie.walkerplus.com/shisyakai/")

    def parse_page(self, html):
        bs = BeautifulSoup(html, "html.parser")
        events = []
        for element in bs.find_all("div", class_="previewMovieInfo"):
            title = element.a.string
            url = urljoin(self.url, element.a["href"])
            table_values = element.table.find_all("td")
            events.append(
                {
                    "title": title,
                    "url": url,
                    "deadline": table_values[0].string,
                    "date_and_time": table_values[1].string,
                    "venue": table_values[2].string,
                }
            )
        return events
