"""
Utility functions for generating timestamped filenames for backups.
"""

from datetime import datetime
from pathlib import Path
import logging
from typing import Optional

def generate_timestamped_filename(
    prefix: str,
    db_name: str,
    extension: str = "sql",
    logger: Optional[logging.Logger] = None
) -> str:
    """
    Generate a filename with the current timestamp.

    Args:
        prefix (str): Prefix for the filename (usually app name)
        db_name (str): Database name
        extension (str): File extension (default 'sql')
        logger (logging.Logger, optional): Logger instance

    Returns:
        str: Timestamped filename in format: prefix_dbname_YYYYmmdd_HHMMSS.ext
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{db_name}_{timestamp}.{extension}"
    if logger:
        logger.debug(f"Generated timestamped filename: {filename}")
    return filename

def get_current_timestamp(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get the current timestamp as a string in the given format.

    Args:
        fmt (str): Datetime format string (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        str: Formatted current timestamp
    """
    return datetime.now().strftime(fmt)