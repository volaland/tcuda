#!/usr/bin/env python3
"""
Constants for the Missilery Database package
Contains all hardcoded values used throughout the database operations
"""

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Default database settings
DEFAULT_DATABASE_URL = "sqlite:///missilery.db"
DEFAULT_DATABASE_PATH = "missilery.db"

# Database table names
COUNTRIES_TABLE = "countries"
PURPOSES_TABLE = "purposes"
BASE_TYPES_TABLE = "base_types"
WARHEAD_TYPES_TABLE = "warhead_types"
GUIDANCE_SYSTEMS_TABLE = "guidance_systems"
MISSILES_TABLE = "missiles"
MISSILE_DETAILED_DATA_TABLE = "missile_detailed_data"
STRUCTURED_CONTENT_TABLE = "structured_content"
CHARACTERISTICS_TABLE = "characteristics"
MISSILE_IMAGES_TABLE = "missile_images"
SCRAPING_SESSIONS_TABLE = "scraping_sessions"

# Legacy table names (for backward compatibility)
INDEX_PAGES_TABLE = "index_pages"
DETAIL_PAGES_TABLE = "detail_pages"
TECHNICAL_CHARACTERISTICS_TABLE = "technical_characteristics"

# =============================================================================
# QUERY LIMITS AND PAGINATION
# =============================================================================

# Query result limits
DEFAULT_QUERY_LIMIT = 10
SAMPLE_DATA_LIMIT = 5
STATISTICS_LIMIT = 15
MAX_QUERY_LIMIT = 100

# Range analysis thresholds
RANGE_CATEGORIES = {
    'SHORT': 100,
    'MEDIUM': 1000,
    'LONG': 5000
}

# Year decade thresholds
YEAR_DECADES = {
    'PRE_1950': 1950,
    '1950s': 1960,
    '1960s': 1970,
    '1970s': 1980,
    '1980s': 1990,
    '1990s': 2000,
    '2000s': 2010,
    '2010s_PLUS': 2010
}

# =============================================================================
# DISPLAY FORMATTING
# =============================================================================

# Separator lines
SEPARATOR_LINE = "=" * 60
DASH_LINE = "-" * 30
THICK_SEPARATOR = "=" * 80

# Query section separators
QUERY_SECTION_DASH = "-" * 25
QUERY_SECTION_DASH_LONG = "-" * 35
QUERY_SECTION_DASH_EXTRA_LONG = "-" * 40

# =============================================================================
# QUERY MESSAGES AND TITLES
# =============================================================================

# Main titles
QUERY_EXAMPLES_TITLE = "MISSILERY DATABASE QUERY EXAMPLES"
QUERY_COMPLETED_TITLE = "QUERY EXAMPLES COMPLETED"
IMPORT_STATISTICS_TITLE = "IMPORT STATISTICS"

# Query section titles
QUERY_SECTIONS = {
    'MISSILES_BY_COUNTRY': "1. MISSILES BY COUNTRY:",
    'MISSILES_BY_PURPOSE': "2. MISSILES BY PURPOSE:",
    'STRATEGIC_MISSILES': "3. STRATEGIC MISSILES WITH DETAILED DATA:",
    'MISSILES_WITH_IMAGES': "4. MISSILES WITH IMAGES:",
    'COMMON_CHARACTERISTICS': "5. MOST COMMON CHARACTERISTICS:",
    'RANGE_ANALYSIS': "6. RANGE ANALYSIS (km):",
    'DEVELOPMENT_TIMELINE': "7. DEVELOPMENT TIMELINE:",
    'COUNTRY_BASE_TYPE': "8. MISSILES BY COUNTRY AND BASE TYPE:",
    'DATABASE_STATISTICS': "9. DATABASE STATISTICS:",
    'SAMPLE_DETAILED_DATA': "10. SAMPLE DETAILED MISSILE DATA:"
}

# =============================================================================
# SQL QUERY PATTERNS
# =============================================================================

# Range category SQL patterns
RANGE_CATEGORY_SQL = """
    CASE 
        WHEN range_km < {short} THEN 'Short (<{short}km)'
        WHEN range_km < {medium} THEN 'Medium ({short}-{medium}km)'
        WHEN range_km < {long} THEN 'Long ({medium}-{long}km)'
        ELSE 'Very Long (>{long}km)'
    END as range_category
""".format(
    short=RANGE_CATEGORIES['SHORT'],
    medium=RANGE_CATEGORIES['MEDIUM'],
    long=RANGE_CATEGORIES['LONG']
)

# Year decade SQL patterns
YEAR_DECADE_SQL = """
    CASE 
        WHEN year_developed < 1950 THEN 'Pre-1950'
        WHEN year_developed < 1960 THEN '1950s'
        WHEN year_developed < 1970 THEN '1960s'
        WHEN year_developed < 1980 THEN '1970s'
        WHEN year_developed < 1990 THEN '1980s'
        WHEN year_developed < 2000 THEN '1990s'
        WHEN year_developed < 2010 THEN '2000s'
        ELSE '2010s+'
    END as decade
"""

# =============================================================================
# STATISTICS TRACKING
# =============================================================================

