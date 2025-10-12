#!/bin/bash

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
PROJECT_DIR="$PROJECT_ROOT/missilery_scraper"
DATABASE_NAME="missilery.db"

# --- Colors for output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Function to display help message ---
show_help() {
  echo -e "${BLUE}Missile Data Database Import Tool${NC}"
  echo ""
  echo "Usage: ./scripts/import_to_database.sh [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --database NAME     Set database name (default: missilery.db)"
  echo "  --help, -h          Show this help message"
  echo ""
  echo "This script imports scraped JSON data into a SQLite database"
  echo "with a comprehensive relational schema."
  echo ""
  echo "Prerequisites:"
  echo "  - Virtual environment must be activated"
  echo "  - Scraped data must exist in missilery_scraper/data/"
  echo "  - Script must be run from project root directory"
  echo ""
  echo "Output:"
  echo "  - SQLite database with normalized missile data"
  echo "  - Comprehensive statistics of imported data"
  echo ""
}

# --- Parse arguments ---
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --database)
            if [[ -n "$2" && "$2" != --* ]]; then
                DATABASE_NAME="$2"
                shift 2
            else
                echo -e "${RED}Error: --database requires a name.${NC}"
                exit 1
            fi
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# --- Change to project root directory ---
cd "$PROJECT_ROOT"

# --- Check if script is run from project root ---
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found. Please run this script from the project root directory.${NC}"
    echo -e "${YELLOW}Expected location: $(pwd)/requirements.txt${NC}"
    exit 1
fi

# --- Check prerequisites ---
echo -e "${BLUE}[INFO]${NC} Checking prerequisites..."

# Check if virtual environment exists
if [ ! -f "${VENV_PATH}/bin/activate" ]; then
    echo -e "${RED}Error: Virtual environment not found at ${VENV_PATH}. Please run ./scripts/setup_env.sh first.${NC}"
    exit 1
fi

# Check if data directory exists
if [ ! -d "${PROJECT_DIR}/data" ]; then
    echo -e "${RED}Error: Data directory not found at ${PROJECT_DIR}/data/. Please run the scraper first.${NC}"
    exit 1
fi

# Check if required JSON files exist
if [ ! -f "${PROJECT_DIR}/data/missiles_basic.json" ]; then
    echo -e "${RED}Error: missiles_basic.json not found. Please run the scraper first.${NC}"
    exit 1
fi

if [ ! -f "${PROJECT_DIR}/data/missiles_detailed.json" ]; then
    echo -e "${RED}Error: missiles_detailed.json not found. Please run the scraper first.${NC}"
    exit 1
fi

if [ ! -d "${PROJECT_DIR}/data/detailed" ]; then
    echo -e "${RED}Error: detailed/ directory not found. Please run the scraper first.${NC}"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} All prerequisites met!"

# --- Activate virtual environment ---
echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
source "${VENV_PATH}/bin/activate"

# --- Install database dependencies ---
echo -e "${BLUE}[INFO]${NC} Installing database dependencies..."
pip install -r "${PROJECT_DIR}/requirements_db.txt"

# --- Run database import ---
echo -e "${BLUE}[INFO]${NC} Starting database import..."
echo -e "${YELLOW}[INFO]${NC} Database will be created as: ${DATABASE_NAME}"
echo ""

# Change to the project directory
cd "${PROJECT_DIR}"

# Run the import script
python import_json_to_db.py

IMPORT_EXIT_CODE=$?

# Change back to the original directory
cd ..

if [ $IMPORT_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}[SUCCESS]${NC} Database import completed successfully!"
    
    # Check if database was created
    if [ -f "${PROJECT_DIR}/${DATABASE_NAME}" ]; then
        DB_SIZE=$(du -h "${PROJECT_DIR}/${DATABASE_NAME}" | cut -f1)
        echo -e "\n${BLUE}[INFO]${NC} Database created:"
        echo -e "  - File: ${PROJECT_DIR}/${DATABASE_NAME}"
        echo -e "  - Size: ${DB_SIZE}"
        
        # Show database statistics
        echo -e "\n${BLUE}[INFO]${NC} Database statistics:"
        python3 -c "
import sqlite3
import os
db_path = '${PROJECT_DIR}/${DATABASE_NAME}'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables = ['countries', 'purposes', 'base_types', 'warhead_types', 'guidance_systems', 
              'missiles', 'missile_detailed_data', 'structured_content', 'characteristics', 'missile_images']
    
    for table in tables:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f'  - {table}: {count} records')
        except:
            print(f'  - {table}: 0 records')
    
    conn.close()
else:
    print('  Database file not found')
"
        
        echo -e "\n${GREEN}[SUCCESS]${NC} Done!"
    else
        echo -e "\n${RED}[ERROR]${NC} Database file was not created!"
        exit 1
    fi
else
    echo -e "\n${RED}[ERROR]${NC} Database import failed with exit code ${IMPORT_EXIT_CODE}."
    echo -e "Please check the error messages above for details."
    exit 1
fi

deactivate
