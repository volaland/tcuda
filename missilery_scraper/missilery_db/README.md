# Missilery Database Module

This module contains all database-related functionality for the Missilery scraper project. It provides a clean separation between web scraping and database operations.

## Module Structure

```
missilery_db/
├── __init__.py              # Module initialization and exports
├── __main__.py              # Command-line interface
├── database_models.py       # SQLAlchemy ORM models
├── database.py              # Database connection management
├── import_json_to_db.py     # JSON data import functionality
├── query_examples.py        # Example queries and analysis
├── corrected_final_summary.py # Comprehensive data summary
└── README.md               # This file
```

## Usage

### Command Line Interface

The module can be run directly from the command line:

```bash
# Import data to database
python -m missilery_db import --database missilery.db

# Update existing data
python -m missilery_db import --update --database missilery.db

# Run example queries
python -m missilery_db query

# Generate data summary
python -m missilery_db summary
```

### Programmatic Usage

```python
from missilery_db import DatabaseManager, Missile, Country

# Initialize database connection
db_manager = DatabaseManager("sqlite:///missilery.db")
session = db_manager.get_session()

# Query missiles
missiles = session.query(Missile).join(Country).filter(Country.name == "Россия").all()

# Close connection
session.close()
db_manager.close()
```

## Database Schema

The database uses a normalized relational schema with the following main entities:

- **Countries**: Missile-producing countries
- **Purposes**: Missile purposes (air defense, strategic, etc.)
- **BaseTypes**: Launch platforms (aircraft, ships, vehicles, etc.)
- **WarheadTypes**: Warhead types
- **GuidanceSystems**: Guidance systems
- **Missiles**: Main missile records
- **MissileDetailedData**: Detailed missile information
- **StructuredContent**: Structured content from detailed pages
- **Characteristics**: Technical characteristics
- **MissileImages**: Missile images
- **ScrapingSession**: Scraping session metadata

## Features

- **Data Import**: Import JSON data from scraped files
- **Update Mode**: Update existing records without creating duplicates
- **Data Integrity**: Comprehensive data validation and integrity checks
- **Query Examples**: Pre-built queries for common analysis tasks
- **Data Summary**: Detailed analysis of database contents and quality

## Dependencies

- SQLAlchemy 2.0+
- Python 3.8+

## Integration

This module is designed to work seamlessly with the main scraper:

1. Scraper collects data and saves to JSON files
2. Database module imports JSON data to SQLite database
3. Analysis tools query the database for insights

The separation allows for:
- Independent testing of database operations
- Easy maintenance and updates
- Clean code organization
- Reusable database functionality
