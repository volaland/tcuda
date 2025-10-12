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
from database import DatabaseManager

def run_stage1():
    """Run Stage 1: Collect raw HTML data"""
    print("=" * 60)
    print("STAGE 1: Collecting raw HTML data from missilery.info")
    print("=" * 60)
    
    # Change to scraper directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run Scrapy spider for Stage 1
    cmd = ['scrapy', 'crawl', 'missile_spider', '-s', 'stage=1']
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Stage 1 completed successfully!")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Warnings: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Stage 1 failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

def run_stage2():
    """Run Stage 2: Process structured data"""
    print("=" * 60)
    print("STAGE 2: Processing structured data and creating database")
    print("=" * 60)
    
    # Change to scraper directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Import and run data processor
    try:
        from data_processor import DataProcessor
        processor = DataProcessor()
        processor.process_stage2_data()
        print("Stage 2 completed successfully!")
    except Exception as e:
        print(f"Stage 2 failed with error: {e}")
        return False
    
    return True

def show_database_stats():
    """Show database statistics"""
    print("=" * 60)
    print("DATABASE STATISTICS")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        
        # Get counts
        conn = db.db_path
        import sqlite3
        conn = sqlite3.connect(conn)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM index_pages')
        index_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM detail_pages')
        detail_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM missiles')
        missile_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM technical_characteristics')
        tech_count = cursor.fetchone()[0]
        
        print(f"Index pages collected: {index_count}")
        print(f"Detail pages collected: {detail_count}")
        print(f"Missiles processed: {missile_count}")
        print(f"Technical characteristics: {tech_count}")
        
        # Show sample data
        if missile_count > 0:
            print("\nSample missiles:")
            cursor.execute('SELECT name, country, purpose FROM missiles LIMIT 5')
            for row in cursor.fetchall():
                print(f"  - {row[0]} ({row[1]}) - {row[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting database stats: {e}")

def main():
    parser = argparse.ArgumentParser(description='Missilery Scraper - Two-stage data collection')
    parser.add_argument('--stage', type=int, choices=[1, 2], help='Run specific stage (1 or 2)')
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
