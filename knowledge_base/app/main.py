''' gRPC server for the knowledge base service '''''
from concurrent import futures
import grpc
import os
import service_pb2
import service_pb2_grpc
from content_scraper import WebContentScraper, WebContentScraperEAK
from database import DatabaseHandler

data_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
db__bsv_admin_ch = DatabaseHandler(f'{data_path}/bsv_faq.db')

def init_databases(data_path):
    ''' run scrapers for the EAK & BSV-FAQ website in german, french and italian '''
    # BSV-FAQ
    database__bsv_admin_ch = DatabaseHandler(f'{data_path}/bsv_faq.db')
    scraper__bsv_admin_ch = WebContentScraper(
        database=database__bsv_admin_ch,
        sitemap_url='https://faq.bsv.admin.ch/sitemap.xml',
        remove_patterns=['Antwort\n', 'Rispondi\n', 'Réponse\n', 'Answer\n', '\n']
    )
    scraper__bsv_admin_ch.scrape_and_store()
    # EAK-Website
    database__eak_admin_ch = DatabaseHandler(f'{data_path}/eak_website.db')
    scraper_de = WebContentScraperEAK(
        database=database__eak_admin_ch,
        sitemap_url='https://www.eak.admin.ch/eak/de/home.sitemap.xml',
        remove_patterns=[            
            'Navigation', 
            'Einkaufskorb',
            'Seite drucken',
            'Zum Seitenanfang',])
    scraper_de.scrape_and_store()
    scraper_fr = WebContentScraperEAK(
        database=database__eak_admin_ch,
        sitemap_url='https://www.eak.admin.ch/eak/fr/home.sitemap.xml',
        remove_patterns=["Début de la page","Panier d'achat",'\n']
    )
    scraper_fr.scrape_and_store()
    scraper_it = WebContentScraperEAK(
        database=database__eak_admin_ch,
        sitemap_url='https://www.eak.admin.ch/eak/it/home.sitemap.xml',
        remove_patterns=["Navigazione","Inizio pagina", "Carrello acquistiCarrello acquisti", "\n"]
    )
    scraper_it.scrape_and_store()

# gRPC server
class DatabaseHandlerService(service_pb2_grpc.DatabaseHandlerServiceServicer):
    def GetSuggestions(self, request, context):
        # Hier die Logik zur Abfrage der Datenbank
        suggestions = db__bsv_admin_ch.get_suggestions_questions(
            request.topic, request.languages, request.categories)
        return service_pb2.GetSuggestionsResponse(suggestions=suggestions)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DatabaseHandlerServiceServicer_to_server(DatabaseHandlerService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    init_databases(data_path)
    serve()
