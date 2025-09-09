"""
Entry point for the Database Backup & Restore Tool.
"""

import sys
from dbbackup.cli import parse_args
from dbbackup.core.config_loader import load_config
from dbbackup.core.logger import get_logger
from dbbackup.core.backup import DatabaseBackup
from dbbackup.core.restore import DatabaseRestore
from dbbackup.core.verifier import BackupVerifier


def main():
    """
    Main function to coordinate backup, restore, and verification operations.
    """
    try:
        # Parse CLI arguments
        args = parse_args()

        # Load configuration
        config = load_config("config/config.yaml")

        # Override config runtime options from CLI
        if args.dry_run:
            config.runtime.dry_run = True
        if args.verbose:
            config.runtime.verbose = True

        # Initialize logger
        logger = get_logger(
            name="dbbackup",
            log_dir=config.paths.log_dir,
            console=True
        )

        # Execute operations
        if args.backup:
            db_backup = DatabaseBackup(config, logger)
            db_backup.run(databases=args.databases)

        if args.restore:
            if not args.database:
                logger.error("Please specify a target database using --database")
            else:
                db_restore = DatabaseRestore(config, logger)
                db_restore.run(target_db=args.database, backup_file=args.file)

        if args.verify:
            verifier = BackupVerifier(config, logger)
            if args.all:
                verifier.run(all_files=True)
            elif args.file or args.database:
                backup_file = args.file if args.file is not None else ""
                target_db = args.database if args.database is not None else ""
                verifier.run(all_files=False, backup_file=backup_file)
            else:
                logger.error("Please specify --file or --database for verification")

        # If no operation specified
        if not any([args.backup, args.restore, args.verify]):
            logger.info("No operation specified. Use --help for usage information.")

    except Exception as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        print("Shutting down Database Backup Tool... Done.")