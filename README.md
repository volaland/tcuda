# Missilery Data Scraper & Database

A comprehensive web scraping and database system for missile data from missilery.info, featuring PyTorch CUDA support, Scrapy web scraping, and SQLite database integration.

## 🚀 Quick Start

### 1. Setup Environment
```bash
./scripts/setup_env.sh
```

### 2. Run Scraper
```bash
# Quick test (3 items, 1 page)
./scripts/run_scraper.sh --test

# Full scraping (all 22 pages)
./scripts/run_scraper.sh --full

# Custom run (5 pages, 2s delay)
./scripts/run_scraper.sh --pages 5 --delay 2
```

### 3. Import to Database
```bash
./scripts/import_to_database.sh
```

## 📁 Project Structure

```
tcuda/
├── scripts/                          # Shell scripts
│   ├── setup_env.sh                 # Environment setup
│   ├── run_scraper.sh               # Scraper runner
│   └── import_to_database.sh        # Database import
├── missilery_scraper/               # Scrapy project
│   ├── data/                        # Scraped data
│   │   ├── missiles_basic.json     # Basic missile data
│   │   ├── missiles_detailed.json  # Detailed index
│   │   └── detailed/               # Individual files
│   ├── database_models.py          # SQLAlchemy models
│   ├── import_json_to_db.py        # Import script
│   ├── query_examples.py           # Query examples
│   └── missilery.db                # SQLite database
├── requirements.txt                 # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🛠️ Scripts Overview

### `./scripts/setup_env.sh`
Sets up Python 3.13 environment with PyTorch CUDA support.

**Features:**
- Creates virtual environment in `.venv/`
- Installs PyTorch with CUDA support
- Installs Jupyter ecosystem
- Installs Scrapy for web scraping
- Verifies installation

**Usage:**
```bash
./scripts/setup_env.sh [--help]
```

### `./scripts/run_scraper.sh`
Runs the Scrapy missile data scraper with various options.

**Features:**
- Test mode (3 items, 1 page)
- Full scraping (all 22 pages)
- Custom page count and delay
- Progress reporting
- Results summary

**Usage:**
```bash
./scripts/run_scraper.sh [OPTIONS]

Options:
  --test              Quick test run (3 items, 1 page) [default]
  --full              Full scraping run (all 22 pages)
  --pages N           Custom run with N pages
  --delay N           Set delay between requests to N seconds
  --help, -h          Show help message
```

**Examples:**
```bash
./scripts/run_scraper.sh --test                    # Quick test
./scripts/run_scraper.sh --full                    # Full scraping
./scripts/run_scraper.sh --pages 5 --delay 2       # 5 pages, 2s delay
```

### `./scripts/import_to_database.sh`
Imports scraped JSON data into a SQLite database.

**Features:**
- Comprehensive relational schema
- Data normalization
- Referential integrity
- Import statistics
- Error handling

**Usage:**
```bash
./scripts/import_to_database.sh [OPTIONS]

Options:
  --database NAME     Set database name (default: missilery.db)
  --help, -h          Show help message
```

## 📊 Database Schema

The database uses a normalized relational schema with 10 tables:

- **Reference Tables**: Countries, Purposes, BaseTypes, WarheadTypes, GuidanceSystems
- **Main Tables**: Missiles, MissileDetailedData
- **Content Tables**: StructuredContent, Characteristics, MissileImages
- **Metadata**: ScrapingSessions

**Key Features:**
- Foreign key constraints for data integrity
- Strategic indexes for performance
- Support for 13,000+ records
- 15MB SQLite database

## 🔧 Prerequisites

### System Requirements
- **Python 3.13** (required)
- **NVIDIA GPU** with CUDA support (optional, for PyTorch)
- **Linux/Unix** environment (tested on Ubuntu)

### Dependencies
- PyTorch 2.6.0+ with CUDA support
- Scrapy 2.13.0+ for web scraping
- SQLAlchemy 2.0.30+ for database
- BeautifulSoup4 4.13.0+ for HTML parsing
- Jupyter ecosystem for notebooks

## 📈 Data Statistics

### Scraped Data
- **448 missile records** with complete data
- **3,287 structured content entries**
- **7,215 technical characteristics**
- **1,544 images and media files**

### Geographic Distribution
- **Russia**: 192 missiles (42.9%)
- **USA**: 78 missiles (17.4%)
- **China**: 39 missiles (8.7%)
- **France**: 29 missiles (6.5%)
- **UK**: 19 missiles (4.2%)

### Purpose Categories
- **Air Defense**: 104 missiles (23.2%)
- **MLRS Systems**: 77 missiles (17.2%)
- **Strategic**: 51 missiles (11.4%)
- **Anti-Ship**: 37 missiles (8.3%)
- **Anti-Tank**: 35 missiles (7.8%)

## 🚨 Important Notes

### Script Execution
- **All scripts must be run from the project root directory**
- Scripts automatically detect correct directory and provide helpful error messages
- Virtual environment is automatically activated when needed

### Data Location
- Scraped data is stored in `missilery_scraper/data/`
- Database is created in `missilery_scraper/missilery.db`
- All paths are relative to project root

### Error Handling
- Scripts provide clear error messages
- Prerequisites are checked before execution
- Progress is reported throughout execution

## 🔍 Query Examples

### Basic Queries
```python
from missilery_scraper.database_models import DatabaseManager

# Initialize database
db = DatabaseManager("sqlite:///missilery_scraper/missilery.db")
session = db.get_session()

# Find missiles by country
missiles = session.query(Missile).join(Country).filter(Country.name == 'Russia').all()

# Find strategic missiles
strategic = session.query(Missile).join(Purpose).filter(Purpose.name.like('%Strategic%')).all()
```

### Run Example Queries
```bash
cd missilery_scraper
python query_examples.py
```

## 🐛 Troubleshooting

### Common Issues

**1. Script not found**
```bash
# Ensure you're in the project root directory
cd /path/to/tcuda
./scripts/setup_env.sh
```

**2. Virtual environment not found**
```bash
# Run setup script first
./scripts/setup_env.sh
```

**3. Scraped data not found**
```bash
# Run scraper first
./scripts/run_scraper.sh --test
```

**4. Database import fails**
```bash
# Ensure data exists and run from project root
ls missilery_scraper/data/
./scripts/import_to_database.sh
```

### Getting Help
- Use `--help` flag with any script
- Check error messages for specific guidance
- Ensure all prerequisites are met

## 📚 Documentation

- **Database Schema**: `missilery_scraper/DATABASE_SCHEMA.md`
- **Analysis Summary**: `missilery_scraper/DATABASE_ANALYSIS_SUMMARY.md`
- **Query Examples**: `missilery_scraper/query_examples.py`

## 🎯 Features

### Web Scraping
- ✅ Dynamic pagination discovery
- ✅ Comprehensive data extraction
- ✅ Image and media collection
- ✅ Structured content parsing
- ✅ Error handling and retry logic

### Database
- ✅ Normalized relational schema
- ✅ Referential integrity
- ✅ Performance optimization
- ✅ Data validation
- ✅ Import statistics

### Usability
- ✅ Single-command execution
- ✅ Progress reporting
- ✅ Error detection
- ✅ Help documentation
- ✅ Cross-platform compatibility

## 🚀 Performance

- **Scraping Speed**: ~114 items per minute
- **Database Size**: 15MB for 13,000+ records
- **Query Performance**: Sub-second response times
- **Memory Usage**: ~80MB peak during scraping

---

**Ready to start?** Run `./scripts/setup_env.sh` to begin! 🎯