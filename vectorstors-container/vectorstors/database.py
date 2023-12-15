import os
import sqlite3

data_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH = data_path + '/bsv_faq.db'
print(f"Using data path: {DB_PATH}")

class DatabaseHandler:
    def __init__(self, db_path, timeout=1):
        self.db_path = db_path
        self.timeout = timeout
        self.create_table_if_not_exists()
        
    def get_connection(self):
        """Herstellt eine Verbindung zur SQLite-Datenbank."""
        conn = sqlite3.connect(self.db_path)
        return conn

    def create_table_if_not_exists(self):
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

    def get_suggestions_questions(self, input_text, languages="de", categories=None):
        """Erhält Vorschläge basierend auf Eingabetext, Sprache und Kategoriefiltern."""
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

    def check_if_url_exists(self, url):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT updated_at FROM faq_data WHERE source = ?", (url,))
            return cursor.fetchone()

    def update(self, data):
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE faq_data SET 
                    language = ?, category = ?, question = ?, answer = ?, created_at = ?, updated_at = ?
                    WHERE source = ?
                """, (data[0], data[1], data[2], data[3], data[5], data[6], data[4]))
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f"Error update to database: {e}")           

    def insert(self, data):
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
    db = DatabaseHandler(DB_PATH)
    res = db.get_suggestions_questions("Wie erhalte ich", ["de"], ["alters-und-hinterlassenenversicherung-ahv"])
    print(f"Result: {len(res)} rows")
    for r in res:
        print(r)

    print(f"Check if url exists: {db.check_if_url_exists('https://faq.bsv.admin.ch/fr/assurance-vieillesse-et-survivants-avs/les-refugies-en-provenance-dukraine-doivent-ils-payer-des')}")