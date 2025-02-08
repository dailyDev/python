#!/usr/bin/env python3

import os
import sys
import git
import shutil
import datetime
import subprocess
from pathlib import Path
import importlib.util


def check_and_install_packages():
    """Check for required packages and install if missing."""
    required_packages = {
        'gitpython': 'git',
        'python-dateutil': 'dateutil'
    }

    def install_package(package_name):
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

    for package, import_name in required_packages.items():
        if importlib.util.find_spec(import_name) is None:
            print(f"Package {package} not found. Installing...")
            install_package(package)
            print(f"Successfully installed {package}")

    # Now import required packages after ensuring they're installed
    global git
    import git


def validate_paths(source_dir, backup_dir):
    """Validate source and backup directories."""
    # Convert to Path objects for easier handling
    source_path = Path(source_dir)
    backup_path = Path(backup_dir)

    # Check if source directory exists and is a git repository
    if not source_path.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")

    try:
        repo = git.Repo(source_path)
    except git.exc.InvalidGitRepositoryError:
        raise ValueError(f"Not a valid Git repository: {source_dir}")

    # Create backup directory if it doesn't exist
    backup_path.mkdir(parents=True, exist_ok=True)

    return repo, source_path, backup_path


def get_changed_files(repo):
    """Get lists of modified, untracked, and staged files."""
    # Get modified files
    modified_files = [item.a_path for item in repo.index.diff(None)]

    # Get untracked files
    untracked_files = repo.untracked_files

    # Get staged files
    staged_files = [item.a_path for item in repo.index.diff('HEAD')]

    return modified_files, untracked_files, staged_files


def create_backup_info(backup_path, repo, modified_files, untracked_files, staged_files):
    """Create backup info file with repository details."""
    info_path = backup_path / 'backup_info.txt'

    try:
        remote_url = repo.remotes.origin.url
    except:
        remote_url = "No remote URL found"

    with open(info_path, 'w') as f:
        f.write(f"Backup created on: {datetime.datetime.now()}\n")
        f.write(f"Repository: {remote_url}\n")
        f.write(f"Current branch: {repo.active_branch.name}\n")
        f.write(f"Last commit: {repo.head.commit.hexsha} - {repo.head.commit.message}\n\n")

        f.write("Modified files:\n")
        f.write("\n".join(modified_files) + "\n\n")

        f.write("Untracked files:\n")
        f.write("\n".join(untracked_files) + "\n\n")

        f.write("Staged files:\n")
        f.write("\n".join(staged_files) + "\n")


def copy_files(files, source_path, backup_path):
    """Copy files preserving directory structure."""
    for file in files:
        source_file = source_path / file
        backup_file = backup_path / file

        # Create directory structure
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        if source_file.exists():
            shutil.copy2(source_file, backup_file)
            print(f"Backed up: {file}")


def create_zip_backup(backup_dir, backup_name):
    """Create zip file of backup and remove original directory."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"{timestamp}.zip"

    # Create zip file
    shutil.make_archive(
        str(backup_dir / timestamp),  # Path without .zip extension
        'zip',  # Archive format
        backup_dir,  # Source directory
        backup_name  # Directory to zip
    )

    # Remove the original backup directory
    shutil.rmtree(backup_dir / backup_name)

    return zip_name


def main():
    """Main function to run the backup process."""
    if len(sys.argv) != 3:
        print("Usage: python git_backup.py <source_git_directory> <backup_destination>")
        print("Example: python git_backup.py /path/to/git/project /path/to/backup/location")
        sys.exit(1)

    source_dir = sys.argv[1]
    backup_dir = sys.argv[2]

    try:
        # Check and install required packages
        check_and_install_packages()

        # Validate paths and get repo
        repo, source_path, backup_path = validate_paths(source_dir, backup_dir)

        # Get changed files
        modified_files, untracked_files, staged_files = get_changed_files(repo)

        # Check if there are any files to backup
        if not any([modified_files, untracked_files, staged_files]):
            print("No modified, untracked, or staged files found to backup.")
            sys.exit(0)

        # Create backup directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        backup_name = f"git_backup_{timestamp}"
        backup_dir_path = backup_path / backup_name
        backup_dir_path.mkdir(parents=True, exist_ok=True)

        # Copy files
        all_files = set(modified_files + untracked_files + staged_files)
        copy_files(all_files, source_path, backup_dir_path)

        # Create backup info file
        create_backup_info(backup_dir_path, repo, modified_files, untracked_files, staged_files)

        # Create zip and cleanup
        zip_name = create_zip_backup(backup_path, backup_name)
        print(f"\nBackup completed successfully: {backup_path / zip_name}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
