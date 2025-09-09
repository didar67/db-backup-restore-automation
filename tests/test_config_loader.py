"""
Unit tests for dbbackup.core.config_loader module.
"""

import pytest
from pathlib import Path
from dbbackup.core.config_loader import load_config, AppConfig
from pydantic import ValidationError


def test_load_valid_config():
    """
    Test loading a valid configuration file.
    """
    config_path = Path("config/config.yaml")
    config = load_config(str(config_path))
    assert isinstance(config, AppConfig)
    assert config.app_name == "DBBackupTool"  # Match your config.yaml


def test_load_missing_config():
    """
    Test loading a non-existent configuration file.
    """
    with pytest.raises(FileNotFoundError):
        load_config("config/missing_config.yaml")


def test_load_invalid_config(tmp_path):
    """
    Test loading an invalid configuration (invalid type) using temporary YAML.
    """
    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("app_name: 123\n")  # Invalid type: should be string
    with pytest.raises(ValidationError):
        load_config(str(invalid_yaml))