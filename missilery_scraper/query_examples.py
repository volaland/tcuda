#!/usr/bin/env python3
"""
Example queries for the Missilery database
Demonstrates various ways to query the relational database
"""

from database_models import DatabaseManager
from sqlalchemy import text

def run_example_queries():
    """Run example queries to demonstrate database capabilities"""
    
    # Initialize database connection
    db_manager = DatabaseManager("sqlite:///missilery.db")
    session = db_manager.get_session()
    
    print("="*60)
    print("MISSILERY DATABASE QUERY EXAMPLES")
    print("="*60)
    
    # Query 1: Basic missile count by country
    print("\n1. MISSILES BY COUNTRY:")
    print("-" * 30)
    result = session.execute(text("""
        SELECT c.name as country, COUNT(m.id) as missile_count
        FROM countries c
        LEFT JOIN missiles m ON c.id = m.country_id
        GROUP BY c.name
        ORDER BY missile_count DESC
        LIMIT 10
    """))
    
    for row in result:
        print(f"{row.country}: {row.missile_count} missiles")
    
    # Query 2: Missiles by purpose
    print("\n2. MISSILES BY PURPOSE:")
    print("-" * 30)
    result = session.execute(text("""
        SELECT p.name as purpose, COUNT(m.id) as missile_count
        FROM purposes p
        LEFT JOIN missiles m ON p.id = m.purpose_id
        GROUP BY p.name
        ORDER BY missile_count DESC
        LIMIT 10
    """))
    
    for row in result:
        print(f"{row.purpose}: {row.missile_count} missiles")
    
    # Query 3: Strategic missiles with detailed data
    print("\n3. STRATEGIC MISSILES WITH DETAILED DATA:")
    print("-" * 40)
    result = session.execute(text("""
        SELECT m.name, c.name as country, m.range_km, md.range_detailed
        FROM missiles m
        JOIN countries c ON m.country_id = c.id
        JOIN purposes p ON m.purpose_id = p.id
        LEFT JOIN missile_detailed_data md ON m.id = md.missile_id
        WHERE p.name LIKE '%Strategic%' AND m.is_detailed = 1
        ORDER BY m.range_km DESC
        LIMIT 10
    """))
    
    for row in result:
        range_info = row.range_detailed if row.range_detailed else f"{row.range_km} km"
        print(f"{row.name} ({row.country}): {range_info}")
    
    # Query 4: Missiles with images
    print("\n4. MISSILES WITH IMAGES:")
    print("-" * 25)
    result = session.execute(text("""
        SELECT m.name, COUNT(mi.id) as image_count
        FROM missiles m
        JOIN missile_images mi ON m.id = mi.missile_id
        GROUP BY m.id, m.name
        ORDER BY image_count DESC
        LIMIT 10
    """))
    
    for row in result:
        print(f"{row.name}: {row.image_count} images")
    
    # Query 5: Characteristics analysis
    print("\n5. MOST COMMON CHARACTERISTICS:")
    print("-" * 35)
    result = session.execute(text("""
        SELECT field_name, COUNT(*) as frequency
        FROM characteristics
        GROUP BY field_name
        ORDER BY frequency DESC
        LIMIT 10
    """))
    
    for row in result:
        print(f"{row.field_name}: {row.frequency} occurrences")
    
    # Query 6: Range analysis
    print("\n6. RANGE ANALYSIS (km):")
    print("-" * 25)
    result = session.execute(text("""
        SELECT 
            CASE 
                WHEN range_km < 100 THEN 'Short (<100km)'
                WHEN range_km < 1000 THEN 'Medium (100-1000km)'
                WHEN range_km < 5000 THEN 'Long (1000-5000km)'
                ELSE 'Very Long (>5000km)'
            END as range_category,
            COUNT(*) as count
        FROM missiles
        WHERE range_km IS NOT NULL
        GROUP BY range_category
        ORDER BY MIN(range_km)
    """))
    
    for row in result:
        print(f"{row.range_category}: {row.count} missiles")
    
    # Query 7: Development timeline
    print("\n7. DEVELOPMENT TIMELINE:")
    print("-" * 25)
    result = session.execute(text("""
        SELECT 
            CASE 
                WHEN year_developed < 1950 THEN 'Pre-1950'
                WHEN year_developed < 1960 THEN '1950s'
                WHEN year_developed < 1970 THEN '1960s'
                WHEN year_developed < 1980 THEN '1970s'
                WHEN year_developed < 1990 THEN '1980s'
                WHEN year_developed < 2000 THEN '1990s'
                WHEN year_developed < 2010 THEN '2000s'
                ELSE '2010s+'
            END as decade,
            COUNT(*) as count
        FROM missiles
        WHERE year_developed IS NOT NULL
        GROUP BY decade
        ORDER BY MIN(year_developed)
    """))
    
    for row in result:
        print(f"{row.decade}: {row.count} missiles")
    
    # Query 8: Complex query - Missiles by country and base type
    print("\n8. MISSILES BY COUNTRY AND BASE TYPE:")
    print("-" * 40)
    result = session.execute(text("""
        SELECT 
            c.name as country,
            bt.name as base_type,
            COUNT(m.id) as count
        FROM countries c
        JOIN missiles m ON c.id = m.country_id
        JOIN base_types bt ON m.base_type_id = bt.id
        GROUP BY c.name, bt.name
        HAVING COUNT(m.id) > 2
        ORDER BY c.name, count DESC
        LIMIT 15
    """))
    
    for row in result:
        print(f"{row.country} - {row.base_type}: {row.count} missiles")
    
    # Query 9: Database statistics
    print("\n9. DATABASE STATISTICS:")
    print("-" * 25)
    tables = [
        'countries', 'purposes', 'base_types', 'warhead_types', 'guidance_systems',
        'missiles', 'missile_detailed_data', 'structured_content', 'characteristics', 'missile_images'
    ]
    
    for table in tables:
        result = session.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
        count = result.fetchone().count
        print(f"{table}: {count:,} records")
    
    # Query 10: Sample detailed missile data
    print("\n10. SAMPLE DETAILED MISSILE DATA:")
    print("-" * 35)
    result = session.execute(text("""
        SELECT 
            m.name,
            c.name as country,
            md.speed,
            md.weight,
            md.length,
            md.engine_type
        FROM missiles m
        JOIN countries c ON m.country_id = c.id
        JOIN missile_detailed_data md ON m.id = md.missile_id
        WHERE md.speed IS NOT NULL OR md.weight IS NOT NULL
        LIMIT 5
    """))
    
    for row in result:
        print(f"\n{row.name} ({row.country})")
        if row.speed:
            print(f"  Speed: {row.speed}")
        if row.weight:
            print(f"  Weight: {row.weight}")
        if row.length:
            print(f"  Length: {row.length}")
        if row.engine_type:
            print(f"  Engine: {row.engine_type}")
    
    print("\n" + "="*60)
    print("QUERY EXAMPLES COMPLETED")
    print("="*60)
    
    # Close database connection
    session.close()
    db_manager.close()

if __name__ == "__main__":
    run_example_queries()
