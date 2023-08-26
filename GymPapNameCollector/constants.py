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
    "TEASER_ATTRS",
    "TEXT_ATTRS",
    "AUTHOR_PATTERN",
    "NAME_PATTERN",
    "BLACKLISTED_NAMES_FILE",
    "BLACKLISTED_NAMES",
)


from pathlib import Path
import re


PROTOCOL: str = "https"
WEBSITE_NAME: str = "www.gymnasium-papenburg.de"
WEBSITE_PATH: str = "/aktuelles/seite/{}/"

USER_AGENT: str = "{__name__}/{__version__} ({__url__})"
# populated with globals() in __init__.py
# Yes, I'm just committing a crime...

LAST_PAGE: re.Pattern[str] = re.compile(r"Aktuelles - Seite (\d+) von \1\D")
ARTICLE_URL: re.Pattern[str] = re.compile(r"href=\"(/artikel/[^/]+/)\"")

BODY_ATTRS: tuple[str, dict[str, str]] = ("div", {"id": "c1265"})
HEADER_ATTRS: tuple[str, dict[str, str]] = ("h1", {"class": "headline", "itemprop": "headline"})
AUTHOR_ATTRS: tuple[str, dict[str, str]] = ("div", {"class": "extra"})
TEASER_ATTRS: tuple[str, dict[str, str]] = ("div", {"class": "lead", "itemprop": "description"})
TEXT_ATTRS: tuple[str, dict[str, str]] = ("div", {"class": "news-text-wrap", "itemprop": "articleBody"})

AUTHOR_PATTERN: re.Pattern[str] = re.compile(r"\s*Von\s+([^|]+)\s+")
NAME_PATTERN: re.Pattern[str] = re.compile(r"")

BLACKLISTED_NAMES_FILE: Path = Path(__file__).parent.joinpath(".blacklisted_names.txt")
BLACKLISTED_NAMES: frozenset[str] = frozenset(BLACKLISTED_NAMES_FILE.read_text("utf-8", "ignore").splitlines(False))
