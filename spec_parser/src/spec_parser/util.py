from __future__ import annotations

import requests
from bs4 import BeautifulSoup


class _RequestCache:
    def __init__(self) -> None:
        self._cache: dict[str, BeautifulSoup] = {}

    def __call__(self, page: str) -> BeautifulSoup:
        page = page.removesuffix(".html")
        if page not in self._cache:
            html = requests.get(
                f"https://html.spec.whatwg.org/multipage/{page}.html"
            ).text
            self._cache[page] = BeautifulSoup(html, "html5lib")
        return self._cache[page]


request_cache = _RequestCache()


def get_input_type_keywords() -> list[str]:
    soup = request_cache("input")

    table = soup.find(id="attr-input-type-keywords")
    return [row.contents[0].find("code").string for row in table.find("tbody").children]  # type: ignore[union-attr]
