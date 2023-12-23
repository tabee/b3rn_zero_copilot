import os
import sqlite3
from content_scraper import WebContentScraper, WebContentScraperEAK


class DatabaseHandler:
    def __init__(self, db_path, timeout=1):
        self.db_path = db_path
        self.timeout = timeout
        self.create_table_if_not_exists()
        print("\n\n********** DatabaseHandler **********")
        print(f"path: {self.db_path}\n")
        
    def get_connection(self):
        """Herstellt eine Verbindung zur SQLite-Datenbank."""
        conn = sqlite3.connect(self.db_path)
        return conn

    def create_table_if_not_exists(self):
        '''Create table if not exists'''
        with self.get_connection() as conn:
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
                print("Table created successfully")
            except sqlite3.DatabaseError as e:
                print(f"Error creating table: {e}")

    def get_unique_languages(self):
        """Ruft einzigartige Sprachen aus der Datenbank ab."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT language FROM faq_data")
            # Extrahiert die Sprachen aus den Ergebniszeilen
            languages = [row[0] for row in cursor.fetchall()]
            return languages if languages else None
        finally:
            cursor.close()
            conn.close()

    def get_unique_categories(self, selected_languages=None):
        """Ruft einzigartige Kategorien für die gegebenen Sprachen ab."""

        if selected_languages is None:
            selected_languages = self.get_unique_languages()

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if selected_languages:
                placeholders = ','.join('?' * len(selected_languages))
                query = f"SELECT DISTINCT category FROM faq_data WHERE language IN ({placeholders})"
                cursor.execute(query, selected_languages)
            else:
                cursor.execute("SELECT DISTINCT category FROM faq_data")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_suggestions_questions(self, input_text, languages=None, categories=None):
        """Erhält Vorschläge basierend auf Eingabetext, Sprache und Kategoriefiltern."""

        if languages is None:
            languages = self.get_unique_languages()

        if categories is None:
            categories = self.get_unique_categories(selected_languages=languages)

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            conditions = ["question LIKE ?"]
            params = [f'%{input_text}%']

            if languages:
                conditions.append(f"language IN ({','.join('?'*len(languages))})")
                params.extend(languages)

            if categories:
                conditions.append(f"category IN ({','.join('?'*len(categories))})")
                params.extend(categories)

            query = f"SELECT question FROM faq_data WHERE {' AND '.join(conditions)}"
            cursor.execute(query, params)
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_answer(self, question):
        """Ruft die Antwort für die ausgewählte Frage aus der Datenbank ab."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT answer FROM faq_data WHERE question = ?", (question,))
            result = cursor.fetchone()
            return result[0] if result else "No answer found."
        finally:
            cursor.close()
            conn.close()

    def get_questions_answers_by_category(self, category):
        """Ruft alle Fragen und Antworten für eine spezifische Kategorie ab."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT question, answer FROM faq_data WHERE category = ?"
            cursor.execute(query, (category,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def check_if_url_exists(self, url):
        '''Check if url exists in database and returns lastmod_date if exists'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT updated_at FROM faq_data WHERE source = ?", (url,))
            return cursor.fetchone()

    def update(self, data):
        '''Update data in database'''
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE faq_data SET 
                    language = ?, category = ?, question = ?, answer = ?, updated_at = ?
                    WHERE source = ?
                """, (data[0], data[1], data[2], data[3], data[5], data[4]))
                # (language[0], category[1], question[2], answer[3], url[4], lastmod_date[5])
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f"Error update to database: {e}")           

    def insert(self, data):
        '''Insert data to database'''
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO faq_data (language, category, question, answer, source, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, data)
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f"Error insert to database: {e}")       

if __name__ == '__main__':
    DB_PATH__BSV_ADMIN_CH = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data')) + '/bsv_faq.db'
    database__bsv_admin_ch = DatabaseHandler(DB_PATH__BSV_ADMIN_CH)
    scraper__bsv_admin_ch = WebContentScraper(
        database=database__bsv_admin_ch,
        sitemap_url='https://faq.bsv.admin.ch/sitemap.xml',
        remove_patterns=['Antwort\n', 'Rispondi\n', 'Réponse\n', 'Answer\n', '\n']
    )
    #scraper__bsv_admin_ch.scrape_and_store()



    
    # faq = database__bsv_admin_ch.get_questions_answers_by_category("alters-und-hinterlassenenversicherung-ahv")
    # for q,a in faq[0:2]:
    #     print(f"Frage: {q}\nAntwort: {a}\n")

    # print("Wie erhalte ich eine AHV-Nummer für mein neugeborenes Kind?")
    print("********** get_answer **********")
    print(database__bsv_admin_ch.get_answer("Wie erhalte ich eine AHV-Nummer für mein neugeborenes Kind?"))
    
    #print(db.get_unique_categories(["de"]))


    res = database__bsv_admin_ch.get_suggestions_questions("Wie erhalte ich", ["de"], ["alters-und-hinterlassenenversicherung-ahv"])
    res = database__bsv_admin_ch.get_suggestions_questions("Wie erhalte ich")
    print(f"\nResult: {len(res)} rows")
    for r in res:
        print(r)

    #print(f"Check if url exists: {database__bsv_admin_ch.check_if_url_exists('https://faq.bsv.admin.ch/fr/assurance-vieillesse-et-survivants-avs/les-refugies-en-provenance-dukraine-doivent-ils-payer-des')}")
