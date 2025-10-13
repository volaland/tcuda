#!/usr/bin/env python3
"""
Main entry point for the missilery_db module
Allows running database operations as a module: python -m missilery_db
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point for the missilery_db module"""
    parser = argparse.ArgumentParser(
        description='Missilery Database Operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m missilery_db import --database missilery.db
  python -m missilery_db import --update --database missilery.db
  python -m missilery_db query
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import JSON data to database')
    import_parser.add_argument('--update', action='store_true',
                              help='Update existing records instead of creating new ones')
    import_parser.add_argument('--database', default='missilery.db',
                              help='Database file name (default: missilery.db)')

    # Query command
    query_parser = subparsers.add_parser('query', help='Run example queries')
    query_parser.add_argument('--database', default='missilery.db',
                             help='Database file name (default: missilery.db)')

    args = parser.parse_args()

    if args.command == 'import':
        from .import_json_to_db import main as import_main
        # Set up sys.argv for the import script
        sys.argv = ['import_json_to_db.py']
        if args.update:
            sys.argv.append('--update')
        if args.database != 'missilery.db':
            sys.argv.extend(['--database', args.database])
        import_main()

    elif args.command == 'query':
        from .query_examples import run_example_queries
        run_example_queries()

    # elif args.command == 'summary':
    #     from .corrected_final_summary import corrected_final_summary
    #     corrected_final_summary()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
