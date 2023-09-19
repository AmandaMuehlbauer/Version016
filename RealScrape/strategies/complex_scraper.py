from base_strategy import BaseScraperStrategy
from bs4 import BeautifulSoup

class ComplexScraper(BaseScraperStrategy):
    def extract_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the article title
        article_title = soup.find('h1', class_='article-title')
        if article_title:
            article_title = article_title.get_text()
        else:
            article_title = "No title found"
        
        # Find the author's name
        author_name = soup.find('div', class_='author-info')
        if author_name:
            author_name = author_name.find('span', class_='author-name')
            author_name = author_name.get_text() if author_name else "Unknown author"
        else:
            author_name = "Author info not found"
        
        # Extract the content of the blog post
        article_content = soup.find('div', class_='article-content')
        if article_content:
            paragraphs = article_content.find_all('p')
            content = '\n'.join(para.get_text() for para in paragraphs)
        else:
            content = "Content not found"
        
        return {
            "article_title": article_title,
            "author_name": author_name,
            "article_content": content
        }
