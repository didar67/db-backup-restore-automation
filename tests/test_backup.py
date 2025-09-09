"""
Unit tests for dbbackup.core.backup module.
"""

import pytest
from unittest.mock import MagicMock
from dbbackup.core.backup import DatabaseBackup
from dbbackup.core.config_loader import load_config
from dbbackup.core.logger import get_logger
from pathlib import Path


@pytest.fixture
def config_and_logger():
    """
    Fixture to load config and logger for testing.
    """
    config = load_config("config/config.yaml")
    logger = get_logger("test_backup", log_dir="logs_test", console=False)
    return config, logger


def test_backup_run_dry_run(config_and_logger, monkeypatch):
    """
    Test DatabaseBackup.run() with dry-run mode to prevent actual backup execution.
    """
    config, logger = config_and_logger
    config.runtime.dry_run = True  # Ensure dry-run is enabled

    db_backup = DatabaseBackup(config, logger)

    # Mock the executor.run method to monitor calls without executing
    mock_run = MagicMock()
    db_backup.executor.run = mock_run

    db_backup.run(databases=["test_db"])
    mock_run.assert_called()  # Ensure executor.run was called

    # Optional: check the command contains database name
    called_args = mock_run.call_args[0][0]
    assert "test_db" in called_args


def test_backup_single_database_invalid_type(config_and_logger):
    """
    Test DatabaseBackup with unsupported database type.
    """
    config, logger = config_and_logger
    config.database.type = "unsupported_db"

    db_backup = DatabaseBackup(config, logger)
    # Should not raise but log error
    db_backup._backup_single_database("mydb")