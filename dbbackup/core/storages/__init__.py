"""
Storage handlers package for DBBackup tool.

This package provides convenient imports for storage backends, allowing
users to easily switch between local filesystem storage and AWS S3 storage.
"""

from dbbackup.core.storages.local import LocalStorage
from dbbackup.core.storages.s3 import S3Storage

__all__ = ["LocalStorage", "S3Storage"]