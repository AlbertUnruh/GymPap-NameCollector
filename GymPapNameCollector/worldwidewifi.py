__all__ = ("Browser",)


from requests.sessions import Session
from typing import Iterable

from vendor.AlbertUnruhUtils.utils.logger import get_logger

from .constants import USER_AGENT, PROTOCOL, WEBSITE_NAME, WEBSITE_PATH, LAST_PAGE


logger = get_logger(__name__, add_handler=False)
logger.manager.getLogger("urllib3.connectionpool").setLevel("INFO")


class Browser:
    header: dict[str, str] = {"User-Agent": USER_AGENT}
    url: str = f"{PROTOCOL}://{WEBSITE_NAME}/{WEBSITE_PATH.lstrip('/')}"

    _cur_page: int = 1

    def get_page(self, page: int, /) -> str:
        url = self.url.format(page)
        logger.info(f"Requesting {url}")
        with Session() as session:
            response = session.request(method="GET", url=url, headers=self.header)
        return response.text

    def get_next_page(self) -> str:
        page = self.get_page(self._cur_page)
        self._cur_page += 1
        logger.debug(f"Page incremented to {self._cur_page}")
        return page

    def iter_pages(self) -> Iterable[str]:
        page: str
        while True:
            page = self.get_next_page()
            yield page
            if LAST_PAGE.search(page):
                logger.info(f"Last page reached")
                return
