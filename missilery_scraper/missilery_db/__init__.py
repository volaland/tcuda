"""
Missilery Database Module

This module contains all database-related functionality for the Missilery scraper project.
It provides database models, connection management, and data import/export utilities.

Modules:
    database_models: SQLAlchemy ORM models for the database schema
    database: Database connection and session management
    import_json_to_db: JSON data import functionality
    query_examples: Example queries and data analysis
    corrected_final_summary: Comprehensive data summary and integrity analysis
"""

from .database_models import (
    Base,
    Country,
    Purpose,
    BaseType,
    WarheadType,
    GuidanceSystem,
    Missile,
    MissileDetailedData,
    StructuredContent,
    Characteristic,
    MissileImage,
    ScrapingSession
)

from .database import DatabaseManager
from .import_json_to_db import JSONToDatabaseImporter, main as import_main
from .query_examples import run_example_queries
from .constants import *

__version__ = "1.0.0"
__author__ = "Missilery Scraper Team"

__all__ = [
    "Base",
    "Country",
    "Purpose",
    "BaseType",
    "WarheadType",
    "GuidanceSystem",
    "Missile",
    "MissileDetailedData",
    "StructuredContent",
    "Characteristic",
    "MissileImage",
    "ScrapingSession",
    "DatabaseManager",
    "JSONToDatabaseImporter",
    "import_main",
    "run_example_queries"
]
