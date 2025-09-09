"""
Unit tests for dbbackup.core.executor module.
"""

import pytest
from unittest.mock import patch, MagicMock
from dbbackup.core.executor import CommandExecutor
import logging


@pytest.fixture
def logger():
    """
    Fixture to create a logger for testing.
    """
    logger = logging.getLogger("test_executor")
    logger.addHandler(logging.NullHandler())
    return logger


def test_executor_run_dry_run(logger):
    """
    Test CommandExecutor.run() in dry-run mode.
    """
    executor = CommandExecutor(logger, dry_run=True)
    # Should not actually execute
    executor.run("echo 'test command'")


@patch("subprocess.run")
def test_executor_run_success(mock_subprocess, logger):
    """
    Test CommandExecutor.run() executes subprocess successfully.
    """
    executor = CommandExecutor(logger, dry_run=False)
    mock_subprocess.return_value.returncode = 0

    executor.run("echo 'test command'")
    mock_subprocess.assert_called_once()


@patch("subprocess.run")
def test_executor_run_failure(mock_subprocess, logger):
    """
    Test CommandExecutor.run() handles subprocess failure.
    """
    executor = CommandExecutor(logger, dry_run=False)
    mock_subprocess.side_effect = Exception("Execution failed")

    with pytest.raises(Exception):
        executor.run("invalid_command")