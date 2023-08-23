__all__ = ("PROTOCOL", "WEBSITE_NAME", "WEBSITE_PATH", "USER_AGENT", "LAST_PAGE")


import re


PROTOCOL: str = "https"
WEBSITE_NAME: str = "www.gymnasium-papenburg.de"
WEBSITE_PATH: str = "/aktuelles/seite/{}/"

USER_AGENT: str = "{__name__}/{__version__}"
# populated with globals() in __init__.py
# Yes, I'm just committing a crime...

LAST_PAGE: re.Pattern[str] = re.compile(r"Aktuelles - Seite (\d+) von \1\D")
