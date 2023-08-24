__all__ = ("Name", "Article", "Page")


from vendor.AlbertUnruhUtils.utils.logger import get_logger

from .constants import BLACKLISTED_NAMES, ARTICLE_URL, PROTOCOL, WEBSITE_NAME


logger = get_logger(__name__.split(".", 1)[1], add_handler=False)


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

    def find_names(self) -> list[Name]:
        name: str
        names: dict[str, Name] = {}
        for name in filter(lambda s: s.istitle(), self.article.split()):
            name = name.strip("-\"„'<>").removesuffix(".")
            if name in BLACKLISTED_NAMES:
                continue
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
