#!/usr/bin/env python3
"""
Import JSON data into SQLite database
Converts scraped missile data from JSON files to relational database
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from database_models import (
    DatabaseManager, get_or_create, parse_comma_separated_values,
    Country, Purpose, BaseType, WarheadType, GuidanceSystem,
    Missile, MissileDetailedData, StructuredContent, StructuredContentLink,
    Characteristic, MissileImage, ScrapingSession
)

class JSONToDatabaseImporter:
    def __init__(self, database_url="sqlite:///missilery.db"):
        self.db_manager = DatabaseManager(database_url)
        self.session = self.db_manager.get_session()
        self.stats = {
            'countries_created': 0,
            'purposes_created': 0,
            'base_types_created': 0,
            'warhead_types_created': 0,
            'guidance_systems_created': 0,
            'missiles_created': 0,
            'detailed_data_created': 0,
            'structured_content_created': 0,
            'characteristics_created': 0,
            'images_created': 0,
            'errors': 0
        }
    
    def import_basic_missiles(self, basic_json_path):
        """Import basic missile data from missiles_basic.json"""
        print(f"Importing basic missiles from {basic_json_path}...")
        
        with open(basic_json_path, 'r', encoding='utf-8') as f:
            basic_data = json.load(f)
        
        for missile_data in basic_data:
            try:
                # Create or get related entities
                country = None
                if missile_data.get('country'):
                    country = get_or_create(
                        self.session, Country, 
                        name=missile_data['country']
                    )
                    if country.id not in [c.id for c in self.session.query(Country).all()]:
                        self.stats['countries_created'] += 1
                
                purpose = None
                if missile_data.get('purpose'):
                    purpose = get_or_create(
                        self.session, Purpose,
                        name=missile_data['purpose']
                    )
                    if purpose.id not in [p.id for p in self.session.query(Purpose).all()]:
                        self.stats['purposes_created'] += 1
                
                base_type = None
                if missile_data.get('base'):
                    base_type = get_or_create(
                        self.session, BaseType,
                        name=missile_data['base']
                    )
                    if base_type.id not in [b.id for b in self.session.query(BaseType).all()]:
                        self.stats['base_types_created'] += 1
                
                warhead_type = None
                if missile_data.get('warhead'):
                    warhead_type = get_or_create(
                        self.session, WarheadType,
                        name=missile_data['warhead']
                    )
                    if warhead_type.id not in [w.id for w in self.session.query(WarheadType).all()]:
                        self.stats['warhead_types_created'] += 1
                
                guidance_system = None
                if missile_data.get('guidance_system'):
                    guidance_system = get_or_create(
                        self.session, GuidanceSystem,
                        name=missile_data['guidance_system']
                    )
                    if guidance_system.id not in [g.id for g in self.session.query(GuidanceSystem).all()]:
                        self.stats['guidance_systems_created'] += 1
                
                # Create missile
                missile = Missile(
                    name=missile_data['name'],
                    detail_page_url=missile_data['detail_page_url'],
                    index_page_url=missile_data['index_page_url'],
                    page_number=missile_data['page_number'],
                    range_km=missile_data.get('range_km'),
                    year_developed=missile_data.get('year_developed'),
                    description=missile_data.get('description', ''),
                    country_id=country.id if country else None,
                    purpose_id=purpose.id if purpose else None,
                    base_type_id=base_type.id if base_type else None,
                    warhead_type_id=warhead_type.id if warhead_type else None,
                    guidance_system_id=guidance_system.id if guidance_system else None,
                    is_detailed=missile_data.get('is_detailed', False),
                    scraped_at=datetime.utcnow()
                )
                
                self.session.add(missile)
                self.session.flush()  # Get the ID
                self.stats['missiles_created'] += 1
                
            except Exception as e:
                print(f"Error importing basic missile {missile_data.get('name', 'Unknown')}: {e}")
                self.stats['errors'] += 1
                continue
        
        self.session.commit()
        print(f"Basic missiles import completed. Created: {self.stats['missiles_created']}")
    
    def import_detailed_missiles(self, detailed_json_path, detailed_dir):
        """Import detailed missile data from missiles_detailed.json and individual files"""
        print(f"Importing detailed missiles from {detailed_json_path}...")
        
        with open(detailed_json_path, 'r', encoding='utf-8') as f:
            detailed_index = json.load(f)
        
        for detailed_entry in detailed_index:
            try:
                # Find the corresponding missile
                missile = self.session.query(Missile).filter_by(
                    detail_page_url=detailed_entry['detail_page_url']
                ).first()
                
                if not missile:
                    print(f"Warning: Missile not found for {detailed_entry['name']}")
                    continue
                
                # Load detailed data from individual file
                detailed_file_path = os.path.join(detailed_dir, detailed_entry['detailed_filename'])
                if not os.path.exists(detailed_file_path):
                    print(f"Warning: Detailed file not found: {detailed_file_path}")
                    continue
                
                with open(detailed_file_path, 'r', encoding='utf-8') as f:
                    detailed_data = json.load(f)
                
                # Create detailed data record
                detailed_record = MissileDetailedData(
                    missile_id=missile.id,
                    detailed_filename=detailed_entry['detailed_filename'],
                    scraped_at=datetime.fromisoformat(detailed_entry['scraped_at'].replace('Z', '+00:00'))
                )
                
                self.session.add(detailed_record)
                self.session.flush()
                self.stats['detailed_data_created'] += 1
                
                # Import structured content
                if 'structured_content' in detailed_data:
                    self.import_structured_content(missile.id, detailed_data['structured_content'])
                
                # Import characteristics table
                if 'characteristics_table' in detailed_data:
                    self.import_characteristics(missile.id, detailed_data['characteristics_table'])
                
                # Import images
                if 'image_urls' in detailed_data:
                    self.import_images(missile.id, detailed_data['image_urls'], 'main')
                
                if 'gallery_images' in detailed_data:
                    self.import_images(missile.id, detailed_data['gallery_images'], 'gallery')
                
            except Exception as e:
                print(f"Error importing detailed missile {detailed_entry.get('name', 'Unknown')}: {e}")
                self.stats['errors'] += 1
                continue
        
        self.session.commit()
        print(f"Detailed missiles import completed. Created: {self.stats['detailed_data_created']}")
    
    def import_structured_content(self, missile_id, structured_content):
        """Import structured content from detailed pages"""
        for field_name, field_data in structured_content.items():
            try:
                structured_record = StructuredContent(
                    missile_id=missile_id,
                    field_name=field_name,
                    field_label=field_data.get('label', ''),
                    field_text=field_data.get('text', '')
                )
                
                self.session.add(structured_record)
                self.session.flush()
                self.stats['structured_content_created'] += 1
                
                # Import links
                if 'links' in field_data and field_data['links']:
                    for link_url in field_data['links']:
                        link_record = StructuredContentLink(
                            structured_content_id=structured_record.id,
                            link_url=link_url,
                            link_text=field_data.get('text', '')[:200]  # Truncate if too long
                        )
                        self.session.add(link_record)
                
            except Exception as e:
                print(f"Error importing structured content {field_name}: {e}")
                self.stats['errors'] += 1
                continue
    
    def import_characteristics(self, missile_id, characteristics_table):
        """Import characteristics table data"""
        for char_data in characteristics_table:
            try:
                characteristic = Characteristic(
                    missile_id=missile_id,
                    field_name=char_data.get('field_name', ''),
                    field_value=char_data.get('field_value', '')
                )
                
                self.session.add(characteristic)
                self.stats['characteristics_created'] += 1
                
            except Exception as e:
                print(f"Error importing characteristic: {e}")
                self.stats['errors'] += 1
                continue
    
    def import_images(self, missile_id, image_urls, image_type):
        """Import missile images"""
        for image_url in image_urls:
            try:
                image_record = MissileImage(
                    missile_id=missile_id,
                    image_url=image_url,
                    image_type=image_type,
                    alt_text=''
                )
                
                self.session.add(image_record)
                self.stats['images_created'] += 1
                
            except Exception as e:
                print(f"Error importing image {image_url}: {e}")
                self.stats['errors'] += 1
                continue
    
    def create_scraping_session(self, session_name="Import Session"):
        """Create a scraping session record"""
        session_record = ScrapingSession(
            session_name=session_name,
            start_time=datetime.utcnow(),
            total_missiles=self.stats['missiles_created'],
            total_detailed=self.stats['detailed_data_created'],
            status='completed'
        )
        
        self.session.add(session_record)
        self.session.commit()
    
    def print_statistics(self):
        """Print import statistics"""
        print("\n" + "="*50)
        print("IMPORT STATISTICS")
        print("="*50)
        print(f"Countries created: {self.stats['countries_created']}")
        print(f"Purposes created: {self.stats['purposes_created']}")
        print(f"Base types created: {self.stats['base_types_created']}")
        print(f"Warhead types created: {self.stats['warhead_types_created']}")
        print(f"Guidance systems created: {self.stats['guidance_systems_created']}")
        print(f"Missiles created: {self.stats['missiles_created']}")
        print(f"Detailed data created: {self.stats['detailed_data_created']}")
        print(f"Structured content created: {self.stats['structured_content_created']}")
        print(f"Characteristics created: {self.stats['characteristics_created']}")
        print(f"Images created: {self.stats['images_created']}")
        print(f"Errors: {self.stats['errors']}")
        print("="*50)
    
    def close(self):
        """Close database connection"""
        self.session.close()
        self.db_manager.close()

def main():
    """Main import function"""
    # Check if data files exist
    data_dir = Path("data")
    basic_json = data_dir / "missiles_basic.json"
    detailed_json = data_dir / "missiles_detailed.json"
    detailed_dir = data_dir / "detailed"
    
    if not basic_json.exists():
        print(f"Error: {basic_json} not found!")
        sys.exit(1)
    
    if not detailed_json.exists():
        print(f"Error: {detailed_json} not found!")
        sys.exit(1)
    
    if not detailed_dir.exists():
        print(f"Error: {detailed_dir} not found!")
        sys.exit(1)
    
    # Create database and import data
    print("Creating database schema...")
    importer = JSONToDatabaseImporter()
    importer.db_manager.create_tables()
    
    print("Starting data import...")
    importer.import_basic_missiles(str(basic_json))
    importer.import_detailed_missiles(str(detailed_json), str(detailed_dir))
    importer.create_scraping_session()
    
    importer.print_statistics()
    importer.close()
    
    print("\nImport completed successfully!")
    print("Database saved as: missilery.db")

if __name__ == "__main__":
    main()
