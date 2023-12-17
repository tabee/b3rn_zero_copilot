''' content scraper module '''
import re
from datetime import datetime
import urllib.parse
import xml.etree.ElementTree as ET
from dateutil import parser
import requests
from bs4 import BeautifulSoup

class WebContentScraper:
    def __init__(self, database, sitemap_url, remove_patterns, timeout=1):
        self.database = database
        self.sitemap_url = sitemap_url
        self.remove_patterns = remove_patterns
        self.timeout = timeout

    def fetch_content(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None

    def parse_html(self, html_content):
        return BeautifulSoup(html_content, 'html.parser') if html_content else None

    def extract_language(self, soup):
        return soup.find('html').get('lang') if soup and soup.find('html') else None

    def extract_category(self, url, position=2):
        path_segments = urllib.parse.urlparse(url).path.strip('/').split('/')
        return path_segments[position - 1] if len(path_segments) >= position else None

    def clean_text(self, text):
        for pattern in self.remove_patterns:
            text = re.sub(pattern, '', text)
        return text

    def extract_text_by_tag(self, soup, tags):
        text_parts = [self.clean_text(element.get_text()) 
                      for tag in tags for element in soup.find_all(tag)]
        return '\n\n'.join(text_parts)
   
    def extract_text_by_id(self, soup, ids):
        text_parts = [self.clean_text(soup.find(id=identifier).get_text())
                    for identifier in ids if soup.find(id=identifier)]
        return '\n\n'.join(text_parts)

    def get_sitemap_item(self):
        xml_content = self.fetch_content(self.sitemap_url)
        if not xml_content:
            return []

        root = ET.fromstring(xml_content)
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls_with_dates = []
        for url in root:
            loc = url.find("sitemap:loc", namespace)
            lastmod_element_sitemap = url.find("sitemap:lastmod", namespace)

            if loc is not None and lastmod_element_sitemap is not None:
                loc_text = loc.text
                lastmod_text = lastmod_element_sitemap.text
                urls_with_dates.append((loc_text, lastmod_text))
            elif loc is not None:
                loc_text = loc.text
                urls_with_dates.append((loc_text, None))  # Fügen Sie 'None' für das Datum hinzu, wenn kein 'lastmod' vorhanden ist

        return urls_with_dates

    def process_url(self, url, lastmod_date):
        print(f"Processing URL: {url}")
        html_content = self.fetch_content(url)
        if not html_content:
            return

        soup = self.parse_html(html_content)
        language = self.extract_language(soup)
        category = self.extract_category(url)
        question = self.extract_text_by_tag(soup, ['h1'])
        answer = self.extract_text_by_tag(soup, ['article'])

        if question and language:
            return (language, category, question, answer, url, lastmod_date, lastmod_date)
        return None

    def should_update(self, url, lastmod_date_sitemap):
        existing_entry = self.database.check_if_url_exists(url)
        if not existing_entry:
            return True

        new_date = parser.parse(lastmod_date_sitemap) if isinstance(lastmod_date_sitemap, str) else lastmod_date_sitemap
        existing_date = existing_entry[0] if isinstance(existing_entry[0], datetime) else parser.parse(existing_entry[0])
        return new_date > existing_date

    def save_or_update_data(self, data):
        # Überprüfen, ob data[5] bereits ein datetime-Objekt ist
        lastmod_date = data[5] if isinstance(data[5], datetime) else parser.parse(data[5])

        if self.should_update(data[4], lastmod_date):

            if self.database.check_if_url_exists(data[4]):
                self.database.update(data)
            else:
                self.database.insert(data)

    def scrape_and_store(self):
        self.database.create_table_if_not_exists()
        urls_with_dates = self.get_sitemap_item()
        print(f"Found {len(urls_with_dates)} URLs in sitemap.")
        
        for url, lastmod_date in urls_with_dates:
            if self.should_update(url, lastmod_date):
                data = self.process_url(url, lastmod_date)
                if data:
                    self.save_or_update_data(data)


class WebContentScraperEAK(WebContentScraper):
    def __init__(self, database, sitemap_url, remove_patterns, timeout=1):
        super().__init__(database, sitemap_url, remove_patterns, timeout)
   
    def extract_category(self, url, position=4):
        return super().extract_category(url, position)
    
    def process_url(self, url, lastmod_date):
        print(f"Processing URL: {url}")
        html_content = self.fetch_content(url)
        if not html_content:
            return

        soup = self.parse_html(html_content)
        language = self.extract_language(soup)
        category = self.extract_category(url)
        question = self.extract_text_by_tag(soup, ['h1'])
        answer = self.extract_text_by_id(soup, ['content'])

        if question and language:
            return (language, category, question, answer, url, lastmod_date, lastmod_date)
        return None