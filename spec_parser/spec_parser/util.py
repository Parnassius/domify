from typing import Dict

import requests
from bs4 import BeautifulSoup  # type: ignore[import]


class _RequestCache:
    def __init__(self) -> None:
        self._cache: Dict[str, BeautifulSoup] = {}

    def __call__(self, page: str) -> BeautifulSoup:
        if page.endswith(".html"):
            page = page[:-5]
        if page not in self._cache:
            html = requests.get(
                f"https://html.spec.whatwg.org/multipage/{page}.html"
            ).text
            self._cache[page] = BeautifulSoup(html, "html5lib")
        return self._cache[page]


request_cache = _RequestCache()
