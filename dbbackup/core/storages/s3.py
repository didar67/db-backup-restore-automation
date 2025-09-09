"""
Handle AWS S3 storage operations for database backups.
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pathlib import Path
import logging


class S3Storage:
    """
    AWS S3 storage handler for database backups.
    """

    def __init__(self, bucket_name: str, logger: logging.Logger, aws_region: str = "us-east-1"):
        """
        Initialize S3Storage.

        Args:
            bucket_name (str): Name of the S3 bucket
            logger (logging.Logger): Logger instance
            aws_region (str): AWS region
        """
        self.bucket_name = bucket_name
        self.logger = logger
        self.s3 = boto3.client("s3", region_name=aws_region)

    def upload_backup(self, source_file: str, target_key: str):
        """
        Upload a local backup file to S3.

        Args:
            source_file (str): Path to the local backup file
            target_key (str): Desired S3 object key
        """
        path = Path(source_file)
        if not path.exists() or not path.is_file():
            self.logger.error(f"Backup file does not exist: {source_file}")
            return

        try:
            self.s3.upload_file(str(path), self.bucket_name, target_key)
            self.logger.info(f"Backup uploaded to S3: s3://{self.bucket_name}/{target_key}")
        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"S3 upload failed: {e}")

    def list_backups(self, prefix: str = "") -> list[str]:
        """
        List backup objects in the S3 bucket with optional prefix.

        Args:
            prefix (str): Optional key prefix

        Returns:
            list[str]: List of S3 object keys
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            objects = response.get("Contents", [])
            keys = [obj["Key"] for obj in objects]
            self.logger.debug(f"S3 backups found: {keys}")
            return keys
        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"S3 list backups failed: {e}")
            return []