#!/usr/bin/env python3
"""
Constants for the Missilery Scraper project
Contains all hardcoded values used throughout the application
"""

# =============================================================================
# SPIDER CONSTANTS
# =============================================================================

# Spider configuration
SPIDER_NAME = 'missile_spider'
ALLOWED_DOMAINS = ['missilery.info']
START_URLS = ['https://missilery.info/search']

# Pagination settings
MAX_PAGE_DISCOVERY_LIMIT = 50  # Reasonable fallback if pagination discovery fails
DEFAULT_PAGE_LIMIT = 22  # Expected number of pages

# =============================================================================
# SCRAPY SETTINGS
# =============================================================================

# Bot configuration
BOT_NAME = 'missilery_scraper'
SPIDER_MODULES = ['missilery_scraper.spiders']
NEWSPIDER_MODULE = 'missilery_scraper.spiders'

# Request settings
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_TIMEOUT = 30

# User agent
USER_AGENT = 'missilery_scraper (+http://www.yourdomain.com)'

# Retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Pipeline settings
ITEM_PIPELINES = {
    'missilery_scraper.pipelines.DataSeparationPipeline': 300,
}

# Logging
LOG_LEVEL = 'INFO'

# Cookies
COOKIES_ENABLED = True

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# =============================================================================
# DATA PROCESSING CONSTANTS
# =============================================================================

# Database settings
DEFAULT_DATABASE_PATH = 'missilery_data.db'
DEFAULT_DATABASE_URL = 'sqlite:///missilery.db'

# Data extraction patterns
BASE_PATTERN = r'Баз\.\s*([^\n\r]+)'
PURPOSE_PATTERN = r'Наз\.\s*([^\n\r]+)'
WARHEAD_PATTERN = r'Б/Ч\.\s*([^\n\r]+)'
GUIDANCE_PATTERN = r'C/У\.\s*([^\n\r]+)'
COUNTRY_PATTERN = r'Стр\.\s*([^\n\r]+)'
RANGE_PATTERN = r'(\d+)\s*км\.'
YEAR_PATTERN = r'(\d{4})\s*г\.'

# Technical characteristics patterns
TECHNICAL_PATTERNS = [
    (r'Длина[:\s]*([0-9.,\s]+)\s*м', 'length_m'),
    (r'Диаметр[:\s]*([0-9.,\s]+)\s*м', 'diameter_m'),
    (r'Масса[:\s]*([0-9.,\s]+)\s*кг', 'weight_kg'),
    (r'Скорость[:\s]*([0-9.,\s]+)\s*м/с', 'speed_ms'),
    (r'Высота[:\s]*([0-9.,\s]+)\s*м', 'altitude_m'),
    (r'Точность[:\s]*([0-9.,\s]+)\s*м', 'accuracy_m'),
]

# =============================================================================
# RUSSIAN TRANSLITERATION MAPPING
# =============================================================================

TRANSLITERATION_MAP = {
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

# =============================================================================
# DIRECTORY PATHS
# =============================================================================

# Data directories
DATA_DIR = 'data'
DETAILED_DIR = 'data/detailed'
BASIC_JSON_FILE = 'data/missiles_basic.json'
DETAILED_JSON_FILE = 'data/missiles_detailed.json'

# =============================================================================
# DATABASE CONSTANTS
# =============================================================================

# Table names
INDEX_PAGES_TABLE = 'index_pages'
DETAIL_PAGES_TABLE = 'detail_pages'
MISSILES_TABLE = 'missiles'
TECHNICAL_CHARACTERISTICS_TABLE = 'technical_characteristics'

# Query limits
DEFAULT_QUERY_LIMIT = 10
SAMPLE_DATA_LIMIT = 5
STATISTICS_LIMIT = 15

# =============================================================================
# RANGE CATEGORIES
# =============================================================================

RANGE_CATEGORIES = {
    'SHORT': 100,
    'MEDIUM': 1000,
    'LONG': 5000
}

# =============================================================================
# YEAR DECADES
# =============================================================================

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
# MESSAGES AND OUTPUT
# =============================================================================

# Stage messages
STAGE1_TITLE = "STAGE 1: Collecting raw HTML data from missilery.info"
STAGE2_TITLE = "STAGE 2: Processing structured data and creating database"
DATABASE_STATS_TITLE = "DATABASE STATISTICS"

# Success messages
STAGE1_SUCCESS = "Stage 1 completed successfully!"
STAGE2_SUCCESS = "Stage 2 completed successfully!"
STAGE2_PROCESSING_SUCCESS = "Stage 2 processing completed!"

# Error messages
STAGE1_ERROR = "Stage 1 failed with error:"
STAGE2_ERROR = "Stage 2 failed with error:"

# Separator lines
SEPARATOR_LINE = "=" * 60
DASH_LINE = "-" * 30

# =============================================================================
# COMMAND LINE ARGUMENTS
# =============================================================================

# Stage choices
STAGE_CHOICES = [1, 2]

# =============================================================================
# REGEX PATTERNS
# =============================================================================

# HTML element patterns
H2_TAG = 'h2'
A_TAG = 'a'
HREF_ATTR = 'href'

# CSS selectors
MISSILE_CARD_SELECTOR = ['div', 'article']
PAGINATION_SELECTOR = 'ul.pagination.justify-content-center.mb-4.mt-4'

# =============================================================================
# FILE EXTENSIONS
# =============================================================================

JSON_EXTENSION = '.json'
HTML_EXTENSION = '.html'

# =============================================================================
# CHARACTERISTICS DELIMITER
# =============================================================================

CHARACTERISTICS_DELIMITER = ':'
