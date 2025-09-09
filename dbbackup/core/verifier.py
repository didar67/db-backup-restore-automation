"""
Verify integrity of backup files for databases.
"""
import logging
from pathlib import Path
from typing import Optional
from dbbackup.core.storages.local import LocalStorage
from dbbackup.core.storages.s3 import S3Storage
from dbbackup.utils.paths import validate_file_exists

class BackupVerifier:
    """
    Class to verify backup files.
    """
    def __init__(self, config, logger: logging.Logger):
        """
        Initialize BackupVerifier.

        Args:
            config: Application configuration object
            logger (logging.Logger): Logger instance
        """
        self.config = config
        self.logger = logger
        self.local_storage = LocalStorage(config.paths.backup_dir, logger)
        self.s3_storage = S3Storage(config.aws.s3_bucket, logger, config.aws.region)
    def run(self, all_files: bool = False, backup_file: Optional[str] = None, target_db: Optional[str] = None):
        """
        Verify backup files based on user input.

        Args:
            all_files (bool): Verify all backups
            backup_file (str): Specific backup file to verify
            target_db (str): Specific database name
        """
        if all_files:
            self.logger.info("Verifying all backups...")
            local_backups = self.local_storage.list_backups()
            s3_backups = self.s3_storage.list_backups()
            self._verify_list(local_backups, "Local")
            self._verify_list(s3_backups, "S3")
        else:
            if backup_file:
                self.logger.info(f"Verifying backup file: {backup_file}")
                if validate_file_exists(backup_file, self.logger):
                    self.logger.info(f"Backup file verified: {backup_file}")
            elif target_db:
                self.logger.info(f"Verifying backups for database: {target_db}")
                local_backups = [f for f in self.local_storage.list_backups() if target_db in f]
                s3_backups = [f for f in self.s3_storage.list_backups() if target_db in f]
                self._verify_list(local_backups, "Local")
                self._verify_list(s3_backups, "S3")
            else:
                self.logger.error("No file or database specified for verification.")
            
    def _verify_list(self, file_list: list[str], storage_type: str):
        """
        Internal helper to verify a list of files.

        Args:
            file_list (list[str]): List of file paths
            storage_type (str): Storage type name for logging
        """
        if not file_list:
            self.logger.warning(f"No backups found in {storage_type} storage.")
            return

        for f in file_list:
            path = Path(f)
            if path.is_file():
                self.logger.info(f"{storage_type} backup verified: {f}")
            else:
                self.logger.error(f"{storage_type} backup missing or corrupted: {f}")