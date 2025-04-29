#!/usr/bin/env python3
"""
lint.py.

Run linting checks on the Python files in the project.
Usage:
  python lint.py           # Check all Python files
  python lint.py file.py   # Check a specific file
  python lint.py --fix     # Fix issues in all Python files
  python lint.py --fix file.py  # Fix issues in a specific file
"""
import argparse
import os
import subprocess  # nosec B404 - Used for running linting tools
import sys
from glob import glob


def validate_files(files):
    """
    Validate that files exist and are safe to use with subprocess.

    Args:
        files: List of file paths to validate

    Returns:
        List of validated file paths

    Raises:
        ValueError: If any file path is invalid or suspicious
    """
    if not files:
        return []

    validated_files = []
    for file_path in files:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise ValueError(f"File does not exist: {file_path}")

        # Convert to absolute path to avoid directory traversal
        abs_path = os.path.abspath(file_path)
        validated_files.append(abs_path)

    return validated_files


def run_command(cmd, files, description=None):
    """
    Run a command on the specified files.

    Args:
        cmd: Command to run
        files: List of files to run the command on
        description: Optional description of the action

    Returns:
        Return code (0 for success, non-zero for errors)

    Raises:
        ValueError: If any file path is invalid
    """
    if not files:
        print(f"No files to {description or 'check'} with {cmd[0]}")
        return 0

    # Validate files before passing to subprocess
    try:
        validated_files = validate_files(files)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    action = description or f"Running {cmd[0]}"
    print(f"{action} on {len(validated_files)} files...")
    # nosec B603 - Command is constructed with validated inputs
    result = subprocess.run([*cmd, *validated_files], capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return 1

    if result.stdout:
        print(result.stdout)

    print(f"{cmd[0]} {'completed' if description else 'passed'}!")
    return 0


def main():
    """Execute the main script functionality."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run linting checks on Python files")
    parser.add_argument("--fix", action="store_true", help="Fix issues automatically")
    parser.add_argument("files", nargs="*", help="Specific files to check")
    args = parser.parse_args()

    # Get Python files to check
    if args.files:
        # Check specific files provided as arguments
        files = [f for f in args.files if f.endswith(".py") and os.path.isfile(f)]
    else:
        # Find all Python files in the project
        files = glob("src/*.py") + glob("tests/*.py")

    if args.fix:
        # Fix mode: run isort to fix import order
        isort_result = run_command(["isort"], files, "Fixing import order")
        # flake8 doesn't have an auto-fix mode, so we only run it in check mode
        flake8_result = run_command(["flake8"], files)
        return isort_result or flake8_result
    else:
        # Check mode: run linters without fixing
        flake8_result = run_command(["flake8"], files)
        isort_result = run_command(["isort", "--check"], files)
        return flake8_result or isort_result


if __name__ == "__main__":
    sys.exit(main())
