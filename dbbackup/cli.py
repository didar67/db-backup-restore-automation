"""
Define and parse command-line arguments for the database backup tool.
"""

import argparse
from typing import List


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for DBBackup tool.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    epilog_text = (
        "Examples:\n"
        "  python main.py init                   # Initialize folder structure and sample config\n"
        "  python main.py backup --databases mydb1 mydb2\n"
        "  python main.py restore --database mydb1 --file backup.sql\n"
        "  python main.py verify --all\n"
        "  python main.py list                   # List available backups\n"
    )

    parser = argparse.ArgumentParser(
        description="DBBackup Tool: Backup, Restore, Verify Databases",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Primary operations
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--backup", action="store_true", help="Perform database backup")
    group.add_argument("--restore", action="store_true", help="Restore database from backup")
    group.add_argument("--verify", action="store_true", help="Verify backup files")
    group.add_argument("--list", action="store_true", help="List available backups")
    group.add_argument("--init", action="store_true", help="Initialize project directories and sample config")

    # Database selection
    parser.add_argument(
        "--databases", nargs="+", help="List of databases to backup"
    )
    parser.add_argument(
        "--database", help="Target database to restore or verify"
    )

    # File selection
    parser.add_argument(
        "--file", help="Specify backup file for restore or verify"
    )

    # Runtime options
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate commands without executing"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()
    return args