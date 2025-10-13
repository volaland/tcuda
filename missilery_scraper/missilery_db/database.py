import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="missilery_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Stage 1: Raw data tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_pages (
                url TEXT PRIMARY KEY,
                page_number INTEGER,
                html_content TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detail_pages (
                url TEXT PRIMARY KEY,
                missile_name TEXT,
                html_content TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Stage 2: Structured data tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                purpose TEXT,
                base TEXT,
                warhead TEXT,
                guidance_system TEXT,
                country TEXT,
                range_km INTEGER,
                year_developed INTEGER,
                description TEXT,
                index_page_url TEXT,
                detail_page_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (index_page_url) REFERENCES index_pages(url),
                FOREIGN KEY (detail_page_url) REFERENCES detail_pages(url)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_characteristics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                missile_id INTEGER,
                characteristic_name TEXT,
                characteristic_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (missile_id) REFERENCES missiles(id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_index_page(self, url, page_number, html_content):
        """Save index page data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO index_pages (url, page_number, html_content, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (url, page_number, html_content, datetime.now()))

        conn.commit()
        conn.close()

    def save_detail_page(self, url, missile_name, html_content):
        """Save detail page data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO detail_pages (url, missile_name, html_content, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (url, missile_name, html_content, datetime.now()))

        conn.commit()
        conn.close()

    def save_missile(self, missile_data):
        """Save structured missile data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO missiles (
                name, purpose, base, warhead, guidance_system, country,
                range_km, year_developed, description, index_page_url, detail_page_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            missile_data.get('name'),
            missile_data.get('purpose'),
            missile_data.get('base'),
            missile_data.get('warhead'),
            missile_data.get('guidance_system'),
            missile_data.get('country'),
            missile_data.get('range_km'),
            missile_data.get('year_developed'),
            missile_data.get('description'),
            missile_data.get('index_page_url'),
            missile_data.get('detail_page_url')
        ))

        missile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return missile_id

    def save_technical_characteristics(self, missile_id, characteristics):
        """Save technical characteristics for a missile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for char_name, char_value in characteristics.items():
            cursor.execute('''
                INSERT INTO technical_characteristics (missile_id, characteristic_name, characteristic_value)
                VALUES (?, ?, ?)
            ''', (missile_id, char_name, char_value))

        conn.commit()
        conn.close()

    def get_missiles_count(self):
        """Get total number of missiles in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM missiles')
        count = cursor.fetchone()[0]
        conn.close()
        return count
