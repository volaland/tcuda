# Missilery Database Schema Documentation

## Overview

This document describes the relational database schema for the Missilery missile data scraper. The database is designed to store comprehensive missile information in a normalized, relational structure using SQLite with SQLAlchemy ORM.

## Database Design Principles

- **Normalization**: Data is normalized to eliminate redundancy and ensure data integrity
- **Referential Integrity**: Foreign key constraints maintain data relationships
- **Indexing**: Strategic indexes for optimal query performance
- **Extensibility**: Schema designed to accommodate future data additions
- **Data Quality**: Constraints and validation ensure data consistency

## Entity Relationship Diagram

```
Countries (1) ←→ (N) Missiles (N) ←→ (1) Purposes
    ↑                    ↑                    ↑
    |                    |                    |
    |                    |                    |
BaseTypes (1) ←→ (N) Missiles (N) ←→ (1) WarheadTypes
    ↑                    ↑                    ↑
    |                    |                    |
    |                    |                    |
GuidanceSystems (1) ←→ (N) Missiles (N) ←→ (1) MissileDetailedData
    ↑                    ↑                    ↑
    |                    |                    |
    |                    |                    |
StructuredContent (N) ←→ (1) Missiles (N) ←→ (1) Characteristics
    ↑                    ↑                    ↑
    |                    |                    |
    |                    |                    |
StructuredContentLinks (N) ←→ (1) StructuredContent
    ↑                    ↑                    ↑
    |                    |                    |
    |                    |                    |
MissileImages (N) ←→ (1) Missiles
```

## Table Descriptions

### Core Reference Tables

#### Countries
Stores country information for missile manufacturers/operators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Country name |
| code | VARCHAR(3) | UNIQUE | ISO country code |

#### Purposes
Categorizes missiles by their intended purpose.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Purpose name |
| description | TEXT | | Purpose description |

#### BaseTypes
Defines launch platforms/base types for missiles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Base type name |
| description | TEXT | | Base type description |

#### WarheadTypes
Categorizes warhead types.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Warhead type name |
| description | TEXT | | Warhead type description |

#### GuidanceSystems
Defines guidance system types.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Guidance system name |
| description | TEXT | | Guidance system description |

### Main Data Tables

#### Missiles
Central table storing basic missile information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Missile name |
| detail_page_url | VARCHAR(500) | UNIQUE, NOT NULL | URL to detailed page |
| index_page_url | VARCHAR(500) | NOT NULL | URL to index page |
| page_number | INTEGER | NOT NULL | Page number where found |
| range_km | INTEGER | | Range in kilometers |
| year_developed | INTEGER | | Year of development |
| description | TEXT | | Basic description |
| country_id | INTEGER | FK → Countries.id | Country reference |
| purpose_id | INTEGER | FK → Purposes.id | Purpose reference |
| base_type_id | INTEGER | FK → BaseTypes.id | Base type reference |
| warhead_type_id | INTEGER | FK → WarheadTypes.id | Warhead type reference |
| guidance_system_id | INTEGER | FK → GuidanceSystems.id | Guidance system reference |
| scraped_at | DATETIME | | Scraping timestamp |
| is_detailed | BOOLEAN | DEFAULT FALSE | Has detailed data flag |

**Indexes:**
- `idx_missile_name` on `name`
- `idx_missile_country` on `country_id`
- `idx_missile_purpose` on `purpose_id`
- `idx_missile_range` on `range_km`
- `idx_missile_year` on `year_developed`

#### MissileDetailedData
Stores detailed technical specifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| missile_id | INTEGER | FK → Missiles.id, UNIQUE | Missile reference |
| detailed_filename | VARCHAR(200) | | Original JSON filename |
| range_detailed | VARCHAR(100) | | Detailed range info |
| speed | VARCHAR(100) | | Speed specifications |
| weight | VARCHAR(100) | | Weight specifications |
| length | VARCHAR(100) | | Length specifications |
| diameter | VARCHAR(100) | | Diameter specifications |
| wingspan | VARCHAR(100) | | Wingspan specifications |
| height | VARCHAR(100) | | Height specifications |
| accuracy | VARCHAR(100) | | Accuracy specifications |
| flight_time | VARCHAR(100) | | Flight time specifications |
| flight_altitude | VARCHAR(100) | | Flight altitude specifications |
| engine_type | VARCHAR(100) | | Engine type |
| thrust | VARCHAR(100) | | Thrust specifications |
| burn_time | VARCHAR(100) | | Burn time specifications |
| fuel_type | VARCHAR(100) | | Fuel type |
| guidance_system_detailed | VARCHAR(200) | | Detailed guidance info |
| warhead_detailed | VARCHAR(200) | | Detailed warhead info |
| fuse_type | VARCHAR(100) | | Fuse type |
| country_detailed | VARCHAR(100) | | Detailed country info |
| developer | VARCHAR(200) | | Developer organization |
| manufacturer | VARCHAR(200) | | Manufacturer |
| year_developed_detailed | VARCHAR(100) | | Detailed year info |
| adoption_year | VARCHAR(100) | | Year of adoption |
| status | VARCHAR(100) | | Current status |
| quantity | VARCHAR(100) | | Production quantity |
| other_characteristics | TEXT | | Other characteristics |
| scraped_at | DATETIME | | Scraping timestamp |

### Content Tables

#### StructuredContent
Stores structured content from detailed pages.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| missile_id | INTEGER | FK → Missiles.id | Missile reference |
| field_name | VARCHAR(100) | NOT NULL | Field name |
| field_label | VARCHAR(200) | | Field label |
| field_text | TEXT | | Field text content |

