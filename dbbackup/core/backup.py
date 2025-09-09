"""
Handle database backup operations with compression and storage integration.
"""
import os
import logging
from datetime import datetime
from dbbackup.core.executor import CommandExecutor
from dbbackup.core.storages.local import LocalStorage
from dbbackup.core.storages.s3 import S3Storage
from dbbackup.utils.timeutils import generate_timestamped_filename
from dbbackup.core.compressor import Compressor

class DatabaseBackup:
    """
    Handles database backup operations including compression and storage.
    """
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.executor = CommandExecutor(logger, dry_run=config.runtime.dry_run)
        
        # Initialize storage handlers
        self.local_storage = LocalStorage(config.paths.backup_dir, logger)
        self.s3_storage = S3Storage(
            bucket_name=config.aws.s3_bucket,
            logger=logger,
            aws_region=config.aws.region
        )
        
        # Initialize compressor
        self.compressor = Compressor(logger)
        
    def run(self, databases: list[str] | None = None):
        """
        Run backup for selected databases.

        Args:
            databases (list[str] | None): List of database names. If None, use defaults.
        """
        if not databases:
            databases = self.config.database.default_databases or ['all']
        
        for db_name in databases:
            self._backup_single_database(db_name)
            
    def _backup_single_database(self, db_name: str):
        """
        Backup a single database, compress it, and save to storage.
        """
        timestamped_filename = generate_timestamped_filename(
            prefix=self.config.app.name,
            db_name=db_name,
            extension="sql",
            logger=self.logger
        )
        
        backup_path = os.path.join(self.config.paths.temp_dir,timestamped_filename)
        
        # Backup command (secure password handling)
        db_type = self.config.database.type.lower()
        try:
            if db_type == "mysql":
                cmd = f"mysqldump -h {self.config.database.host} -P {self.config.database.port} " \
                      f"-u {self.config.database.user} {db_name} > {backup_path}"
                env = os.environ.copy()
                env["MYSQL_PWD"] = self.config.database.password
                self.executor.run(cmd, env=env)

            elif db_type == "postgresql":
                cmd = f"PGPASSWORD={self.config.database.password} pg_dump -h {self.config.database.host} " \
                      f"-p {self.config.database.port} -U {self.config.database.user} {db_name} -f {backup_path}"
                self.executor.run(cmd)
                
            else:
                self.logger.error(f"Unsupported database type: {db_type}")
                return
            
        except Exception as e:
            self.logger.error(f"Backup failed for {db_name}: {e}")
            return
        
        self.logger.info(f"Database backup created: {backup_path}")
        
        # Compress backup
        compressed_file = self.compressor.compress_file(backup_path)
        
        # Save to storage
        self.local_storage.save_backup(compressed_file, os.path.basename(compressed_file))
        self.s3_storage.upload_backup(compressed_file, os.path.basename(compressed_file))
        
        # Optionally, remove temp file
        if os.path.exists(backup_path):
            os.remove(backup_path)
            self.logger.debug(f"Temporary backup file removed: {backup_path}")