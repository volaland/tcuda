import json
import os

class DataSeparationPipeline:
    """Pipeline to separate basic and detailed missile data into different files"""
    
    def __init__(self):
        self.basic_data = []
        self.detailed_data = []
    
    def process_item(self, item, spider):
        if 'missile' in item:
            if item.get('is_detailed', False):
                # Create simplified detailed data entry
                simplified_item = {
                    'name': item.get('name', ''),
                    'detail_page_url': item.get('detail_page_url', ''),
                    'index_page_url': item.get('index_page_url', ''),
                    'page_number': item.get('page_number', 1),
                    'detailed_filename': item.get('detailed_filename', ''),
                    'scraped_at': item.get('scraped_at', '')
                }
                self.detailed_data.append(simplified_item)
            else:
                self.basic_data.append(dict(item))
        return item
    
    def close_spider(self, spider):
        """Write data to separate files when spider closes"""
        # Ensure all required directories exist
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/detailed', exist_ok=True)
        
        # Write basic data
        if self.basic_data:
            with open('data/missiles_basic.json', 'w', encoding='utf-8') as f:
                json.dump(self.basic_data, f, ensure_ascii=False, indent=2)
            spider.logger.info(f"Saved {len(self.basic_data)} basic missile records to missiles_basic.json")
        
        # Write detailed data
        if self.detailed_data:
            with open('data/missiles_detailed.json', 'w', encoding='utf-8') as f:
                json.dump(self.detailed_data, f, ensure_ascii=False, indent=2)
            spider.logger.info(f"Saved {len(self.detailed_data)} detailed missile records to missiles_detailed.json")