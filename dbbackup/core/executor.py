"""
Safely execute shell commands with logging, error handling, and dry-run support.
"""

import subprocess
import logging
from typing import Optional


class CommandExecutor:
    """
    Execute system commands with optional dry-run and proper logging.
    """

    def __init__(self, logger: logging.Logger, dry_run: bool = False):
        """
        Initialize CommandExecutor.

        Args:
            logger (logging.Logger): Logger instance
            dry_run (bool): If True, commands are printed but not executed
            env (dict | None): Optional environment variables
        """
        self.logger = logger
        self.dry_run = dry_run

    def run(self, command: str, capture_output: bool = False, env: dict | None = None) -> Optional[str]:
        """
        Execute a shell command safely.

        Args:
            command (str): Shell command to execute
            capture_output (bool): Whether to capture stdout

        Returns:
            Optional[str]: Command output if captured

        Raises:
            RuntimeError: If command execution fails
        """
        self.logger.debug(f"Executing command: {command}")

        if self.dry_run:
            self.logger.info(f"[DRY-RUN] Command not executed: {command}")
            return None

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=capture_output,
                text=True,
                env=env
            )
            if capture_output:
                self.logger.debug(f"Command output: {result.stdout.strip()}")
                return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}: {command}")
            self.logger.error(f"stderr: {e.stderr.strip() if e.stderr else 'N/A'}")
            raise RuntimeError(f"Command execution failed: {e}")
        except Exception as ex:
            self.logger.error(f"Unexpected error executing command: {command} -> {ex}")
            raise RuntimeError(f"Command execution error: {ex}")