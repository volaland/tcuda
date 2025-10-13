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
from .database_models import (
    DatabaseManager, get_or_create, parse_comma_separated_values,
    Country, Purpose, BaseType, WarheadType, GuidanceSystem,
    Missile, MissileDetailedData, StructuredContent, StructuredContentLink,
    Characteristic, MissileImage, ScrapingSession
)
from .constants import (
    DEFAULT_DATABASE_URL, STATS_KEYS, IMPORT_STATISTICS_TITLE,
    SEPARATOR_LINE, BASIC_JSON_FILE, DETAILED_JSON_FILE, DETAILED_DIR,
    FILE_NOT_FOUND_MESSAGES, IMPORT_ERROR_MESSAGES, MAX_LINK_TEXT_LENGTH,
    DEFAULT_ENCODING
)

class JSONToDatabaseImporter:
    def __init__(self, database_url=DEFAULT_DATABASE_URL, update_mode=False):
        self.db_manager = DatabaseManager(database_url)
        self.session = self.db_manager.get_session()
        self.update_mode = update_mode
        self.stats = {key: 0 for key in STATS_KEYS.values()}
    
    def get_or_create_or_update(self, model_class, **kwargs):
        """Get existing record, create new one, or update existing based on update_mode"""
        # Find existing record by unique fields
        existing = None
        if hasattr(model_class, 'name'):
            existing = self.session.query(model_class).filter_by(name=kwargs.get('name')).first()
        elif hasattr(model_class, 'detail_page_url'):
            existing = self.session.query(model_class).filter_by(detail_page_url=kwargs.get('detail_page_url')).first()
        
        if existing:
            if self.update_mode:
                # Update existing record
                for key, value in kwargs.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                return existing, 'updated'
            else:
                # Return existing without updating
                return existing, 'existing'
        else:
            # Create new record
            new_record = model_class(**kwargs)
            self.session.add(new_record)
            self.session.flush()  # Get the ID
            return new_record, 'created'
    
    def clear_missile_data(self, detail_page_url):
        """Clear existing data for a missile (for update mode)"""
        if not self.update_mode:
            return
            
        # Find the missile
        missile = self.session.query(Missile).filter_by(detail_page_url=detail_page_url).first()
        if not missile:
            return
            
        # Delete related data
        self.session.query(MissileDetailedData).filter_by(missile_id=missile.id).delete()
        self.session.query(StructuredContent).filter_by(missile_id=missile.id).delete()
        self.session.query(Characteristic).filter_by(missile_id=missile.id).delete()
        self.session.query(MissileImage).filter_by(missile_id=missile.id).delete()
        
        # Update missile record
        missile.is_detailed = True
        missile.scraped_at = datetime.utcnow()
    
    def import_basic_missiles(self, basic_json_path):
        """Import basic missile data from missiles_basic.json"""
        print(f"Importing basic missiles from {basic_json_path}...")
        
        with open(basic_json_path, 'r', encoding=DEFAULT_ENCODING) as f:
            basic_data = json.load(f)
        
        for missile_data in basic_data:
            try:
                # Create or get related entities
                country = None
                if missile_data.get('country'):
                    country, action = self.get_or_create_or_update(
                        Country, 
                        name=missile_data['country']
                    )
                    if action == 'created':
                        self.stats['countries_created'] += 1
                    elif action == 'updated':
                        self.stats['countries_updated'] += 1
                
                purpose = None
                if missile_data.get('purpose'):
                    purpose, action = self.get_or_create_or_update(
                        Purpose,
                        name=missile_data['purpose']
                    )
                    if action == 'created':
                        self.stats['purposes_created'] += 1
                    elif action == 'updated':
                        self.stats['purposes_updated'] += 1
                
                base_type = None
                if missile_data.get('base'):
                    base_type, action = self.get_or_create_or_update(
                        BaseType,
                        name=missile_data['base']
                    )
                    if action == 'created':
                        self.stats['base_types_created'] += 1
                    elif action == 'updated':
                        self.stats['base_types_updated'] += 1
                
                warhead_type = None
                if missile_data.get('warhead'):
                    warhead_type, action = self.get_or_create_or_update(
                        WarheadType,
                        name=missile_data['warhead']
                    )
                    if action == 'created':
                        self.stats['warhead_types_created'] += 1
                    elif action == 'updated':
                        self.stats['warhead_types_updated'] += 1
                
                guidance_system = None
                if missile_data.get('guidance_system'):
                    guidance_system, action = self.get_or_create_or_update(
                        GuidanceSystem,
                        name=missile_data['guidance_system']
                    )
                    if action == 'created':
                        self.stats['guidance_systems_created'] += 1
                    elif action == 'updated':
                        self.stats['guidance_systems_updated'] += 1
                
                # Create or update missile
                missile, action = self.get_or_create_or_update(
                    Missile,
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
                
                if action == 'created':
                    self.stats['missiles_created'] += 1
                elif action == 'updated':
                    self.stats['missiles_updated'] += 1
                
            except Exception as e:
                print(f"Error importing basic missile {missile_data.get('name', 'Unknown')}: {e}")
                self.stats['errors'] += 1
                continue
        
        self.session.commit()
        print(f"Basic missiles import completed. Created: {self.stats['missiles_created']}")
    
    def import_detailed_missiles(self, detailed_json_path, detailed_dir, basic_json_path=None):
        """Import detailed missile data from missiles_detailed.json and individual files"""
        print(f"Importing detailed missiles from {detailed_json_path}...")
        
        with open(detailed_json_path, 'r', encoding=DEFAULT_ENCODING) as f:
            detailed_index = json.load(f)
        
        # Load basic data for additional metadata if available
        basic_data = {}
        if basic_json_path and os.path.exists(basic_json_path):
            with open(basic_json_path, 'r', encoding=DEFAULT_ENCODING) as f:
                basic_missiles = json.load(f)
                # Create a lookup by detail_page_url
                basic_data = {missile['detail_page_url']: missile for missile in basic_missiles}
        
        for detailed_entry in detailed_index:
            try:
                # Clear existing data if in update mode
                if self.update_mode:
                    self.clear_missile_data(detailed_entry['detail_page_url'])
                
                # Find the corresponding missile or create it
                missile = self.session.query(Missile).filter_by(
                    detail_page_url=detailed_entry['detail_page_url']
                ).first()
                
                if not missile:
                    # Create missile from detailed entry and basic data if available
                    basic_info = basic_data.get(detailed_entry['detail_page_url'], {})
                    
                    # Create or get related entities from basic data
                    country = None
                    if basic_info.get('country'):
                        country, action = self.get_or_create_or_update(
                            Country, 
                            name=basic_info['country']
                        )
                        if action == 'created':
                            self.stats['countries_created'] += 1
                        elif action == 'updated':
                            self.stats['countries_updated'] += 1
                    
                    purpose = None
                    if basic_info.get('purpose'):
                        purpose, action = self.get_or_create_or_update(
                            Purpose,
                            name=basic_info['purpose']
                        )
                        if action == 'created':
                            self.stats['purposes_created'] += 1
                        elif action == 'updated':
                            self.stats['purposes_updated'] += 1
                    
                    base_type = None
                    if basic_info.get('base'):
                        base_type, action = self.get_or_create_or_update(
                            BaseType,
                            name=basic_info['base']
                        )
                        if action == 'created':
                            self.stats['base_types_created'] += 1
                        elif action == 'updated':
                            self.stats['base_types_updated'] += 1
                    
                    warhead_type = None
                    if basic_info.get('warhead'):
                        warhead_type, action = self.get_or_create_or_update(
                            WarheadType,
                            name=basic_info['warhead']
                        )
                        if action == 'created':
                            self.stats['warhead_types_created'] += 1
                        elif action == 'updated':
                            self.stats['warhead_types_updated'] += 1
                    
                    guidance_system = None
                    if basic_info.get('guidance_system'):
                        guidance_system, action = self.get_or_create_or_update(
                            GuidanceSystem,
                            name=basic_info['guidance_system']
                        )
                        if action == 'created':
                            self.stats['guidance_systems_created'] += 1
                        elif action == 'updated':
                            self.stats['guidance_systems_updated'] += 1
                    
                    # Create missile
                    missile, action = self.get_or_create_or_update(
                        Missile,
                        name=detailed_entry['name'],
                        detail_page_url=detailed_entry['detail_page_url'],
                        index_page_url=detailed_entry['index_page_url'],
                        page_number=detailed_entry['page_number'],
                        range_km=basic_info.get('range_km'),
                        year_developed=basic_info.get('year_developed'),
                        description=basic_info.get('description', ''),
                        country_id=country.id if country else None,
                        purpose_id=purpose.id if purpose else None,
                        base_type_id=base_type.id if base_type else None,
                        warhead_type_id=warhead_type.id if warhead_type else None,
                        guidance_system_id=guidance_system.id if guidance_system else None,
                        is_detailed=True,  # All detailed entries are detailed
                        scraped_at=datetime.utcnow()
                    )
                    
                    if action == 'created':
                        self.stats['missiles_created'] += 1
                    elif action == 'updated':
                        self.stats['missiles_updated'] += 1
                
                # Load detailed data from individual file
                detailed_file_path = os.path.join(detailed_dir, detailed_entry['detailed_filename'])
                if not os.path.exists(detailed_file_path):
                    print(f"Warning: Detailed file not found: {detailed_file_path}")
                    continue
                
                with open(detailed_file_path, 'r', encoding=DEFAULT_ENCODING) as f:
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
                            link_text=field_data.get('text', '')[:MAX_LINK_TEXT_LENGTH]  # Truncate if too long
                        )
                        self.session.add(link_record)
                
            except Exception as e:
                print(IMPORT_ERROR_MESSAGES['STRUCTURED_CONTENT'].format(field_name=field_name, error=e))
                self.stats[STATS_KEYS['ERRORS']] += 1
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
                print(IMPORT_ERROR_MESSAGES['CHARACTERISTIC'].format(error=e))
                self.stats[STATS_KEYS['ERRORS']] += 1
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
                print(IMPORT_ERROR_MESSAGES['IMAGE'].format(image_url=image_url, error=e))
                self.stats[STATS_KEYS['ERRORS']] += 1
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
        print("\n" + SEPARATOR_LINE)
        print(IMPORT_STATISTICS_TITLE)
        print(SEPARATOR_LINE)
        print(f"Countries - Created: {self.stats['countries_created']}, Updated: {self.stats['countries_updated']}")
        print(f"Purposes - Created: {self.stats['purposes_created']}, Updated: {self.stats['purposes_updated']}")
        print(f"Base types - Created: {self.stats['base_types_created']}, Updated: {self.stats['base_types_updated']}")
        print(f"Warhead types - Created: {self.stats['warhead_types_created']}, Updated: {self.stats['warhead_types_updated']}")
        print(f"Guidance systems - Created: {self.stats['guidance_systems_created']}, Updated: {self.stats['guidance_systems_updated']}")
        print(f"Missiles - Created: {self.stats['missiles_created']}, Updated: {self.stats['missiles_updated']}")
        print(f"Detailed data - Created: {self.stats['detailed_data_created']}, Updated: {self.stats['detailed_data_updated']}")
        print(f"Structured content - Created: {self.stats['structured_content_created']}, Updated: {self.stats['structured_content_updated']}")
        print(f"Characteristics - Created: {self.stats['characteristics_created']}, Updated: {self.stats['characteristics_updated']}")
        print(f"Images - Created: {self.stats['images_created']}, Updated: {self.stats['images_updated']}")
        print(f"Errors: {self.stats['errors']}")
        print(SEPARATOR_LINE)
    
    def close(self):
        """Close database connection"""
        self.session.close()
        self.db_manager.close()

