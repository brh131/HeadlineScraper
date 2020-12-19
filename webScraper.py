import urllib.request
import html.parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class WebScraper(html.parser.HTMLParser):
    def __init__(self):
        super(WebScraper, self).__init__()
        self.articleTagDepth = 0
        self.inHeadlineTag = False
        self.inHeadline = False
        self.inCategory = False
        self.exclude = False
        self.currentHeadline = ""
        self.nextURL = ""
        self.headlineList = []

        # Configuration fields.
        self.headlineTag = ""
        self.findHeadlineByClass = False
        self.headlineClass = ""

        self.baseURL = ""
        self.pageSuffix = ""
        self.nextURLMode = ""
        self.nextLinkClass = ""

        self.categoryExcludeList = []
        self.excludePhrases = []
        self.categoryClass = None

        self.outputFileMode = "w"
        self.resultLimit = 0

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.articleTagDepth += 1
            #print("Beginning of article tag")
        if tag == self.headlineTag:
            self.inHeadlineTag = True
        if ('class', self.categoryClass) in attrs:
            self.inCategory = True
        if ('class', self.headlineClass) in attrs and self.findHeadlineByClass:
            self.inHeadline = True

        # Find the next link and set the next URL to that.
        if ("class", self.nextLinkClass) in attrs and self.nextLinkClass != "":
            for attr in attrs:
                if attr[0] == "href":
                    self.nextURL = self.convertNextURL(attr[1])
    
    def handle_endtag(self, tag):
        if tag == "article" or self.inHeadline == True:
            if tag == "article":
                self.articleTagDepth -= 1
            if not self.exclude:
                self.headlineList.append(self.currentHeadline)
            self.exclude = False
        if tag == self.headlineTag:
            self.inHeadlineTag = False

        if self.inHeadline:
            self.inHeadline = False

    def handle_data(self, data):
        if self.articleTagDepth > 0 or self.findHeadlineByClass:
            if (self.inHeadlineTag and self.articleTagDepth > 0) or self.inHeadline:
                if data.strip() != "":
                    self.currentHeadline = data.replace('\n', ' ').replace(u'\xa0', u' ').strip()
                for start in self.excludePhrases:
                    if data.startswith(start):
                        self.exclude = True

            if self.inCategory:
                if data in self.categoryExcludeList:
                    self.exclude = True
                self.inCategory = False


    def scrape(self, depth, outputPath):
        if self.nextURLMode == "continuous":
            driver = webdriver.Firefox()
            driver.get(self.baseURL)
            #actions = ActionChains(driver)
            try:
                if(depth == 0):
                    depth = float("inf")
                i = 0
                while i < depth and (self.resultLimit == 0 or len(self.headlineList) < self.resultLimit):
                    print(self.nextURL)
                    source = driver.page_source
                    previousSource = source
                    exitDepth = i
                    while len(previousSource) == len(source):
                        # Wait until the button is clickable then click it. Repeat until the html gets longer.
                        element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.'+self.nextLinkClass))
                        )
                        element.click()
                        previousSource = source
                        source = driver.page_source
                    i += 1
            finally:
                source = driver.page_source
                self.feed(source)
                print("Exited at depth " + str(exitDepth))
                driver.quit()
            


        else:
            self.nextURL = self.baseURL
            if(depth == 0):
                depth = float("inf")
            i = 0
            while i < depth and (self.resultLimit == 0 or len(self.headlineList) < self.resultLimit):
                print(self.nextURL)
                req = urllib.request.Request(self.nextURL, headers={'User-Agent': "Mozilla/5.0"})
                response = urllib.request.urlopen(req)
                decode = response.read().decode("utf-8")
                self.feed(decode)
                if(self.nextURLMode=="page"):
                    self.nextURL = self.baseURL + self.pageSuffix + str(i+1)
                i += 1
        
        output = open(outputPath, self.outputFileMode, encoding="utf-8")
        for headline in self.headlineList:
            output.write(headline + "\n")
        output.close()
    
    def convertNextURL(self, link):
        if self.nextURLMode == "append":
            return self.baseURL + link
        elif self.nextURLMode == "exact":
            return link
        else:
            return None
