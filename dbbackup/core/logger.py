"""
Configure and provide application-wide logging using RotatingFileHandler.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional
from dbbackup.core.config_loader import PathsConfig

def get_logger(
    name: str,
    log_file: Optional[str] = None,
    log_dir: Optional[str] = None,
    level: int = logging.INFO,
    console: bool = True
) -> logging.Logger:
    """
    Initialize and return a logger with rotating file handler and optional console output.

    Args:
        name (str): Logger name
        log_file (str, optional): Specific log filename
        log_dir (str, optional): Directory to store logs
        level (int): Logging level (default INFO)
        console (bool): Whether to log to console

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger  # Prevent duplicate handlers

    logger.setLevel(level)

    # Ensure log directory exists
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Default log file
    log_path = Path(log_dir or ".") / (log_file or f"{name}.log")

    # Rotating file handler: 10 MB per file, keep 5 backups
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console output
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)
        logger.addHandler(console_handler)

    logger.debug(f"Logger initialized: {log_path}")
    return logger