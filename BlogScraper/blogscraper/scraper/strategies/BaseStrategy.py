#scraper/strategies/BaseStrategy.py

from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def scrape(self, url):
        pass