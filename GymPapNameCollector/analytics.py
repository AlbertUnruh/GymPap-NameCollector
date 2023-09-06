__all__ = ("Name", "Article", "Page")


import bs4
from typing import TypedDict

from vendor.AlbertUnruhUtils.utils.logger import get_logger

from .constants import (
    NOT_A_NAME,
    ARTICLE_URL,
    PROTOCOL,
    WEBSITE_NAME,
    BODY_ATTRS,
    HEADER_ATTRS,
    AUTHOR_ATTRS,
    AUTHOR_PATTERN,
    CAPTION_ATTRS,
    TEASER_ATTRS,
    TEXT_ATTRS,
    NAME_PATTERN,
    STR_TO_STRIP,
    STR_TO_REMOVE,
)


logger = get_logger(__name__.split(".", 1)[1], add_handler=False)


class Content(TypedDict):
    header: str
    author: str
    teaser: str
    text: str


class Name(str):
    amount: int = 0
    name: str

    def __init__(self, object: str = ""):
        self.name = object

    def __str__(self) -> str:
        return "{0.name} ({0.amount}x)".format(self)

    __repr__ = __str__


class Article(str):
    article: str

    def __init__(self, object: str = ""):
        self.article = object

    def get_content(self) -> Content:
        soup = bs4.BeautifulSoup(self.article, features="html.parser")
        body = soup.find(*BODY_ATTRS)
        sep: str = " | "  # to prevent colliding words and "|" to keep sentences logically separated
        content: Content = {
            "header": body.find(*HEADER_ATTRS).get_text(sep),
            "author": AUTHOR_PATTERN.search(body.find(*AUTHOR_ATTRS).get_text(sep)).group(1),
            "caption": _.get_text(sep) if (_ := body.find(*CAPTION_ATTRS)) else "",  # caption may not be present
            "teaser": body.find(*TEASER_ATTRS).get_text(sep),
            "text": body.find(*TEXT_ATTRS).get_text(sep),
        }
        for k, v in content.items():
            content[k] = v.strip()  # noqa
        return content

    def get_invalidated_content(self) -> Content:
        # Note: "~" is used to invalidate names
        content: Content = self.get_content()
        for k, v in content.items():
            content[k] = " ".join(  # noqa
                # this long line is definitely *not* a crime ^^
                (w if w.strip(STR_TO_STRIP) not in NOT_A_NAME else f"~{w.lstrip(STR_TO_REMOVE)}")
                for w in v.split()
            )
        return content

    def find_names(self) -> list[Name]:
        name: str
        names: dict[str, Name] = {}
        for s in self.get_invalidated_content().values():
            for res in NAME_PATTERN.finditer(s):
                name = res.group(0).strip(STR_TO_STRIP)
                if name not in names:
                    names[name] = Name(name)
                names[name].amount += 1
        return list(names.values())


class Page(str):
    page: str

    def __init__(self, object: str = ""):
        self.page = object

    def find_article_urls(self) -> set[str]:
        return set(map(lambda m: f"{PROTOCOL}://{WEBSITE_NAME}{m.group(1)}", ARTICLE_URL.finditer(self.page)))
