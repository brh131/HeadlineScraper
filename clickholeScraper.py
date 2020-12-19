import urllib.request
import html.parser
from webScraper import WebScraper

clickholeScraper = WebScraper()

clickholeScraper.baseURL = "https://clickhole.com/category/news/"
clickholeScraper.nextURLMode = "exact"
clickholeScraper.nextLinkClass = "next page-numbers"
clickholeScraper.headlineTag = "h2"
clickholeScraper.scrape(50, "test.txt")
