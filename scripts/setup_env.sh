#!/bin/bash

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"

# --- Colors for output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Function to display help message ---
show_help() {
  echo -e "${BLUE}PyTorch CUDA Environment Setup${NC}"
  echo ""
  echo "Usage: ./scripts/setup_env.sh [OPTIONS]"
  echo ""
  echo "This script sets up a Python 3.13 environment with PyTorch and CUDA support."
  echo ""
  echo "Options:"
  echo "  --help, -h          Show this help message"
  echo ""
  echo "Prerequisites:"
  echo "  - Python 3.13 installed"
  echo "  - NVIDIA GPU with CUDA support (optional)"
  echo ""
  echo "What this script does:"
  echo "  - Creates virtual environment in .venv/"
  echo "  - Installs PyTorch with CUDA support"
  echo "  - Installs Jupyter ecosystem"
  echo "  - Installs Scrapy for web scraping"
  echo "  - Verifies installation"
  echo ""
}

# --- Parse arguments ---
while [[ "$#" -gt 0 ]]; do
    case "$1" in
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

set -e

echo -e "${BLUE}[INFO]${NC} Setting up PyTorch CUDA environment..."
echo -e "${BLUE}[INFO]${NC} Project root: $PROJECT_ROOT"
echo -e "${BLUE}[INFO]${NC} Virtual environment: $VENV_PATH"

if ! command -v python3.13 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3.13 not found.${NC}"
    echo -e "${YELLOW}Please install Python 3.13 first.${NC}"
    exit 1
fi

if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} NVIDIA GPU not detected. PyTorch will be installed with CPU support only."
fi

echo -e "${BLUE}[INFO]${NC} Creating virtual environment..."
python3.13 -m venv "$VENV_PATH"

echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}[INFO]${NC} Upgrading pip..."
python -m pip install --upgrade pip

echo -e "${BLUE}[INFO]${NC} Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo -e "${BLUE}[INFO]${NC} Verifying installation..."
python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'Number of GPUs: {torch.cuda.device_count()}')
    print(f'Current GPU: {torch.cuda.get_device_name(0)}')
else:
    print('Running on CPU only')
"

echo -e "${GREEN}[SUCCESS]${NC} Environment setup complete!"
echo -e "${BLUE}[INFO]${NC} Virtual environment created at: $VENV_PATH"
echo -e "${BLUE}[INFO]${NC} To activate: source .venv/bin/activate"
