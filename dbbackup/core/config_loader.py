"""
Load and validate configuration using Pydantic, supporting environment variables for sensitive data.
"""

import yaml
import os
import logging
from pathlib import Path
from pydantic import BaseModel, field_validator, Field
from dbbackup.utils.paths import ensure_directory

# Pydantic Models for Validation
class AppConfig(BaseModel):
    app_name: str
    version: str
    
class DatabaseConfig(BaseModel):
    type: str
    host: str
    port: int
    user: str
    password: str = Field(..., description="Database password (from ENV variable preferred)")
    default_databases: list[str] = []
    
    @field_validator("password", mode="before")
    def load_password_from_env(cls, v):
        """
        Load password from environment variable if available.
        """
        env_password = os.getenv("DB_PASSWORD")
        if env_password:
            return env_password
        if v:
            return v
        raise ValueError("Database password must be provided either in config.yaml or via DB_PASSWORD environment variable.")
    
class PathsConfig(BaseModel):
    backup_dir: str
    log_dir: str
    temp_dir: str
    
class RuntimeConfig(BaseModel):
    dry_run: bool =False
    verbose: bool = False
    max_concurrent_jobs: int = 1
    
class AWSConfig(BaseModel):
    s3_bucket: str
    region: str = "us-east-1"
    
class Config(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    paths: PathsConfig
    runtime: RuntimeConfig
    aws: AWSConfig
    
# Configuration Loader Function
def load_config(config_path: str = "config/config.yaml", logger: logging.Logger | None = None) -> Config:
    """
    Load YAML configuration and validate using Pydantic.
    
    Args:
        config_path (str): Path to the YAML config file.
        logger (logging.Logger | None): Optional logger instance.
    
    Returns:
        Config: Validated configuration object.
    """
    config_file = Path(config_path)
    if not config_file.is_file():
        if logger:
            logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config.model_validate(raw_config)

    # Ensure directories exist
    if logger:
        ensure_directory(Path(config.paths.backup_dir), logger)
        ensure_directory(Path(config.paths.log_dir), logger)
        ensure_directory(Path(config.paths.temp_dir), logger)

    return config