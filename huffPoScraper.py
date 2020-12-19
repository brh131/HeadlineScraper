import urllib.request
import html.parser
from webScraper import WebScraper
huffPoScraper = WebScraper()

huffPoScraper.baseURL = "https://www.huffpost.com/news/"
huffPoScraper.nextURLMode = "continuous"
huffPoScraper.nextLinkClass = "see-more__button"
huffPoScraper.findHeadlineByClass = True
huffPoScraper.headlineClass = "card__headline__text"
huffPoScraper.resultLimit = 300
huffPoScraper.scrape(0, "huffpo.txt")