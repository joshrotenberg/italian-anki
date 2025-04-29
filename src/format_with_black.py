#!/usr/bin/env python3
"""
format_with_black.py.

Formats Python files using Black according to the project's configuration.

Usage:
  python format_with_black.py           # Format all Python files
  python format_with_black.py <file>    # Format a specific file
  python format_with_black.py --check   # Check if files need formatting
  python format_with_black.py --diff    # Show diff of formatting changes
"""
import argparse
import os
import subprocess  # nosec B404 - Used for running Black formatter
import sys


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


def format_files(files=None, check=False, diff=False):
    """
    Format Python files using Black.

    Args:
        files: Optional list of files to format. If None, formats all Python files.
        check: If True, don't write the files back, just return the status.
        diff: If True, show the diff of what would change.

    Returns:
        Return code from Black

    Raises:
        ValueError: If any file path is invalid
    """
    cmd = ["black"]

    if check:
        cmd.append("--check")

    if diff:
        cmd.append("--diff")

    if files:
        validated_files = validate_files(files)
        cmd.extend(validated_files)
    else:
        cmd.append(".")

    print(f"Running: {' '.join(cmd)}")
    # nosec B603 - Command is constructed with validated inputs
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print("Errors:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)

    return result.returncode


def main():
    """Execute the main script functionality."""
    parser = argparse.ArgumentParser(description="Format Python files using Black")
    parser.add_argument("files", nargs="*", help="Files to format")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Don't write the files back, return the status",
    )
    parser.add_argument(
        "--diff", action="store_true", help="Show the diff of what would change"
    )

    args = parser.parse_args()

    return format_files(args.files if args.files else None, args.check, args.diff)


if __name__ == "__main__":
    sys.exit(main())
