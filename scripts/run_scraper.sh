#!/bin/bash

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
SPIDER_NAME="missile_spider"
PROJECT_DIR="$PROJECT_ROOT/missilery_scraper"
LOG_LEVEL="INFO"

# --- Colors for output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Default settings ---
ROBOTSTXT_OBEY="False"
CLOSESPIDER_ITEMCOUNT=""
CLOSESPIDER_PAGECOUNT=""
DOWNLOAD_DELAY="1" # Default delay in seconds
MAX_PAGES_TO_SCRAPE="22" # Default max pages for full run

# --- Function to display help message ---
show_help() {
  echo -e "${BLUE}Missile Data Scraper Runner${NC}"
  echo ""
  echo "Usage: ./scripts/run_scraper.sh [OPTIONS]"
  echo ""
  echo "This script runs the Scrapy missile data scraper with various options."
  echo ""
  echo "Options:"
  echo "  --test              Quick test run (3 items, 1 page) [default]"
  echo "  --full              Full scraping run (all ${MAX_PAGES_TO_SCRAPE} pages)"
  echo "  --pages N           Custom run with N pages"
  echo "  --delay N           Set delay between requests to N seconds"
  echo "  --help, -h          Show this help message"
  echo ""
  echo "Examples:"
  echo "  ./scripts/run_scraper.sh --test                    # Quick test run"
  echo "  ./scripts/run_scraper.sh --full                    # Full scraping run"
  echo "  ./scripts/run_scraper.sh --pages 5 --delay 2       # 5 pages with 2s delay"
  echo "  ./scripts/run_scraper.sh --pages 10                # 10 pages with default delay"
  echo ""
  echo "Prerequisites:"
  echo "  - Virtual environment must be activated"
  echo "  - Scrapy project must exist in missilery_scraper/"
  echo ""
  echo "Output files:"
  echo "  missilery_scraper/data/missiles_basic.json     # Basic missile data index"
  echo "  missilery_scraper/data/missiles_detailed.json  # Detailed missile index"
  echo "  missilery_scraper/data/detailed/               # Individual detailed files"
  echo ""
}

# --- Parse arguments ---
MODE="test" # Default mode
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --test)
            MODE="test"
            shift
            ;;
        --full)
            MODE="full"
            shift
            ;;
        --pages)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                CLOSESPIDER_PAGECOUNT="$2"
                MODE="custom"
                shift 2
            else
                echo -e "${RED}Error: --pages requires a number.${NC}"
                exit 1
            fi
            ;;
        --delay)
            if [[ -n "$2" && "$2" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
                DOWNLOAD_DELAY="$2"
                shift 2
            else
                echo -e "${RED}Error: --delay requires a number.${NC}"
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

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Error: Scrapy project directory not found at $PROJECT_DIR${NC}"
    echo -e "${YELLOW}Please ensure the missilery_scraper directory exists.${NC}"
    exit 1
fi

# --- Set spider settings based on mode ---
SPIDER_SETTINGS=""
if [ "$MODE" == "test" ]; then
    CLOSESPIDER_ITEMCOUNT="3"
    CLOSESPIDER_PAGECOUNT="1"
    echo -e "${BLUE}[INFO]${NC} Running test mode (3 items, 1 page)..."
elif [ "$MODE" == "full" ]; then
    CLOSESPIDER_PAGECOUNT="${MAX_PAGES_TO_SCRAPE}"
    echo -e "${BLUE}[INFO]${NC} Running full scraping mode (all ${MAX_PAGES_TO_SCRAPE} pages)..."
elif [ "$MODE" == "custom" ]; then
    echo -e "${BLUE}[INFO]${NC} Running custom mode (${CLOSESPIDER_PAGECOUNT} pages, ${DOWNLOAD_DELAY}s delay)..."
fi

if [ -n "$CLOSESPIDER_ITEMCOUNT" ]; then
    SPIDER_SETTINGS+=" -s CLOSESPIDER_ITEMCOUNT=${CLOSESPIDER_ITEMCOUNT}"
fi
if [ -n "$CLOSESPIDER_PAGECOUNT" ]; then
    SPIDER_SETTINGS+=" -s CLOSESPIDER_PAGECOUNT=${CLOSESPIDER_PAGECOUNT}"
fi
SPIDER_SETTINGS+=" -s DOWNLOAD_DELAY=${DOWNLOAD_DELAY}"
SPIDER_SETTINGS+=" -s ROBOTSTXT_OBEY=${ROBOTSTXT_OBEY}"
SPIDER_SETTINGS+=" -L ${LOG_LEVEL}"

# --- Activate virtual environment ---
echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
if [ -f "${VENV_PATH}/bin/activate" ]; then
    source "${VENV_PATH}/bin/activate"
else
    echo -e "${RED}Error: Virtual environment not found at ${VENV_PATH}. Please run ./scripts/setup_env.sh first.${NC}"
    exit 1
fi

# --- Run Scrapy spider ---
echo -e "${BLUE}[INFO]${NC} Executing: scrapy crawl ${SPIDER_NAME} ${SPIDER_SETTINGS}"
echo ""
echo -e "${BLUE}[INFO]${NC} Starting missile data scraper..."
echo ""

# Change to the Scrapy project directory
pushd "${PROJECT_DIR}" > /dev/null

scrapy crawl "${SPIDER_NAME}" ${SPIDER_SETTINGS}

SCRAPY_EXIT_CODE=$?

# Change back to the original directory
popd > /dev/null

if [ $SCRAPY_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}[SUCCESS]${NC} Scraping completed successfully!"

    # Summarize results
    BASIC_RECORDS=$(jq '. | length' "${PROJECT_DIR}/data/missiles_basic.json" 2>/dev/null || echo 0)
    DETAILED_RECORDS=$(jq '. | length' "${PROJECT_DIR}/data/missiles_detailed.json" 2>/dev/null || echo 0)
    INDIVIDUAL_FILES=$(find "${PROJECT_DIR}/data/detailed" -maxdepth 1 -type f -name "*.json" 2>/dev/null | wc -l)

    echo -e "\n${BLUE}[INFO]${NC} Results:"
    echo -e "  - Basic missile records: ${BASIC_RECORDS}"
    echo -e "  - Detailed missile records: ${DETAILED_RECORDS}"
    echo -e "  - Individual detailed files: ${INDIVIDUAL_FILES}"

    echo -e "\n${BLUE}[INFO]${NC} Data saved to:"
    echo -e "  - ${PROJECT_DIR}/data/missiles_basic.json"
    echo -e "  - ${PROJECT_DIR}/data/missiles_detailed.json"
    echo -e "  - ${PROJECT_DIR}/data/detailed/ (individual files)"
    echo -e "${GREEN}[SUCCESS]${NC} Done!"
else
    echo -e "\n${RED}[ERROR]${NC} Scrapy spider exited with code ${SCRAPY_EXIT_CODE}. Please check the logs above for details."
fi

deactivate