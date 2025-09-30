__all__ = ("Name", "merge_names_into_list", "Article", "Page")


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
    _name: list[str]

    def __init__(self, object: str = ""):
        self._name = object.split()

        # valid name lengths: 2 and 3
        # e.g. "FORENAME SURNAME" or "FORENAME SECOND-NAME SURNAME"
        assert len(self._name) >= 2, f"Name {object!r} is to short!"
        assert len(self._name) <= 3, f"Name {object!r} is to long!"

    @property
    def name(self) -> str:
        # will only return forename and surname
        return f"{self._name[0]} {self._name[-1]}"

    @property
    def full_name(self) -> str:
        if len(self._name) == 2:
            return " ".join(self._name)
        return "{0} ({1}) {2}".format(*self._name)

    @property
    def has_second_name(self) -> bool:
        return len(self._name) == 3

    def __eq__(self, other) -> bool:
        # same type?
        if not isinstance(other, Name):
            return NotImplemented
        # do both have a second name?
        if other.has_second_name and self.has_second_name:
            return other.full_name == self.full_name
        # just compare forename and surname
        return other.name == self.name

    def __str__(self) -> str:
        return "{0.full_name} ({0.amount}x)".format(self)

    __repr__ = __str__


def merge_names_into_list(*_names: Name) -> list[Name]:
    # ``regex:/names?/gi`` is only used 23 times in this function...
    names: dict[str, Name] = {}
    for name in _names:
        if name.name not in names:
            names[name.name] = Name(name.name)
        names[name.name].amount += name.amount
    return list(names.values())


class Article(str):
    article: str

    def __init__(self, object: str = ""):
        self.article = object

    def get_content(self) -> Content:
        soup = bs4.BeautifulSoup(self.article, features="html.parser")
        body = soup.find(BODY_ATTRS[0], **BODY_ATTRS[1])
        sep: str = " | "  # to prevent colliding words and "|" to keep sentences logically separated
        content: Content = {
            "header": body.find(HEADER_ATTRS[0], **HEADER_ATTRS[1]).get_text(sep),
            "author": _.group(1) if (_ := AUTHOR_PATTERN.search(body.find(AUTHOR_ATTRS[0], **AUTHOR_ATTRS[1]).get_text(sep))) else "",
            "caption": _.get_text(sep) if (_ := body.find(CAPTION_ATTRS[0], **CAPTION_ATTRS[1])) else "",  # caption may not be present
            "teaser": body.find(TEASER_ATTRS[0], **TEASER_ATTRS[1]).get_text(sep),
            "text": body.find(TEXT_ATTRS[0], **TEXT_ATTRS[1]).get_text(sep),
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
