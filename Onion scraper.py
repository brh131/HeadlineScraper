
import urllib.request
import html.parser
from webScraper import WebScraper

onionParser = WebScraper()
onionParser.excludeList = ["American Voices", "Video", "Infographic", "Editorial Cartoon"]
onionParser.excludePhrases = ["The Week In Pictures", "Your Horoscopes", "Our Dumb Decade", "Our Annual Year"]
onionParser.categoryClass = 'vxl3c2-0 eYptU'
onionParser.baseURL = "https://www.theonion.com/latest"
onionParser.nextLinkClass = "sc-1out364-0 hMndXN js_link"
onionParser.nextURLMode = "append"
onionParser.headlineTag = "h2"

onionParser.scrape(100,"test.txt")