def main():
    """Main import function"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Import missile data to database')
    parser.add_argument('--update', action='store_true', 
                       help='Update existing records instead of creating new ones')
    parser.add_argument('--database', default='missilery.db',
                       help='Database file name (default: missilery.db)')
    args = parser.parse_args()
    
    # Check if data files exist
    data_dir = Path("data")
    basic_json = data_dir / BASIC_JSON_FILE
    detailed_json = data_dir / DETAILED_JSON_FILE
    detailed_dir = data_dir / DETAILED_DIR
    
    if not basic_json.exists():
        print(FILE_NOT_FOUND_MESSAGES['BASIC_JSON'].format(file=basic_json))
        sys.exit(1)
    
    if not detailed_json.exists():
        print(FILE_NOT_FOUND_MESSAGES['DETAILED_JSON'].format(file=detailed_json))
        sys.exit(1)
    
    if not detailed_dir.exists():
        print(FILE_NOT_FOUND_MESSAGES['DETAILED_DIR'].format(dir=detailed_dir))
        sys.exit(1)
    
    # Create database and import data
    mode_text = "updating" if args.update else "creating"
    print(f"{mode_text.title()} database schema...")
    
    importer = JSONToDatabaseImporter(
        database_url=f"sqlite:///{args.database}",
        update_mode=args.update
    )
    importer.db_manager.create_tables()
    
    print(f"Starting data import ({mode_text} mode)...")
    # Import all missiles from detailed data, using basic data for additional metadata
    importer.import_detailed_missiles(str(detailed_json), str(detailed_dir), str(basic_json))
    importer.create_scraping_session()
    
    importer.print_statistics()
    importer.close()
    
    print(f"\nImport completed successfully!")
    print(f"Database saved as: {args.database}")

if __name__ == "__main__":
    main()
