import csv
import re
import requests
from bs4 import BeautifulSoup

# specify the website URL to scrape
url = 'https://example.com/'

# send a GET request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# find all the email addresses on the page
email_addresses = set()
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith('mailto:'):
        email_addresses.add(href[7:])

# find all the phone numbers on the page
phone_numbers = set()
phone_pattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})')
for text in soup.find_all(text=phone_pattern):
    match = phone_pattern.search(text)
    phone_numbers.add('-'.join(match.groups()))

# find all the first and last names on the page
names = set()
name_pattern = re.compile(r'([A-Z][a-z]+)\s+([A-Z][a-z]+)')
for text in soup.find_all(text=name_pattern):
    match = name_pattern.search(text)
    names.add(match.groups())

# write the data to a CSV file
with open('contacts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['First Name', 'Last Name', 'Email Address', 'Phone Number'])
    for name, email, phone in zip(names, email_addresses, phone_numbers):
        writer.writerow([name[0], name[1], email, phone])
