"""
Handle local filesystem storage operations for backups.
"""

from pathlib import Path
import shutil
import logging
from dbbackup.utils.paths import ensure_directory, validate_file_exists


class LocalStorage:
    """
    Local filesystem storage handler for database backups.
    """

    def __init__(self, backup_dir: str, logger: logging.Logger):
        """
        Initialize LocalStorage.

        Args:
            backup_dir (str): Path to backup directory
            logger (logging.Logger): Logger instance
        """
        self.backup_dir = Path(backup_dir)
        self.logger = logger
        ensure_directory(self.backup_dir, logger)  # Ensure backup folder exists

    def save_backup(self, source_file: str, target_filename: str):
        """
        Save a backup file to the local backup directory.

        Args:
            source_file (str): Path to the source file
            target_filename (str): Desired filename in backup directory
        """
        target_path = self.backup_dir / target_filename
        if not validate_file_exists(source_file, self.logger):
            return
        try:
            shutil.copy2(source_file, target_path)
            self.logger.info(f"Backup saved locally: {target_path}")
        except Exception as e:
            self.logger.error(f"Failed to save backup locally: {e}")

    def list_backups(self) -> list[str]:
        """
        List all backup files in the local backup directory.

        Returns:
            list[str]: List of backup file paths
        """
        files = [str(f) for f in self.backup_dir.glob("*") if f.is_file()]
        self.logger.debug(f"Local backups found: {files}")
        return files