import scrapy
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from ..items import MissileItem

class MissileSpider(scrapy.Spider):
    name = 'missile_spider'
    allowed_domains = ['missilery.info']
    start_urls = ['https://missilery.info/search']

    def __init__(self, *args, **kwargs):
        super(MissileSpider, self).__init__(*args, **kwargs)
        self.discovered_pages = set()
        self.processed_pages = set()
        self.max_page = 22  # Stop at page 22 as requested
        
        # Ensure all required directories exist from the start
        self.ensure_directories()
        
        # Russian to Latin transliteration mapping
        self.transliteration_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    def ensure_directories(self):
        """Ensure all required directories exist"""
        import os
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/detailed', exist_ok=True)
        self.logger.info("Ensured data directories exist: data/ and data/detailed/")

    def transliterate_russian(self, text):
        """Transliterate Russian text to Latin ASCII"""
        result = ""
        for char in text:
            if char in self.transliteration_map:
                result += self.transliteration_map[char]
            elif char.isalnum() or char in (' ', '-', '_'):
                result += char
        return result
    
    def get_url_prefix(self, url):
        """Extract prefix from missile URL like https://missilery.info/missile/<prefix>"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'missile':
            return path_parts[1]
        return 'missile'
    
    def parse(self, response):
        """Parse index pages and extract missile data"""
        self.logger.info(f"Parsing index page: {response.url}")
        page_number = response.meta.get('page_number', 1)
        current_url = response.url
        
        # Mark this page as processed
        self.processed_pages.add(current_url)
        
        # Discover pagination links and yield requests for more pages
        yield from self.discover_pagination_links(response)
        
        # Extract missile data from this page
        yield from self.extract_missile_data_from_index(response, page_number)
    
    def discover_pagination_links(self, response):
        """Discover pagination links and yield requests for more pages"""
        self.logger.info(f"Discovering pagination links from: {response.url}")
        
        # Look for pagination links
        pagination_links = response.css('a[href*="page="]::attr(href)').getall()
        self.logger.info(f"Found {len(pagination_links)} pagination links")
        
        for link in pagination_links:
            full_url = urljoin(response.url, link)
            
            # Extract page number from URL
            page_match = re.search(r'page=(\d+)', full_url)
            if page_match:
                page_num = int(page_match.group(1))
                
                # Only process pages up to max_page and not already processed
                if page_num <= self.max_page and full_url not in self.discovered_pages and full_url not in self.processed_pages:
                    self.discovered_pages.add(full_url)
                    self.logger.info(f"Yielding request for page {page_num}: {full_url}")
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse,
                        meta={'page_number': page_num},
                        dont_filter=True
                    )
    
    def extract_missile_data_from_index(self, response, page_number):
        """Extract structured missile data from index page"""
        self.logger.info(f"Extracting missile data from page {page_number}: {response.url}")
        
        # Look for missile entries on the page - each missile is in a card div
        all_cards = response.css('.card')
        
        # Filter for missile cards (those with h2 a)
        missile_cards = []
        for card in all_cards:
            name_tag = card.css('h2 a')
            if name_tag:
                missile_cards.append(card)
        
        self.logger.info(f"Found {len(missile_cards)} missile entries on page {page_number}")
        
        for card in missile_cards:
            # Extract missile name from h2 a tag
            name_tag = card.css('h2 a')
            if not name_tag:
                continue
            
            name = name_tag.css('::text').get()
            if not name:
                continue
            name = name.strip()
            
            # Get detail page URL
            detail_url = name_tag.attrib['href']
            if detail_url:
                detail_url = urljoin(response.url, detail_url)
            
            # Find the parent container (the card body)
            parent_div = card.css('div.card-body')
            
            characteristics = {}
            
            if parent_div:
                # Parse the HTML with BeautifulSoup
                soup = BeautifulSoup(parent_div[0].get(), 'html.parser')
                
                # Extract characteristics using BeautifulSoup
                # Base type - look for field-label "Баз." and get text from field-items
                base_label = soup.find('div', class_='field-label', string='Баз.')
                if base_label:
                    base_items = base_label.find_next_sibling('div', class_='field-items')
                    if base_items:
                        base_links = base_items.find_all('a')
                        base_values = [link.get_text(strip=True) for link in base_links]
                        characteristics['base'] = ', '.join(base_values)
                
                # Purpose - look for field-label "Наз." and get text from field-items
                purpose_label = soup.find('div', class_='field-label', string='Наз.')
                if purpose_label:
                    purpose_items = purpose_label.find_next_sibling('div', class_='field-items')
                    if purpose_items:
                        purpose_links = purpose_items.find_all('a')
                        purpose_values = [link.get_text(strip=True) for link in purpose_links]
                        characteristics['purpose'] = ', '.join(purpose_values)
                
                # Warhead - look for field-label "Б/Ч." and get text from field-items
                warhead_label = soup.find('div', class_='field-label', string='Б/Ч.')
                if warhead_label:
                    warhead_items = warhead_label.find_next_sibling('div', class_='field-items')
                    if warhead_items:
                        warhead_links = warhead_items.find_all('a')
                        warhead_values = [link.get_text(strip=True) for link in warhead_links]
                        characteristics['warhead'] = ', '.join(warhead_values)
                
                # Guidance system - look for field-label "C/У." and get text from field-items
                guidance_label = soup.find('div', class_='field-label', string='C/У.')
                if guidance_label:
                    guidance_items = guidance_label.find_next_sibling('div', class_='field-items')
                    if guidance_items:
                        guidance_links = guidance_items.find_all('a')
                        guidance_values = [link.get_text(strip=True) for link in guidance_links]
                        characteristics['guidance_system'] = ', '.join(guidance_values)
                
                # Country - look for field-label "Стр." and get text from field-items
                country_label = soup.find('div', class_='field-label', string='Стр.')
                if country_label:
                    country_items = country_label.find_next_sibling('div', class_='field-items')
                    if country_items:
                        country_links = country_items.find_all('a')
                        country_values = [link.get_text(strip=True) for link in country_links]
                        characteristics['country'] = ', '.join(country_values)
                
                # Extract range from card-footer
                card_footer = soup.find('div', class_='card-footer')
                if card_footer:
                    range_text = card_footer.get_text(strip=True)
                    range_match = re.search(r'(\d+)\s*км\.', range_text)
                    if range_match:
                        characteristics['range_km'] = int(range_match.group(1))
                
                # Extract year from card-footer
                if card_footer:
                    year_text = card_footer.get_text(strip=True)
                    year_match = re.search(r'(\d{4})\s*г\.', year_text)
                    if year_match:
                        characteristics['year_developed'] = int(year_match.group(1))
            
            # Create missile item
            missile_item = MissileItem()
            missile_item['missile'] = True
            missile_item['name'] = name
            missile_item['detail_page_url'] = detail_url
            missile_item['index_page_url'] = response.url
            missile_item['page_number'] = page_number
            missile_item['description'] = ""  # Description will be empty for basic item
            missile_item['technical_characteristics'] = {}  # Placeholder for now
            missile_item['is_detailed'] = False  # Mark as basic item
            
            # Add extracted characteristics
            missile_item.update(characteristics)
            
            self.logger.info(f"Extracted missile: {name}")
            yield missile_item
            
            # Schedule detail page request if we have a detail URL
            if detail_url:
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail_page,
                    meta={'missile_name': name, 'index_page_url': response.url, 'page_number': page_number}
                )
    
    def parse_detail_page(self, response):
        """Parse individual missile detail page and extract detailed information"""
        self.logger.info(f"Parsing detail page: {response.url}")
        
        missile_name = response.meta.get('missile_name', '')
        index_page_url = response.meta.get('index_page_url', '')
        page_number = response.meta.get('page_number', 1)
        
        # Extract detailed information from the page-content-inner div
        page_content = response.css('#page-content-inner')
        if not page_content:
            self.logger.warning(f"No page-content-inner found for {response.url}")
            return
        
        detailed_info = {
            'missile_name': missile_name,
            'detail_page_url': response.url,
            'index_page_url': index_page_url,
            'page_number': page_number,
            'scraped_at': '',
            'structured_content': {}
        }
        
        # Parse all field classes in the page content
        field_elements = page_content.css('[class*="field-"]')
        for field_element in field_elements:
            field_classes = field_element.attrib.get('class', '').split()
            
            # Find the main field class (e.g., field-missile-composition)
            main_field_class = None
            for cls in field_classes:
                if cls.startswith('field-') and cls != 'field':
                    main_field_class = cls
                    break
            
            if main_field_class:
                field_name = main_field_class.replace('field-', '').replace('-', '_')
                
                # Extract field label
                field_label = field_element.css('.field-label::text').get()
                if not field_label:
                    field_label = field_element.css('label::text').get()
                
                # Extract field items/content
                field_items = field_element.css('.field-items')
                if field_items:
                    # Extract text from field items
                    field_text = field_items.css('::text').getall()
                    field_text = ' '.join([text.strip() for text in field_text if text.strip()])
                    
                    # Extract links with both text and URLs
                    field_links = []
                    field_urls = []
                    for link in field_items.css('a'):
                        link_text = link.css('::text').get()
                        link_href = link.css('::attr(href)').get()
                        if link_href:
                            full_url = urljoin(response.url, link_href)
                            field_urls.append(full_url)
                            # Use URL as the link text if no text, otherwise use the text
                            if link_text and link_text.strip():
                                field_links.append(full_url)  # Store URL instead of text
                            else:
                                field_links.append(full_url)
                    
                    detailed_info['structured_content'][field_name] = {
                        'label': field_label.strip() if field_label else '',
                        'text': field_text,
                        'links': field_links,  # Now contains URLs
                        'urls': field_urls
                    }
                else:
                    # If no field-items, get direct text content
                    field_text = field_element.css('::text').getall()
                    field_text = ' '.join([text.strip() for text in field_text if text.strip()])
                    detailed_info['structured_content'][field_name] = {
                        'label': field_label.strip() if field_label else '',
                        'text': field_text,
                        'links': [],
                        'urls': []
                    }
        
        # Extract description from content-text
        description_elements = page_content.css('.content-text')
        if description_elements:
            description_text = description_elements.css('p::text').getall()
            if description_text:
                detailed_info['description'] = ' '.join([text.strip() for text in description_text if text.strip()])
        
        # Extract characteristics table if present
        characteristics_table = page_content.css('table')
        if characteristics_table:
            detailed_info['characteristics_table'] = []
            for table in characteristics_table:
                rows = table.css('tr')
                for row in rows:
                    cells = row.css('td')
                    if len(cells) >= 2:
                        field_name = cells[0].css('::text').get()
                        field_value = cells[1].css('::text').get()
                        if field_name and field_value:
                            detailed_info['characteristics_table'].append({
                                'field_name': field_name.strip(),
                                'field_value': field_value.strip()
                            })
        
        # Extract image URLs
        image_urls = page_content.css('img::attr(src)').getall()
        if image_urls:
            detailed_info['image_urls'] = [urljoin(response.url, img_url) for img_url in image_urls if img_url]
        
        # Extract gallery images
        gallery_images = page_content.css('.gallery-item a::attr(href)').getall()
        if gallery_images:
            detailed_info['gallery_images'] = [urljoin(response.url, img_url) for img_url in gallery_images if img_url]
        
        # Save individual missile data to separate file and get filename
        filename = self.save_individual_missile_data(detailed_info, missile_name)
        
        # Create detailed missile item for pipeline
        detailed_item = MissileItem()
        detailed_item['missile'] = True
        detailed_item['name'] = missile_name
        detailed_item['detail_page_url'] = response.url
        detailed_item['index_page_url'] = index_page_url
        detailed_item['page_number'] = page_number
        detailed_item['detailed_filename'] = filename
        detailed_item['scraped_at'] = detailed_info.get('scraped_at', '')
        detailed_item['is_detailed'] = True
        
        self.logger.info(f"Extracted detailed data for: {missile_name}")
        yield detailed_item
    
    def save_individual_missile_data(self, detailed_info, missile_name):
        """Save individual missile detailed data to separate JSON file"""
        import json
        import os
        from datetime import datetime
        
        # Create detailed data directory
        detailed_dir = 'data/detailed'
        os.makedirs(detailed_dir, exist_ok=True)
        
        # Get URL prefix from detail page URL
        detail_url = detailed_info.get('detail_page_url', '')
        url_prefix = self.get_url_prefix(detail_url)
        
        # Transliterate missile name and create short filename
        transliterated_name = self.transliterate_russian(missile_name)
        # Clean up the transliterated name
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', transliterated_name)
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        
        # Create filename: prefix_transliterated_name (max 64 chars total)
        base_filename = f"{url_prefix}_{clean_name}"
        if len(base_filename) > 60:  # Leave room for .json
            base_filename = base_filename[:60]
        
        filename = f"{base_filename}.json"
        
        # Add timestamp
        detailed_info['scraped_at'] = datetime.now().isoformat()
        
        # Save to individual file
        filepath = os.path.join(detailed_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(detailed_info, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Saved detailed data for {missile_name} to {filepath}")
        return filename