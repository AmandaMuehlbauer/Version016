#test.py
import requests
from bs4 import BeautifulSoup
from config import BASE_DIR

#print(BASE_DIR)

def scrape_blog_names(urls):
    blog_names = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            site_title_tag = soup.find('p', class_='site-title').find('a')

            if site_title_tag:
                blog_name = site_title_tag.text
            else:
                blog_name = "Blog name not found"

            blog_names.append((url, blog_name))
        except requests.exceptions.RequestException:
            blog_names.append((url, "Failed to fetch the page"))

    return blog_names

if __name__ == "__main__":
    # List of URLs to scrape
    urls = ["https://thewoksoflife.com"]

    result = scrape_blog_names(urls)

    for url, blog_name in result:
        print(f"URL: {url}\nBlog Name: {blog_name}\n")
