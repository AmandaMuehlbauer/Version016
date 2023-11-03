#scraper/strategies/BlogNameStrategy.py
import requests
from bs4 import BeautifulSoup
from BaseStrategy import BaseStrategy

class BlogNameStrategy(BaseStrategy):
    def scrape(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            blog_name = self.extract_blog_name(soup)
            return blog_name
        else:
            return "Failed to fetch the page."

    def extract_blog_name(self, soup):
        # Implement logic to extract the blog name here
        # For this example, let's assume the blog name is in a <title> tag
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
        else:
            return "Blog name not found."
