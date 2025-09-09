## Overview

DBBackup is a professional-grade Python-based Database Backup & Restore tool supporting **MySQL** and **PostgreSQL**. It offers modular, reusable architecture with robust logging, CLI support, configuration management, optional S3 cloud storage, and comprehensive unit tests.

## Features

* **Database Operations:** Backup, Restore, and Verify databases.
* **CLI Support:** Flexible command-line interface for automation.
* **Dry-Run Mode:** Simulate operations without actual execution.
* **Verbose Mode:** Detailed logging for debugging and monitoring.
* **Storage Options:** Save backups locally or upload to AWS S3.
* **Timestamped Filenames:** Automatic timestamped backup filenames.
* **Configuration Management:** YAML-based configuration with Pydantic validation.
* **Logging:** Rotating logs with console output.
* **Unit Tests:** Reliable and testable codebase using `pytest` and `unittest.mock`.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dbbackup.git
cd dbbackup

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to set your database credentials, backup paths, runtime options, and optional AWS S3 settings.

Example:

```yaml
app:
  name: DBBackupTool
  version: "1.0.0"

database:
  type: mysql
  host: localhost
  port: 3306
  user: backup_user
  password: secure_password
  default_databases: []

paths:
  backup_dir: backups/
  log_dir: logs/
  temp_dir: temp/

runtime:
  dry_run: false
  verbose: false
  max_concurrent_jobs: 4

aws:
  s3_bucket: my-db-backups
  region: us-east-1
```

## Usage

```bash
# Initialize project directories and sample config
python main.py --init

# Backup databases
python main.py --backup --databases db1 db2

# Restore a database
python main.py --restore --database db1 --file backup.sql

# Verify a backup
python main.py --verify --file backup.sql

# List all backups
python main.py --list
```

### Runtime Options

* `--dry-run` : Simulate operations without executing.
* `--verbose` : Enable detailed logging.

## Project Structure

```
dbbackup/
├── cli.py                  # CLI argument parsing
├── core/
│   ├── backup.py          # Backup operations
│   ├── restore.py         # Restore operations
│   ├── verifier.py        # Backup verification
│   ├── executor.py        # Command execution
│   ├── logger.py          # Logging setup
│   ├── config_loader.py   # Configuration loader
│   ├── compressor.py      # Optional compression
│   └── storages/
│       ├── local.py       # Local storage
│       └── s3.py          # AWS S3 storage
├── utils/
│   ├── paths.py           # Path utilities
│   └── timeutils.py       # Timestamped filename generator
└── version.py              # Version info
```

## Testing

Run unit tests using `pytest`:

```bash
pytest tests/
```

Tests cover CLI parsing, backup, restore, executor, and configuration loader modules.

## Docker Support

The project includes a Dockerfile and optional `docker-compose.yml` for containerized execution. Refer to `docs/docker.md` for details.

## Logging

Logs are written to the configured log directory with rotation and console output. Use `--verbose` for detailed runtime information.

## License

This project is licensed under the MIT License.