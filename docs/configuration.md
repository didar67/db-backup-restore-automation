# DBBackup Tool Configuration

## config/config.yaml

```yaml
# Database Backup Tool Configuration

app:
  name: DBBackupTool
  version: "1.0.0"

database:
  type: mysql         # Supported: mysql, postgresql
  host: localhost
  port: 3306
  user: backup_user
  password: secure_password
  default_databases: []  # Empty means all databases

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