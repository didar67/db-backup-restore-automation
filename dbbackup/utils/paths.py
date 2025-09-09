"""
Utility functions for filesystem operations like directory creation and file validation.
"""
import logging
from pathlib import Path

def ensure_directory(path: Path, logger: logging.Logger):
    """
    Ensure that a directory exists; create it if it does not.

    Args:
        path (Path): Directory path to check or create
        logger (logging.Logger): Logger instance
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {path}")
    except PermissionError as pe:
        logger.error(f"Permission denied creating directory: {path} -> {pe}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating directory: {path} -> {e}")
        raise
    
def validate_file_exists(file_path: str, logger: logging.Logger):
    """
    Validate that a file exists at the given path.

    Args:
        file_path (str): Path to the file
        logger (logging.Logger): Logger instance

    Returns:
        bool: True if file exists, False otherwise
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        logger.error(f"File not found: {file_path}")
        return False
    logger.debug(f"File exists: {file_path}")
    return True