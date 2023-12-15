import os
from content_scraper import WebContentScraper

data_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
print(f"Using data path: {data_path}")


def ignite_faq__bsv_admin_ch():
    scraper = WebContentScraper(
        db_path= f'{data_path}/bsv_faq.db',
        sitemap_url='https://faq.bsv.admin.ch/sitemap.xml',
        remove_patterns=['Antwort\n', 'Rispondi\n', 'Réponse\n', 'Answer\n']
    )
    scraper.scrape_and_store()

def ignite__eak_ch():
    scraper = WebContentScraper(
        db_path= f'{data_path}/eak_faq.db',
        sitemap_url='https://www.eak.admin.ch/eak/de/home.sitemap.xml',
        remove_patterns=['Onlineshop\n', '\n']
    )
    scraper.scrape_and_store()
   
if __name__ == '__main__':
    ignite_faq__bsv_admin_ch()
    #ignite__eak_ch()