# Import statistics keys
STATS_KEYS = {
    'COUNTRIES_CREATED': 'countries_created',
    'COUNTRIES_UPDATED': 'countries_updated',
    'PURPOSES_CREATED': 'purposes_created',
    'PURPOSES_UPDATED': 'purposes_updated',
    'BASE_TYPES_CREATED': 'base_types_created',
    'BASE_TYPES_UPDATED': 'base_types_updated',
    'WARHEAD_TYPES_CREATED': 'warhead_types_created',
    'WARHEAD_TYPES_UPDATED': 'warhead_types_updated',
    'GUIDANCE_SYSTEMS_CREATED': 'guidance_systems_created',
    'GUIDANCE_SYSTEMS_UPDATED': 'guidance_systems_updated',
    'MISSILES_CREATED': 'missiles_created',
    'MISSILES_UPDATED': 'missiles_updated',
    'DETAILED_DATA_CREATED': 'detailed_data_created',
    'DETAILED_DATA_UPDATED': 'detailed_data_updated',
    'STRUCTURED_CONTENT_CREATED': 'structured_content_created',
    'STRUCTURED_CONTENT_UPDATED': 'structured_content_updated',
    'CHARACTERISTICS_CREATED': 'characteristics_created',
    'CHARACTERISTICS_UPDATED': 'characteristics_updated',
    'IMAGES_CREATED': 'images_created',
    'IMAGES_UPDATED': 'images_updated',
    'ERRORS': 'errors'
}

# =============================================================================
# FILE PATHS AND NAMES
# =============================================================================

# JSON file names
BASIC_JSON_FILE = "missiles_basic.json"
DETAILED_JSON_FILE = "missiles_detailed.json"
DETAILED_DIR = "detailed"

# File extensions
JSON_EXTENSION = ".json"
HTML_EXTENSION = ".html"

# =============================================================================
# DATA PROCESSING
# =============================================================================

# Text truncation limits
MAX_LINK_TEXT_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Encoding
DEFAULT_ENCODING = "utf-8"

# =============================================================================
# SQL QUERY CONDITIONS
# =============================================================================

# Common WHERE conditions
STRATEGIC_MISSILES_CONDITION = "p.name LIKE '%Strategic%' AND m.is_detailed = 1"
MISSILES_WITH_IMAGES_CONDITION = "mi.missile_id IS NOT NULL"
DETAILED_MISSILES_CONDITION = "m.is_detailed = 1"
MISSILES_WITH_CHARACTERISTICS_CONDITION = "md.speed IS NOT NULL OR md.weight IS NOT NULL"

# Group by conditions
MIN_MISSILE_COUNT_FOR_GROUPING = 2

# =============================================================================
# TABLE LISTS FOR STATISTICS
# =============================================================================

# All database tables
ALL_TABLES = [
    COUNTRIES_TABLE,
    PURPOSES_TABLE,
    BASE_TYPES_TABLE,
    WARHEAD_TYPES_TABLE,
    GUIDANCE_SYSTEMS_TABLE,
    MISSILES_TABLE,
    MISSILE_DETAILED_DATA_TABLE,
    STRUCTURED_CONTENT_TABLE,
    CHARACTERISTICS_TABLE,
    MISSILE_IMAGES_TABLE
]

# =============================================================================
# ERROR MESSAGES
# =============================================================================

# File not found messages
FILE_NOT_FOUND_MESSAGES = {
    'BASIC_JSON': "Error: {file} not found!",
    'DETAILED_JSON': "Error: {file} not found!",
    'DETAILED_DIR': "Error: {dir} not found!"
}

# Import error messages
IMPORT_ERROR_MESSAGES = {
    'STRUCTURED_CONTENT': "Error importing structured content {field_name}: {error}",
    'CHARACTERISTIC': "Error importing characteristic: {error}",
    'IMAGE': "Error importing image {image_url}: {error}"
}

# =============================================================================
# VERSION AND METADATA
# =============================================================================

# Package metadata
PACKAGE_VERSION = "1.0.0"
PACKAGE_AUTHOR = "Missilery Scraper Team"

# =============================================================================
# SQL QUERY TEMPLATES
# =============================================================================

# Common query templates
QUERY_TEMPLATES = {
    'MISSILES_BY_COUNTRY': """
        SELECT c.name as country, COUNT(m.id) as missile_count
        FROM {countries_table} c
        LEFT JOIN {missiles_table} m ON c.id = m.country_id
        GROUP BY c.name
        ORDER BY missile_count DESC
        LIMIT {limit}
    """,
    
    'MISSILES_BY_PURPOSE': """
        SELECT p.name as purpose, COUNT(m.id) as missile_count
        FROM {purposes_table} p
        LEFT JOIN {missiles_table} m ON p.id = m.purpose_id
        GROUP BY p.name
        ORDER BY missile_count DESC
        LIMIT {limit}
    """,
    
    'MISSILES_WITH_IMAGES': """
        SELECT m.name, COUNT(mi.id) as image_count
        FROM {missiles_table} m
        LEFT JOIN {missile_images_table} mi ON m.id = mi.missile_id
        WHERE {images_condition}
        GROUP BY m.id, m.name
        ORDER BY image_count DESC
        LIMIT {limit}
    """
}
