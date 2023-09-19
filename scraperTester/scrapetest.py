import os
import json
import requests
from bs4 import BeautifulSoup

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file relative to the current script's directory
json_file_path = os.path.join(current_directory, "data", "urls.json")

# Read fake HTML file names from the JSON file
with open(json_file_path, 'r') as file:
    test_pages = json.load(file)

# Directory where your fake HTML files are stored
html_directory = os.path.join(current_directory, "data")
print(html_directory)

for filename in test_pages:
    # Construct the full path to the HTML file
    html_file_path = os.path.join(html_directory, filename)

    # Read the HTML content from the file
    with open(html_file_path, "r") as file:
        html_content = file.read()

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the title tag
    title_tag = soup.find("title")

    # Print the title
    if title_tag:
        print(f"Page Title for {filename}: {title_tag.text}")
    else:
        print(f"Title not found for {filename}.")








