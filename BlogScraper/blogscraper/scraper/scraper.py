#scraper/scraper.py
from strategies import BlogNameStrategy
from strategies import BaseStrategy


class Scraper:
    def __init__(self, strategy):
        self.strategy = strategy

    def scrape(self, url):
        return self.strategy.scrape(url)
