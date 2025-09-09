"""
Unit tests for dbbackup.core.restore module.
"""

import pytest
from unittest.mock import MagicMock
from dbbackup.core.restore import DatabaseRestore
from dbbackup.core.config_loader import load_config
from dbbackup.core.logger import get_logger


@pytest.fixture
def config_and_logger():
    """
    Fixture to load config and logger for testing.
    """
    config = load_config("config/config.yaml")
    logger = get_logger("test_restore", log_dir="logs_test", console=False)
    return config, logger


def test_restore_run_dry_run(config_and_logger, monkeypatch):
    """
    Test DatabaseRestore.run() with dry-run mode.
    """
    config, logger = config_and_logger
    config.runtime.dry_run = True  # Ensure dry-run is enabled

    db_restore = DatabaseRestore(config, logger)

    # Mock the executor.run method to monitor calls without executing
    mock_run = MagicMock()
    db_restore.executor.run = mock_run

    db_restore.run(target_db="test_db", backup_file="backup.sql")
    mock_run.assert_called()  # Ensure executor.run was called

    # Optional: check command contains database name
    called_args = mock_run.call_args[0][0]
    assert "test_db" in called_args


def test_restore_no_file(config_and_logger):
    """
    Test restoring a database without specifying a valid backup file.
    """
    config, logger = config_and_logger
    db_restore = DatabaseRestore(config, logger)

    # Should log an error but not raise
    db_restore.run(target_db="test_db", backup_file="nonexistent.sql")