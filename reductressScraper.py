import urllib.request
import html.parser
from webScraper import WebScraper

reductressScraper = WebScraper()

reductressScraper.baseURL = 'https://reductress.com/news/page/1'
reductressScraper.nextURLMode = "exact"
reductressScraper.nextLinkClass = "next page-numbers"
reductressScraper.headlineTag = "h1"
reductressScraper.scrape(96, "reductress.txt")