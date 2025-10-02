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

    return [
        x.text
        for x in soup.select(
            "#attr-input-type-keywords > tbody > tr > td:first-child code"
        )
    ]
