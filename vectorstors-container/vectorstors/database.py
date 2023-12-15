import sqlite3
import os
from content_scraper import WebContentScraper

data_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH = data_path + '/bsv_faq.db'
print(f"Using data path: {DB_PATH}")


def get_db_connection():
    """Herstellt eine Verbindung zur SQLite-Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    return conn

""" def create_table_if_not_exists(self):
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
            print(f"Error creating table: {e}") """

def get_suggestions(input_text, languages, categories):
    """Erhält Vorschläge basierend auf Eingabetext, Sprache und Kategoriefiltern."""
    conn = get_db_connection()
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

if __name__ == '__main__':
    # Test
    print(get_suggestions("Krank", ["de"], ["alters-und-hinterlassenenversicherung-ahv"]))