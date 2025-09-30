__all__ = (
    "PROTOCOL",
    "WEBSITE_NAME",
    "WEBSITE_PATH",
    "USER_AGENT",
    "LAST_PAGE",
    "ARTICLE_URL",
    "BODY_ATTRS",
    "HEADER_ATTRS",
    "AUTHOR_ATTRS",
    "CAPTION_ATTRS",
    "TEASER_ATTRS",
    "TEXT_ATTRS",
    "STR_TO_REMOVE",
    "STR_TO_STRIP",
    "AUTHOR_PATTERN",
    "NAME_PATTERN",
    "NOT_A_NAME_FILE",
    "NOT_A_NAME",
)


from pathlib import Path
import re


PROTOCOL: str = "https"
WEBSITE_NAME: str = "www.gymnasium-papenburg.de"
WEBSITE_PATH: str = "/aktuelles/{}/"

USER_AGENT: str = "{__name__}/{__version__} ({__url__})"
# populated with globals() in __init__.py
# Yes, I'm just committing a crime...

LAST_PAGE: re.Pattern[str] = re.compile(r'active">(?!.*"page-item").*?</ul>')
ARTICLE_URL: re.Pattern[str] = re.compile(r"href=\"(/artikel/[^/]+?)\"")

BODY_ATTRS: tuple[str, dict[str, str]] = ("div", {"id": "c1265"})
HEADER_ATTRS: tuple[str, dict[str, str]] = ("h1", {"itemprop": "headline"})
AUTHOR_ATTRS: tuple[str, dict[str, str]] = ("li", {"class": "news-meta-item"})
CAPTION_ATTRS: tuple[str, dict[str, str]] = ("figcaption", {"class": "image-caption"})
TEASER_ATTRS: tuple[str, dict[str, str]] = ("div", {"class": "lead", "itemprop": "description"})
TEXT_ATTRS: tuple[str, dict[str, str]] = ("div", {"class": "news-text-wrap", "itemprop": "articleBody"})

STR_TO_REMOVE: str = "\"„“”'’"
STR_TO_STRIP: str = f"-,<>():;.!? \n{STR_TO_REMOVE}"
AUTHOR_PATTERN: re.Pattern[str] = re.compile(r"\s*Von\s+([^|]+)\s+")
NAME_PATTERN: re.Pattern[str] = re.compile(fr"(?<!~)([A-Z][^{STR_TO_STRIP}]+ (?<!~)[A-Z]\S+)")

NOT_A_NAME_FILE: Path = Path(__file__).parent.joinpath(".not_a_name.txt")
NOT_A_NAME: frozenset[str] = frozenset(NOT_A_NAME_FILE.read_text("utf-8", "ignore").splitlines(False))
