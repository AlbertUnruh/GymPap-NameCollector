from GymPapNameCollector import analytics, worldwidewifi as www


all_names: list[analytics.Name] = []

browser = www.Browser()
for page in browser.iter_pages():
    for url in page.find_article_urls():
        article = analytics.Article(www.get(url).text)
        all_names = analytics.merge_names_into_list(*all_names, *article.find_names())

    # still work in progress here...
    print(*sorted(all_names), sep="\n")
    all_names = []