**Indexes:**
- `idx_structured_content_missile` on `missile_id`
- `idx_structured_content_field` on `field_name`

#### StructuredContentLink
Stores links within structured content.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| structured_content_id | INTEGER | FK → StructuredContent.id | Content reference |
| link_url | VARCHAR(500) | NOT NULL | Link URL |
| link_text | VARCHAR(200) | | Link text |

#### Characteristics
Stores characteristics table data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| missile_id | INTEGER | FK → Missiles.id | Missile reference |
| field_name | VARCHAR(200) | NOT NULL | Characteristic name |
| field_value | TEXT | NOT NULL | Characteristic value |

**Indexes:**
- `idx_characteristics_missile` on `missile_id`
- `idx_characteristics_field` on `field_name`

#### MissileImages
Stores image information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| missile_id | INTEGER | FK → Missiles.id | Missile reference |
| image_url | VARCHAR(500) | NOT NULL | Image URL |
| image_type | VARCHAR(50) | | Image type (main, gallery, diagram) |
| alt_text | VARCHAR(200) | | Alt text for image |

**Indexes:**
- `idx_missile_images_missile` on `missile_id`
- `idx_missile_images_type` on `image_type`

### Metadata Tables

#### ScrapingSessions
Tracks scraping sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| session_name | VARCHAR(100) | NOT NULL | Session name |
| start_time | DATETIME | | Session start time |
| end_time | DATETIME | | Session end time |
| total_pages | INTEGER | | Total pages scraped |
| total_missiles | INTEGER | | Total missiles scraped |
| total_detailed | INTEGER | | Total detailed records |
| status | VARCHAR(50) | DEFAULT 'running' | Session status |
| notes | TEXT | | Session notes |

## Data Relationships

### One-to-Many Relationships
- Country → Missiles (1:N)
- Purpose → Missiles (1:N)
- BaseType → Missiles (1:N)
- WarheadType → Missiles (1:N)
- GuidanceSystem → Missiles (1:N)
- Missile → MissileDetailedData (1:1)
- Missile → StructuredContent (1:N)
- Missile → Characteristics (1:N)
- Missile → MissileImages (1:N)
- StructuredContent → StructuredContentLink (1:N)

### Foreign Key Constraints
All foreign key relationships are enforced with referential integrity constraints.

## Indexes and Performance

### Primary Indexes
- All primary keys are automatically indexed
- Foreign keys are indexed for join performance

### Custom Indexes
- `idx_missile_name`: Fast name searches
- `idx_missile_country`: Country-based filtering
- `idx_missile_purpose`: Purpose-based filtering
- `idx_missile_range`: Range-based queries
- `idx_missile_year`: Year-based filtering
- Content and characteristic indexes for efficient lookups

## Data Import Process

### Import Steps
1. **Reference Data**: Create countries, purposes, base types, warhead types, guidance systems
2. **Basic Missiles**: Import basic missile data with foreign key references
3. **Detailed Data**: Import detailed specifications and structured content
4. **Relationships**: Establish all foreign key relationships
5. **Validation**: Verify data integrity and completeness

### Data Quality Measures
- Unique constraints prevent duplicate entries
- Foreign key constraints maintain referential integrity
- Data type constraints ensure data consistency
- Indexes optimize query performance

## Usage Examples

### Basic Queries

```sql
-- Find all missiles by country
SELECT m.name, c.name as country
FROM missiles m
JOIN countries c ON m.country_id = c.id
WHERE c.name = 'Russia';

-- Find missiles by purpose
SELECT m.name, p.name as purpose
FROM missiles m
JOIN purposes p ON m.purpose_id = p.id
WHERE p.name LIKE '%Strategic%';

-- Find missiles with detailed data
SELECT m.name, md.range_detailed, md.speed
FROM missiles m
JOIN missile_detailed_data md ON m.id = md.missile_id
WHERE m.is_detailed = 1;
```

### Advanced Queries

```sql
-- Find missiles with specific characteristics
SELECT m.name, c.field_name, c.field_value
FROM missiles m
JOIN characteristics c ON m.id = c.missile_id
WHERE c.field_name = 'Range' AND c.field_value LIKE '%km%';

-- Find missiles with images
SELECT m.name, mi.image_url, mi.image_type
FROM missiles m
JOIN missile_images mi ON m.id = mi.missile_id
WHERE mi.image_type = 'main';

-- Count missiles by country and purpose
SELECT c.name as country, p.name as purpose, COUNT(*) as count
FROM missiles m
JOIN countries c ON m.country_id = c.id
JOIN purposes p ON m.purpose_id = p.id
GROUP BY c.name, p.name
ORDER BY count DESC;
```

## Maintenance and Updates

### Regular Maintenance
- Monitor database size and performance
- Update indexes as needed
- Clean up orphaned records
- Backup database regularly

### Schema Updates
- Use migrations for schema changes
- Test changes on development database
- Maintain backward compatibility when possible

## File Structure

```
missilery_scraper/
├── database_models.py      # SQLAlchemy models
├── import_json_to_db.py    # Import script
├── requirements_db.txt     # Database dependencies
├── DATABASE_SCHEMA.md      # This documentation
└── missilery.db           # SQLite database (created after import)
```

## Dependencies

- SQLAlchemy 2.0.30+
- SQLite3 (included with Python)
- Python 3.8+

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_db.txt
   ```

2. **Run Import**:
   ```bash
   ./import_to_database.sh
   ```

3. **Query Database**:
   ```python
   from database_models import DatabaseManager
   db = DatabaseManager()
   session = db.get_session()
   # Use session for queries
   ```

This schema provides a robust, scalable foundation for storing and querying missile data with full relational integrity and optimal performance.
