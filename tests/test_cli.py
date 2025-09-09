"""
Unit tests for dbbackup.cli module.
"""

import pytest
from dbbackup.cli import parse_args
import sys


def test_parse_backup_arguments(monkeypatch):
    """
    Test CLI parsing for backup operation.
    """
    test_args = ["main.py", "--backup", "--databases", "db1", "db2"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_args()
    assert args.backup is True
    assert args.databases == ["db1", "db2"]
    assert args.restore is False
    assert args.verify is False


def test_parse_restore_arguments(monkeypatch):
    """
    Test CLI parsing for restore operation.
    """
    test_args = ["main.py", "--restore", "--database", "db1", "--file", "backup.sql"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_args()
    assert args.restore is True
    assert args.database == "db1"
    assert args.file == "backup.sql"
    assert args.backup is False
    assert args.verify is False


def test_parse_verify_arguments(monkeypatch):
    """
    Test CLI parsing for verify operation with dry-run.
    """
    test_args = ["main.py", "--verify", "--file", "backup.sql", "--dry-run"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_args()
    assert args.verify is True
    assert args.file == "backup.sql"
    assert args.dry_run is True