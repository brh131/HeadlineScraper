import urllib.request
from selenium import webdriver
import html.parser
from webScraper import WebScraper
from selenium.webdriver.common.keys import Keys

class BuzzfeedScraper(WebScraper):
    def __init__(self):
        super(BuzzfeedScraper, self).__init__()
    
    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == "div" and ("class", "post-badge__svg badge__svg") in attrs:
            self.exclude = True
        

buzzfeedScraper = BuzzfeedScraper()
buzzfeedScraper.baseURL = "https://www.buzzfeed.com/"
buzzfeedScraper.categoryClass = "bold xs-inline-block xs-mt05 xs-text-6 link-gray-lighter"
buzzfeedScraper.categoryExcludeList = ["Nifty", "BuzzFeed Video", "As/Is", "Goodful", "Bring Me", "Pero Like"]
buzzfeedScraper.headlineTag = "h2"
buzzfeedScraper.scrape(10, "buzzfeed.txt")