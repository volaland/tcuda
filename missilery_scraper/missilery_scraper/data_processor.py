"""
Data processor for the Missilery scraper project.

This module handles the processing of raw HTML data collected by the scraper
and converts it into structured missile data for database storage.
"""

import sqlite3
import re
from bs4 import BeautifulSoup
from missilery_db.database import DatabaseManager
from .constants import (
    DEFAULT_DATABASE_PATH, H2_TAG, CHARACTERISTICS_DELIMITER,
    BASE_PATTERN, PURPOSE_PATTERN, WARHEAD_PATTERN, GUIDANCE_PATTERN,
    COUNTRY_PATTERN, RANGE_PATTERN, YEAR_PATTERN, TECHNICAL_PATTERNS
)


class DataProcessor:
    """Processes raw HTML data and creates structured missile data."""
    def __init__(self, db_path=DEFAULT_DATABASE_PATH):
        self.db = DatabaseManager(db_path)

    def process_stage2_data(self):
        """Process raw HTML data and create structured missile data"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        # Get all index pages
        cursor.execute('SELECT url, html_content FROM index_pages')
        index_pages = cursor.fetchall()

        for index_url, html_content in index_pages:
            print(f"Processing index page: {index_url}")
            self.process_index_page(index_url, html_content)

        conn.close()

    def process_index_page(self, index_url, html_content):
        """Process a single index page"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find missile cards
        missile_cards = soup.find_all(['div', 'article'], class_=re.compile(r'missile|card'))

        for card in missile_cards:
            missile_data = self.extract_missile_from_card(card, index_url)
            if missile_data:
                # Save to database
                missile_id = self.db.save_missile(missile_data)

                # Get detail page data
                detail_url = self.get_detail_url_from_card(card)
                if detail_url:
                    detail_data = self.get_detail_page_data(detail_url)
                    if detail_data:
                        # Update missile with detailed information
                        self.update_missile_with_detail_data(missile_id, detail_data)

    def extract_missile_from_card(self, card, index_url):
        """Extract missile data from a card element"""
        missile_data = {
            'index_page_url': index_url,
            'detail_page_url': '',
            'description': ''
        }

        # Extract name
        name_elem = card.find(H2_TAG)
        if name_elem:
            name_link = name_elem.find('a')
            if name_link:
                missile_data['name'] = name_link.get_text(strip=True)
                missile_data['detail_page_url'] = name_link.get('href', '')
            else:
                missile_data['name'] = name_elem.get_text(strip=True)

        if not missile_data.get('name'):
            return None

        # Extract characteristics from text
        card_text = card.get_text()

        # Base (Баз.)
        base_match = re.search(BASE_PATTERN, card_text)
        if base_match:
            missile_data['base'] = base_match.group(1).strip()

        # Purpose (Наз.)
        purpose_match = re.search(PURPOSE_PATTERN, card_text)
        if purpose_match:
            missile_data['purpose'] = purpose_match.group(1).strip()

        # Warhead (Б/Ч.)
        warhead_match = re.search(WARHEAD_PATTERN, card_text)
        if warhead_match:
            missile_data['warhead'] = warhead_match.group(1).strip()

        # Guidance System (C/У.)
        guidance_match = re.search(GUIDANCE_PATTERN, card_text)
        if guidance_match:
            missile_data['guidance_system'] = guidance_match.group(1).strip()

        # Country (Стр.)
        country_match = re.search(COUNTRY_PATTERN, card_text)
        if country_match:
            missile_data['country'] = country_match.group(1).strip()

        # Range (км.)
        range_match = re.search(RANGE_PATTERN, card_text)
        if range_match:
            missile_data['range_km'] = int(range_match.group(1))

        # Year developed
        year_match = re.search(YEAR_PATTERN, card_text)
        if year_match:
            missile_data['year_developed'] = int(year_match.group(1))

        return missile_data

    def get_detail_url_from_card(self, card):
        """Get detail page URL from card"""
        name_elem = card.find(H2_TAG)
        if name_elem:
            name_link = name_elem.find('a')
            if name_link:
                return name_link.get('href', '')
        return None

    def get_detail_page_data(self, detail_url):
        """Get detail page data from database"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT html_content FROM detail_pages WHERE url = ?', (detail_url,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        return None

    def update_missile_with_detail_data(self, missile_id, detail_html):
        """Update missile with detailed information from detail page"""
        soup = BeautifulSoup(detail_html, 'html.parser')

        # Extract detailed description
        description_parts = []
        desc_selectors = [
            'div[class*="description"] p',
            'div[class*="content"] p',
            'article p',
            '.description p'
        ]

        for selector in desc_selectors:
            desc_elements = soup.select(selector)
            if desc_elements:
                description_parts.extend([elem.get_text(strip=True) for elem in desc_elements])
                break

        description = ' '.join(description_parts)

        # Extract technical characteristics
        tech_chars = self.extract_technical_characteristics(soup)

        # Update database
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE missiles SET description = ? WHERE id = ?
        ''', (description, missile_id))

        # Save technical characteristics
        for char_name, char_value in tech_chars.items():
            cursor.execute('''
                INSERT INTO technical_characteristics (missile_id, characteristic_name, characteristic_value)
                VALUES (?, ?, ?)
            ''', (missile_id, char_name, char_value))

        conn.commit()
        conn.close()

    def extract_technical_characteristics(self, soup):
        """Extract technical characteristics from detail page"""
        characteristics = {}

        # Look for characteristics section
        char_section = soup.find(text=re.compile(r'Характеристики', re.IGNORECASE))
        if char_section:
            char_parent = char_section.parent
            # Look for characteristics in the following elements
            for elem in char_parent.find_next_siblings():
                text = elem.get_text(strip=True)
                if CHARACTERISTICS_DELIMITER in text:
                    key, value = text.split(CHARACTERISTICS_DELIMITER, 1)
                    characteristics[key.strip()] = value.strip()

        # Look for common characteristic patterns
        char_patterns = TECHNICAL_PATTERNS

        page_text = soup.get_text()

        for pattern, key in char_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                characteristics[key] = match.group(1).strip()

        return characteristics

if __name__ == "__main__":
    processor = DataProcessor()
    print("Starting Stage 2 data processing...")
    processor.process_stage2_data()
    print("Stage 2 processing completed!")
