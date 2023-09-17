from GymPapNameCollector import analytics, worldwidewifi as www


all_names: list[analytics.Name] = []

browser = www.Browser()
for page in browser.iter_pages():
    for url in page.find_article_urls():
        article = analytics.Article(www.get(url).text)
        all_names = analytics.merge_names_into_list(*all_names, *article.find_names())

_bn = "\n"  # just because "\n" aren't supported in f-strings in Python 3.11
print(
    f"""\
================================================================================
Names:
--------------------------------------------------------------------------------
{_bn.join(map(str, sorted(all_names, key=lambda n: (-n.amount, n.full_name))))}
================================================================================
Counts:
--------------------------------------------------------------------------------
{_bn.join(sorted({f"Names with {c:2} mention(s): {list(map(lambda n: n.amount, all_names)).count(c)}"
                  for c in map(lambda n: n.amount, all_names)}, reverse=True))}
"""
)
