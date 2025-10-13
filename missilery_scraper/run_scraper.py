#!/usr/bin/env python3
"""
Missilery Scraper - Two-stage data collection and processing

Stage 1: Collect raw HTML data from index and detail pages
Stage 2: Process HTML data and create structured database

Usage:
    python run_scraper.py --stage 1  # Collect raw data
    python run_scraper.py --stage 2  # Process structured data
    python run_scraper.py --all      # Run both stages
"""

import os
import sys
import subprocess
import argparse
from missilery_db.database import DatabaseManager
from missilery_scraper.constants import (
    STAGE1_TITLE, STAGE2_TITLE, DATABASE_STATS_TITLE,
    STAGE1_SUCCESS, STAGE2_SUCCESS, STAGE2_PROCESSING_SUCCESS,
    STAGE1_ERROR, STAGE2_ERROR, SEPARATOR_LINE, DASH_LINE,
    STAGE_CHOICES, DEFAULT_QUERY_LIMIT, SAMPLE_DATA_LIMIT,
    INDEX_PAGES_TABLE, DETAIL_PAGES_TABLE, MISSILES_TABLE, TECHNICAL_CHARACTERISTICS_TABLE
)

def run_stage1():
    """Run Stage 1: Collect raw HTML data"""
    print(SEPARATOR_LINE)
    print(STAGE1_TITLE)
    print(SEPARATOR_LINE)

    # Change to scraper directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run Scrapy spider for Stage 1
    cmd = ['scrapy', 'crawl', 'missile_spider', '-s', 'stage=1']
    print(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(STAGE1_SUCCESS)
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Warnings: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"{STAGE1_ERROR} {e}")
        print(f"Error output: {e.stderr}")
        return False

    return True

def run_stage2():
    """Run Stage 2: Process structured data"""
    print(SEPARATOR_LINE)
    print(STAGE2_TITLE)
    print(SEPARATOR_LINE)

    # Change to scraper directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Import and run data processor
    try:
        from missilery_scraper.data_processor import DataProcessor
        processor = DataProcessor()
        processor.process_stage2_data()
        print(STAGE2_SUCCESS)
    except Exception as e:
        print(f"{STAGE2_ERROR} {e}")
        return False

    return True

def show_database_stats():
    """Show database statistics"""
    print(SEPARATOR_LINE)
    print(DATABASE_STATS_TITLE)
    print(SEPARATOR_LINE)

    try:
        db = DatabaseManager()

        # Get counts
        conn = db.db_path
        import sqlite3
        conn = sqlite3.connect(conn)
        cursor = conn.cursor()

        cursor.execute(f'SELECT COUNT(*) FROM {INDEX_PAGES_TABLE}')
        index_count = cursor.fetchone()[0]

        cursor.execute(f'SELECT COUNT(*) FROM {DETAIL_PAGES_TABLE}')
        detail_count = cursor.fetchone()[0]

        cursor.execute(f'SELECT COUNT(*) FROM {MISSILES_TABLE}')
        missile_count = cursor.fetchone()[0]

        cursor.execute(f'SELECT COUNT(*) FROM {TECHNICAL_CHARACTERISTICS_TABLE}')
        tech_count = cursor.fetchone()[0]

        print(f"Index pages collected: {index_count}")
        print(f"Detail pages collected: {detail_count}")
        print(f"Missiles processed: {missile_count}")
        print(f"Technical characteristics: {tech_count}")

        # Show sample data
        if missile_count > 0:
            print("\nSample missiles:")
            cursor.execute(f'SELECT name, country, purpose FROM {MISSILES_TABLE} LIMIT {SAMPLE_DATA_LIMIT}')
            for row in cursor.fetchall():
                print(f"  - {row[0]} ({row[1]}) - {row[2]}")

        conn.close()

    except Exception as e:
        print(f"Error getting database stats: {e}")

def main():
    parser = argparse.ArgumentParser(description='Missilery Scraper - Two-stage data collection')
    parser.add_argument('--stage', type=int, choices=STAGE_CHOICES, help='Run specific stage (1 or 2)')
    parser.add_argument('--all', action='store_true', help='Run both stages')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')

    args = parser.parse_args()

    if args.stats:
        show_database_stats()
        return

    if args.all:
        print("Running both stages...")
        if run_stage1():
            run_stage2()
            show_database_stats()
    elif args.stage == 1:
        run_stage1()
    elif args.stage == 2:
        run_stage2()
        show_database_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
