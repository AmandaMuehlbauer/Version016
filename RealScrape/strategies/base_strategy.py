from abc import ABC, abstractmethod

class BaseScraperStrategy(ABC):
    @abstractmethod
    def extract_data(self, html):
        pass
