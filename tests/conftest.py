"""
Define fixtures for all tests
"""

import pytest
from dbbackup.core.config_loader import load_config
from dbbackup.core.logger import get_logger

@pytest.fixture
def config_and_logger():
    """
    Fixture to provide config and logger for tests
    """
    config = load_config("config/config.yaml")
    logger = get_logger("test_logger", log_dir="logs_test", console=False)
    return config, logger