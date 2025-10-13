# Missilery Scraper

A comprehensive Scrapy project to scrape missile data from [missilery.info](https://missilery.info/search) and store it in a structured SQLite database.

## Project Overview

This project implements a two-stage data collection and processing system:

### Stage 1: Raw Data Collection
- Scrapes all index pages (pages 1-22) from missilery.info
- Collects raw HTML content from index and detail pages
- Stores raw data in `index_pages` and `detail_pages` tables

### Stage 2: Structured Data Processing
- Processes raw HTML data to extract structured information
- Creates normalized database schema for missile data
- Stores technical characteristics in separate tables

## Database Schema

### Raw Data Tables (Stage 1)
- **index_pages**: Raw HTML from index pages
- **detail_pages**: Raw HTML from missile detail pages

### Structured Data Tables (Stage 2)
- **missiles**: Main missile information
- **technical_characteristics**: Detailed technical specifications

## Installation

1. Ensure you have the main environment set up:
```bash
cd /home/vola/src/tcuda
source .venv/bin/activate
```

2. Install additional dependencies:
```bash
pip install beautifulsoup4
```

## Usage

### Run Stage 1 (Collect Raw Data)
```bash
cd missilery_scraper
python run_scraper.py --stage 1
```

### Run Stage 2 (Process Structured Data)
```bash
python run_scraper.py --stage 2
```

### Run Both Stages
```bash
python run_scraper.py --all
```

### Show Database Statistics
```bash
python run_scraper.py --stats
```

### Direct Scrapy Commands
```bash
# Stage 1
scrapy crawl missile_spider -s stage=1

# Stage 2
scrapy crawl missile_spider -s stage=2
```

## Data Structure

### Missile Information Extracted
- **Name**: Missile name
- **Purpose**: Intended use (air-to-air, surface-to-air, etc.)
- **Base**: Launch platform (aircraft, ground, ship, etc.)
- **Warhead**: Type of warhead
- **Guidance System**: Guidance method
- **Country**: Country of origin
- **Range**: Maximum range in kilometers
- **Year Developed**: Development year
- **Description**: Detailed description
- **Technical Characteristics**: Detailed specifications

### Technical Characteristics
- Length, diameter, weight
- Speed, altitude, accuracy
- Additional specifications from detail pages

## Project Structure

```
missilery_scraper/
├── missilery_scraper/
│   ├── spiders/
│   │   └── missile_spider.py      # Main spider
│   ├── items.py                   # Scrapy items
│   ├── pipelines.py               # Data processing pipeline
│   ├── settings.py                # Scrapy settings
│   ├── database.py                # Database management
│   ├── data_processor.py          # Stage 2 data processing
├── run_scraper.py                 # Main execution script
├── requirements.txt               # Additional dependencies
└── README.md                      # This file
```

## Configuration

### Scrapy Settings
- **DOWNLOAD_DELAY**: 1 second between requests
- **CONCURRENT_REQUESTS**: 16 concurrent requests
- **USER_AGENT**: Custom user agent
- **ROBOTSTXT_OBEY**: Disabled (False)

### Database
- **File**: `missilery_data.db` (SQLite)
- **Location**: Project root directory

## Data Sources

- **Index Pages**: https://missilery.info/search?page=1 to page=22
- **Detail Pages**: https://missilery.info/missile/* (individual missile pages)

## Features

- **Respectful Scraping**: 1-second delay between requests
- **Error Handling**: Retry failed requests
- **Data Validation**: Clean and validate extracted data
- **Structured Storage**: Normalized database schema
- **Progress Tracking**: Detailed logging and statistics
- **Two-Stage Processing**: Separate collection and processing phases

## Technical Details

### Languages Used
- **Python 3.13+**
- **Scrapy 2.13+**
- **BeautifulSoup4** for HTML parsing
- **SQLite3** for data storage

### Data Processing
- **Regex patterns** for characteristic extraction
- **CSS selectors** for HTML parsing
- **BeautifulSoup** for advanced HTML processing
- **SQLite** for relational data storage

## Output

The scraper creates a SQLite database (`missilery_data.db`) with:
- Complete missile catalog (400+ missiles)
- Technical specifications
- Structured data ready for analysis
- Raw HTML for reference

## Example Queries

```sql
-- Get all Russian missiles
SELECT name, purpose, range_km FROM missiles WHERE country = 'Россия';

-- Get missiles by range
SELECT name, country, range_km FROM missiles WHERE range_km > 1000 ORDER BY range_km DESC;

-- Get technical characteristics for a specific missile
SELECT characteristic_name, characteristic_value 
FROM technical_characteristics tc
JOIN missiles m ON tc.missile_id = m.id
WHERE m.name = 'AGM-65 Maverick';
```
