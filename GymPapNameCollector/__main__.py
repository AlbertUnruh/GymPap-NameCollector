import GymPapNameCollector


browser = GymPapNameCollector.worldwidewifi.Browser()
for page in browser.iter_pages():
    print(page.find_article_urls())
