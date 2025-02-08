# Git Backup Utility Documentation

## Overview
This Python script creates backups of modified, untracked, and staged files in a Git repository. It preserves the directory structure and creates a timestamped ZIP archive containing all changes along with metadata about the repository state.

## Requirements
- Python 3.x
- Required packages (auto-installed if missing):
  - gitpython
  - python-dateutil

## Usage
```bash
python git_backup.py <source_git_directory> <backup_destination>
```

Example:
```bash
python git_backup.py /path/to/git/project /path/to/backup/location
```

## Features
- Automatically detects and backs up:
  - Modified files
  - Untracked files
  - Staged files
- Preserves directory structure
- Creates timestamped ZIP archives
- Generates backup metadata
- Auto-installs required dependencies

## Function Documentation

### check_and_install_packages()
Checks for required Python packages and installs them if missing.
- Verifies presence of 'gitpython' and 'python-dateutil'
- Uses pip to install missing packages
- Imports required modules after installation

### validate_paths(source_dir, backup_dir)
Validates source and backup directory paths.
- Parameters:
  - source_dir: Path to Git repository
  - backup_dir: Path for backup storage
- Returns:
  - Tuple containing (repo, source_path, backup_path)
- Checks:
  - Source directory existence
  - Valid Git repository
  - Creates backup directory if missing

### get_changed_files(repo)
Retrieves lists of modified, untracked, and staged files from the repository.
- Parameters:
  - repo: GitPython repository object
- Returns:
  - Tuple containing (modified_files, untracked_files, staged_files)

### create_backup_info(backup_path, repo, modified_files, untracked_files, staged_files)
Generates a metadata file containing repository and backup information.
- Creates backup_info.txt with:
  - Timestamp
  - Repository URL
  - Current branch
  - Last commit details
  - Lists of modified, untracked, and staged files

### copy_files(files, source_path, backup_path)
Copies files while maintaining directory structure.
- Parameters:
  - files: List of files to copy
  - source_path: Source directory path
  - backup_path: Backup directory path
- Preserves file metadata using shutil.copy2

### create_zip_backup(backup_dir, backup_name)
Creates a ZIP archive of the backup and removes the original directory.
- Parameters:
  - backup_dir: Directory containing backups
  - backup_name: Name of backup to compress
- Returns:
  - Name of created ZIP file
- Uses timestamp format: YYYYMMDD_HHMM.zip

## Output Structure
The backup is created as a ZIP file with the following structure:
```
YYYYMMDD_HHMM.zip
├── backup_info.txt
└── [preserved directory structure]
    └── [backed up files]
```

## Error Handling
- Validates command-line arguments
- Checks for valid Git repository
- Verifies source directory existence
- Creates backup directories as needed
- Provides descriptive error messages

## Exit Codes
- 0: Successful execution
- 1: Error occurred (with error message)
  - Invalid arguments
  - Invalid paths
  - Package installation failure
  - Backup creation failure

## Notes
- The script automatically handles nested directories
- Existing backup directories are preserved
- Each backup is isolated in its own timestamped ZIP file
- Repository state is captured in backup_info.txt
- Required packages are automatically installed if missing