#!/usr/bin/env python3
"""
Example queries for the Missilery database
Demonstrates various ways to query the relational database
"""

from .database_models import DatabaseManager
from sqlalchemy import text
from .constants import (
    DEFAULT_QUERY_LIMIT, SAMPLE_DATA_LIMIT, STATISTICS_LIMIT,
    RANGE_CATEGORIES, YEAR_DECADES, SEPARATOR_LINE, DASH_LINE,
    QUERY_EXAMPLES_TITLE, QUERY_COMPLETED_TITLE, QUERY_SECTIONS,
    QUERY_SECTION_DASH, QUERY_SECTION_DASH_LONG, QUERY_SECTION_DASH_EXTRA_LONG,
    RANGE_CATEGORY_SQL, YEAR_DECADE_SQL, ALL_TABLES,
    STRATEGIC_MISSILES_CONDITION, MISSILES_WITH_IMAGES_CONDITION,
    DETAILED_MISSILES_CONDITION, MISSILES_WITH_CHARACTERISTICS_CONDITION,
    MIN_MISSILE_COUNT_FOR_GROUPING
)

def run_example_queries():
    """Run example queries to demonstrate database capabilities"""

    # Initialize database connection
    db_manager = DatabaseManager("sqlite:///missilery.db")
    session = db_manager.get_session()

    print(SEPARATOR_LINE)
    print(QUERY_EXAMPLES_TITLE)
    print(SEPARATOR_LINE)

    # Query 1: Basic missile count by country
    print(f"\n{QUERY_SECTIONS['MISSILES_BY_COUNTRY']}")
    print(DASH_LINE)
    result = session.execute(text(f"""
        SELECT c.name as country, COUNT(m.id) as missile_count
        FROM countries c
        LEFT JOIN missiles m ON c.id = m.country_id
        GROUP BY c.name
        ORDER BY missile_count DESC
        LIMIT {DEFAULT_QUERY_LIMIT}
    """))

    for row in result:
        print(f"{row.country}: {row.missile_count} missiles")

    # Query 2: Missiles by purpose
    print(f"\n{QUERY_SECTIONS['MISSILES_BY_PURPOSE']}")
    print(QUERY_SECTION_DASH)
    result = session.execute(text(f"""
        SELECT p.name as purpose, COUNT(m.id) as missile_count
        FROM purposes p
        LEFT JOIN missiles m ON p.id = m.purpose_id
        GROUP BY p.name
        ORDER BY missile_count DESC
        LIMIT {DEFAULT_QUERY_LIMIT}
    """))

    for row in result:
        print(f"{row.purpose}: {row.missile_count} missiles")

    # Query 3: Strategic missiles with detailed data
    print(f"\n{QUERY_SECTIONS['STRATEGIC_MISSILES']}")
    print(QUERY_SECTION_DASH_EXTRA_LONG)
    result = session.execute(text(f"""
        SELECT m.name, c.name as country, m.range_km, md.range_detailed
        FROM missiles m
        JOIN countries c ON m.country_id = c.id
        JOIN purposes p ON m.purpose_id = p.id
        LEFT JOIN missile_detailed_data md ON m.id = md.missile_id
        WHERE {STRATEGIC_MISSILES_CONDITION}
        ORDER BY m.range_km DESC
        LIMIT {DEFAULT_QUERY_LIMIT}
    """))

    for row in result:
        range_info = row.range_detailed if row.range_detailed else f"{row.range_km} km"
        print(f"{row.name} ({row.country}): {range_info}")

    # Query 4: Missiles with images
    print(f"\n{QUERY_SECTIONS['MISSILES_WITH_IMAGES']}")
    print(QUERY_SECTION_DASH)
    result = session.execute(text(f"""
        SELECT m.name, COUNT(mi.id) as image_count
        FROM missiles m
        JOIN missile_images mi ON m.id = mi.missile_id
        GROUP BY m.id, m.name
        ORDER BY image_count DESC
        LIMIT {DEFAULT_QUERY_LIMIT}
    """))

    for row in result:
        print(f"{row.name}: {row.image_count} images")

    # Query 5: Characteristics analysis
    print(f"\n{QUERY_SECTIONS['COMMON_CHARACTERISTICS']}")
    print(QUERY_SECTION_DASH_LONG)
    result = session.execute(text(f"""
        SELECT field_name, COUNT(*) as frequency
        FROM characteristics
        GROUP BY field_name
        ORDER BY frequency DESC
        LIMIT {DEFAULT_QUERY_LIMIT}
    """))

    for row in result:
        print(f"{row.field_name}: {row.frequency} occurrences")

    # Query 6: Range analysis
    print(f"\n{QUERY_SECTIONS['RANGE_ANALYSIS']}")
    print(QUERY_SECTION_DASH)
    result = session.execute(text(f"""
        SELECT
            {RANGE_CATEGORY_SQL},
            COUNT(*) as count
        FROM missiles
        WHERE range_km IS NOT NULL
        GROUP BY range_category
        ORDER BY MIN(range_km)
    """))

    for row in result:
        print(f"{row.range_category}: {row.count} missiles")

    # Query 7: Development timeline
    print(f"\n{QUERY_SECTIONS['DEVELOPMENT_TIMELINE']}")
    print(QUERY_SECTION_DASH)
    result = session.execute(text(f"""
        SELECT
            {YEAR_DECADE_SQL},
            COUNT(*) as count
        FROM missiles
        WHERE year_developed IS NOT NULL
        GROUP BY decade
        ORDER BY MIN(year_developed)
    """))

    for row in result:
        print(f"{row.decade}: {row.count} missiles")

    # Query 8: Complex query - Missiles by country and base type
    print(f"\n{QUERY_SECTIONS['COUNTRY_BASE_TYPE']}")
    print(QUERY_SECTION_DASH_EXTRA_LONG)
    result = session.execute(text(f"""
        SELECT
            c.name as country,
            bt.name as base_type,
            COUNT(m.id) as count
        FROM countries c
        JOIN missiles m ON c.id = m.country_id
        JOIN base_types bt ON m.base_type_id = bt.id
        GROUP BY c.name, bt.name
        HAVING COUNT(m.id) > {MIN_MISSILE_COUNT_FOR_GROUPING}
        ORDER BY c.name, count DESC
        LIMIT {STATISTICS_LIMIT}
    """))

    for row in result:
        print(f"{row.country} - {row.base_type}: {row.count} missiles")

    # Query 9: Database statistics
    print(f"\n{QUERY_SECTIONS['DATABASE_STATISTICS']}")
    print(QUERY_SECTION_DASH)
    tables = ALL_TABLES

    for table in tables:
        result = session.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
        count = result.fetchone().count
        print(f"{table}: {count:,} records")

    # Query 10: Sample detailed missile data
    print(f"\n{QUERY_SECTIONS['SAMPLE_DETAILED_DATA']}")
    print(QUERY_SECTION_DASH_LONG)
    result = session.execute(text(f"""
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
        WHERE {MISSILES_WITH_CHARACTERISTICS_CONDITION}
        LIMIT {SAMPLE_DATA_LIMIT}
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

    print("\n" + SEPARATOR_LINE)
    print(QUERY_COMPLETED_TITLE)
    print(SEPARATOR_LINE)

    # Close database connection
    session.close()
    db_manager.close()

if __name__ == "__main__":
    run_example_queries()
