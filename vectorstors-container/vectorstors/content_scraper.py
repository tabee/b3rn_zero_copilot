import re
import time
import sqlite3
import urllib.parse
import xml.etree.ElementTree as ET
from dateutil import parser
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class WebContentScraper:
    def __init__(self, db_path, sitemap_url, remove_patterns, timeout=1):
        self.db_path = db_path
        self.sitemap_url = sitemap_url
        self.remove_patterns = remove_patterns
        self.timeout = timeout
        print(f"Using database: {self.db_path}")

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

    def extract_text(self, soup, tags):
        text_parts = [self.clean_text(element.get_text()) 
                      for tag in tags for element in soup.find_all(tag)]
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
        question = self.extract_text(soup, ['h1'])
        answer = self.extract_text(soup, ['article'])

        if question and language:
            return (language, category, question, answer, url, lastmod_date, lastmod_date)
        return None

    def check_if_url_exists(self, url):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT updated_at FROM faq_data WHERE source = ?", (url,))
            return cursor.fetchone()

    def should_update(self, url, lastmod_date_sitemap):
        existing_entry = self.check_if_url_exists(url)
        if not existing_entry:
            return True

        # Überprüfen, ob lastmod_date ein String ist, bevor es geparst wird
        new_date = parser.parse(lastmod_date_sitemap) if isinstance(lastmod_date_sitemap, str) else lastmod_date_sitemap

        existing_date = existing_entry[0] if isinstance(existing_entry[0], datetime) else parser.parse(existing_entry[0])
        #print(f"Comparing dates: {new_date} > {existing_date} from {url} resultat ist {new_date > existing_date}")
        return new_date > existing_date

    def save_or_update_data(self, data):
        # Überprüfen, ob data[5] bereits ein datetime-Objekt ist
        lastmod_date = data[5] if isinstance(data[5], datetime) else parser.parse(data[5])

        if self.should_update(data[4], lastmod_date):
            with sqlite3.connect(self.db_path) as conn:
                try:
                    cursor = conn.cursor()
                    if self.check_if_url_exists(data[4]):
                        cursor.execute("""
                            UPDATE faq_data SET 
                            language = ?, category = ?, question = ?, answer = ?, created_at = ?, updated_at = ?
                            WHERE source = ?
                        """, (data[0], data[1], data[2], data[3], data[5], data[6], data[4]))
                    else:
                        cursor.execute("""
                            INSERT INTO faq_data (language, category, question, answer, source, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, data)
                    conn.commit()
                except sqlite3.DatabaseError as e:
                    print(f"Error saving to database: {e}")

    def create_table_if_not_exists(self):
        with sqlite3.connect(self.db_path) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS faq_data (
                        id INTEGER PRIMARY KEY,
                        language TEXT,
                        category TEXT,
                        question TEXT,
                        answer TEXT,
                        source TEXT,
                        created_at TEXT,
                        updated_at TEXT
                    )
                ''')
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f"Error creating table: {e}")

    def scrape_and_store(self):
        self.create_table_if_not_exists()
        urls_with_dates = self.get_sitemap_item()
        print(f"Found {len(urls_with_dates)} URLs in sitemap.")
        
        for url, lastmod_date in urls_with_dates:
            if self.should_update(url, lastmod_date):
                data = self.process_url(url, lastmod_date)
                if data:
                    self.save_or_update_data(data)

# def demo():
#     start_time = time.time()  # Startzeit erfassen

#     scraper = WebContentScraper(
#         db_path='/workspaces/b3rn_zero_copilot/vectorstors-container/vectorstors/data/bsv_faq.db',
#         sitemap_url='https://faq.bsv.admin.ch/sitemap.xml',
#         remove_patterns=['Antwort\n', 'Rispondi\n', 'Réponse\n','\n\n\n\n \n']
#     )
#     scraper.scrape_and_store()
#     print("Scraping and storing process completed.")
#     end_time = time.time()  # Endzeit erfassen
#     duration = end_time - start_time
#     print(f"Die Ausführungsdauer beträgt {duration} Sekunden.")

# if __name__ == '__main__':
#     demo()
