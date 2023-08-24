__all__ = ("Browser",)


from requests.models import Response
from requests.sessions import Session
from typing import Iterable

from vendor.AlbertUnruhUtils.utils.logger import get_logger

from .analytics import Page
from .constants import USER_AGENT, PROTOCOL, WEBSITE_NAME, WEBSITE_PATH, LAST_PAGE


logger = get_logger(__name__.split(".", 1)[1], add_handler=False)
logger.manager.getLogger("urllib3.connectionpool").setLevel("INFO")


def get(url: str) -> Response:
    logger.info(f"Requesting {url}")
    with Session() as session:
        response = session.request(method="GET", url=url, headers={"User-Agent": USER_AGENT})
    return response


class Browser:
    url: str = f"{PROTOCOL}://{WEBSITE_NAME}/{WEBSITE_PATH.lstrip('/')}"

    _cur_page: int = 1

    def get_page(self, page: int, /) -> Page:
        url = self.url.format(page)
        response = get(url)
        return Page(response.text)

    def get_next_page(self) -> Page:
        page = self.get_page(self._cur_page)
        self._cur_page += 1
        logger.debug(f"Page incremented to {self._cur_page}")
        return page

    def iter_pages(self) -> Iterable[Page]:
        page: Page
        while True:
            page = self.get_next_page()
            yield page
            if LAST_PAGE.search(page):
                logger.info(f"Last page reached")
                self.reset_cur_page()
                return

    def reset_cur_page(self) -> None:
        logger.debug(f"Resetting `_cur_page` from {self._cur_page} to {self.__class__._cur_page}")
        self._cur_page = self.__class__._cur_page
