from GymPapNameCollector import analytics, worldwidewifi as www


browser = www.Browser()
for page in browser.iter_pages():
    for url in page.find_article_urls():
        article = analytics.Article(www.get(url).text)
        print(article.find_names())
        exit()
