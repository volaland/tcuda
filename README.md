# TCUDA Project

A multi-project repository containing various data science and AI projects, including the Missilery Data Scraper.

## Project Structure

```
tcuda/
├── agents/                      # AI Agents projects
├── drone/                       # Drone-related research papers
├── missilery_scraper/          # Standalone Missilery Data Scraper application
├── scripts/                     # Root-level scripts
│   └── setup_env.sh            # Environment setup (PyTorch/CUDA)
├── requirements.txt             # Root-level dependencies (PyTorch, Jupyter, etc.)
└── README.md                    # This file
```

## Missilery Scraper

The **Missilery Scraper** is now a **fully standalone application**. For complete documentation, setup instructions, and usage, see:

**[missilery_scraper/README.md](missilery_scraper/README.md)**

### Quick Reference

The missilery scraper has its own scripts in `missilery_scraper/scripts/`:

```bash
cd missilery_scraper
./scripts/setup_env.sh              # Setup scraper-specific environment
./scripts/run_scraper.sh --test      # Run scraper
./scripts/import_to_database.sh      # Import data to database
```

## Root-Level Setup

The root-level `scripts/setup_env.sh` sets up a Python environment with PyTorch CUDA support and Jupyter ecosystem, which may be useful for other projects in this repository (such as the agents projects).

### Setup Root Environment

```bash
./scripts/setup_env.sh
```

This will:
- Create virtual environment in `.venv/`
- Install PyTorch with CUDA support
- Install Jupyter ecosystem
- Install additional dependencies from `requirements.txt`

## Projects

### Missilery Scraper
A comprehensive web scraping and database system for missile data from missilery.info. **Standalone application** - see `missilery_scraper/README.md` for details.

### Agents
AI agent projects and notebooks - see `agents/` directory.

### Drone
Drone-related research papers and documentation - see `drone/` directory.

---

For detailed documentation on any specific project, please refer to the README files within each project directory.
