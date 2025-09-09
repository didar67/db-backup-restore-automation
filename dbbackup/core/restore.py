"""
Restore databases from backup files.
"""

import os
import logging
from pathlib import Path
from dbbackup.core.executor import CommandExecutor
from dbbackup.core.storages.local import LocalStorage
from dbbackup.core.storages.s3 import S3Storage
from dbbackup.utils.paths import validate_file_exists

class DatabaseRestore:
    """
    Class to handle database restore operations.
    """

    def __init__(self, config, logger: logging.Logger):
        """
        Initialize DatabaseRestore.

        Args:
            config: Application configuration object
            logger (logging.Logger): Logger instance
        """
        self.config = config
        self.logger = logger
        self.executor = CommandExecutor(logger, dry_run=config.runtime.dry_run)
        self.local_storage = LocalStorage(config.paths.backup_dir, logger)
        self.s3_storage = S3Storage(config.aws.s3_bucket, logger, config.aws.region)
        
    def run(self, target_db: str, backup_file: str):
        """
        Restore a database from backup.

        Args:
            target_db (str): Database name to restore
            backup_file (str, optional): Specific backup file
        """
        
        # Determine backup file to restore
        if backup_file:
            if not validate_file_exists(backup_file, self.logger):
                self.logger.error(f"Backup file not found: {backup_file}")
                return
            backup_path = backup_file
        else:
            # Attempt to get latest backup for the database from local
            backups = [f for f in self.local_storage.list_backups() if target_db in f]
            if not backups:
                self.logger.error(f"No backups found for database '{target_db}'")
                return
            backup_path = sorted(backups)[-1]  # Latest backup
            
        self.logger.info(f"Restoring database '{target_db}' from backup: {backup_path}")
        
        # Restore based on database type
        db_type = self.config.database.type.lower()
        if db_type == "mysql":
            self._restore_mysql(target_db, backup_path)
        elif db_type == "postgresql":
            self._restore_postgresql(target_db, backup_path)
        else:
            self.logger.error(f"Unsupported database type: {db_type}")
            
    def _restore_mysql(self, db_name: str, backup_path: str):
        """
        Restore MySQL database from backup file.

        Args:
            db_name (str): Database name
            backup_path (str): Path to backup file
        """
        self.logger.info(f"MySQL restore initiated for database '{db_name}'")
        env = os.environ.copy()
        env["MYSQL_PWD"] = self.config.database.password

        cmd = f"mysql -h {self.config.database.host} -P {self.config.database.port} -u {self.config.database.user} {db_name} < {backup_path}"
        self.executor.run(cmd, env=env)
        self.logger.info(f"MySQL restore completed for database '{db_name}'")

    def _restore_postgresql(self, db_name: str, backup_path: str):
        """
        Restore PostgreSQL database from backup file.

        Args:
            db_name (str): Database name
            backup_path (str): Path to backup file
        """
        self.logger.info(f"PostgreSQL restore initiated for database '{db_name}'")
        env = os.environ.copy()
        env["PGPASSWORD"] = self.config.database.password

        cmd = f"psql -h {self.config.database.host} -p {self.config.database.port} -U {self.config.database.user} -d {db_name} -f {backup_path}"
        self.executor.run(cmd, env=env)
        self.logger.info(f"PostgreSQL restore completed for database '{db_name}'")