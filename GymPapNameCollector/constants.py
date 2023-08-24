__all__ = (
    "PROTOCOL",
    "WEBSITE_NAME",
    "WEBSITE_PATH",
    "USER_AGENT",
    "LAST_PAGE",
    "ARTICLE_URL",
    "DIV_ID",
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

DIV_ID: str = "c1265"

BLACKLISTED_NAMES_FILE: Path = Path(__file__).parent.joinpath(".blacklisted_names.txt")
BLACKLISTED_NAMES: frozenset[str] = frozenset(BLACKLISTED_NAMES_FILE.read_text("utf-8", "ignore").splitlines(False))
