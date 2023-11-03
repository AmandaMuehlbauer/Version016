#main.py
import argparse
from scraper.scraper import Scraper
from scraper.strategies.BlogNameStrategy import BlogNameStrategy
from config import BASE_DIR


def main():
    parser = argparse.ArgumentParser(description="Web Scraper")
    parser.add_argument("url", help="URL to scrape")

    args = parser.parse_args()
    url = args.url

    try:
        # Initialize the scraper with the BlogNameStrategy
        blog_name_scraper = Scraper(BlogNameStrategy())

        # Scrape the blog name using the strategy
        blog_name = blog_name_scraper.scrape(url)

        print("Blog Name: {}".format(blog_name))

    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()