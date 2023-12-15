import os
from content_scraper import WebContentScraper
from database import DatabaseHandler
# import DatabaseHandler, WebContentScraper

data_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH = data_path + '/bsv_faq.db'
print(f"Using data path: {DB_PATH}")


def ignite_faq__bsv_admin_ch():
    database = DatabaseHandler(f'{data_path}/bsv_faq.db')
    scraper = WebContentScraper(
        database=database,
        sitemap_url='https://faq.bsv.admin.ch/sitemap.xml',
        remove_patterns=['Antwort\n', 'Rispondi\n', 'Réponse\n', 'Answer\n', '\n\n\n \n']
    )
    scraper.scrape_and_store()





class WebContentScraperEAK(WebContentScraper):
    def __init__(self, database, sitemap_url, remove_patterns, timeout=1):
        super().__init__(database, sitemap_url, remove_patterns, timeout)

    def process_url(self, url, lastmod_date):
        return super().process_url(url, lastmod_date)
    
    def extract_category(self, url, position=4):
        return super().extract_category(url, position)
    


def ignite__eak_ch():
    database = DatabaseHandler(f'{data_path}/eak_faq.db')
    scraper = WebContentScraperEAK(
        database=database,
        sitemap_url='https://www.eak.admin.ch/eak/de/home.sitemap.xml',
        remove_patterns=['Onlineshop\n', '\n']
    )
    scraper.scrape_and_store()
   
if __name__ == '__main__':
    #ignite_faq__bsv_admin_ch()
    ignite__eak_ch()
