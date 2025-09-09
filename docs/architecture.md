# DBBackup Tool Architecture

## Overview
DBBackup is a Python-based Database Backup & Restore tool supporting MySQL and PostgreSQL. It provides modular, enterprise-grade architecture with logging, CLI, configuration management, and optional cloud storage (S3).

## Modules

### dbbackup/
- `__init__.py` : Package initialization
- `cli.py` : Handles command-line arguments with argparse
- `core/` : Core functionality modules
  - `config_loader.py` : Loads and validates configuration using Pydantic
  - `logger.py` : Sets up RotatingFileHandler and console logging
  - `executor.py` : Executes shell commands securely
  - `backup.py` : Handles database backup operations
  - `restore.py` : Handles database restore operations
  - `compressor.py` : Optional compression of backup files
  - `verifier.py` : Validates backup integrity
  - `storages/` : Storage handlers
    - `local.py` : Local filesystem storage
    - `s3.py` : AWS S3 storage
- `utils/` : Utility functions
  - `paths.py` : Directory and file helpers
  - `timeutils.py` : Timestamped filename generation
- `version.py` : Maintains tool version

### tests/
- Unit tests for all modules using pytest and unittest.mock

## Features
- CLI operations: backup, restore, verify
- Dry-run and verbose modes
- Modular, reusable, professional-grade code
- Rotating logging with console output
- Pydantic-based configuration validation
- Local and S3 storage support
- Unit tests for reliability