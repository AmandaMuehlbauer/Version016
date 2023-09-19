from base_strategy import BaseScraperStrategy
import os
import json
from bs4 import BeautifulSoup

class SimpleScraper(BaseScraperStrategy):
    def extract_data(self, html):
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Example: Extract titles from <h1> and <h2> elements
        titles = []
        h1_elements = soup.find_all('h1')
        h2_elements = soup.find_all('h2')
        
        for h1 in h1_elements:
            titles.append(h1.get_text())
        
        for h2 in h2_elements:
            titles.append(h2.get_text())
        
        return titles