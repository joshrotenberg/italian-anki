#!/usr/bin/env python3
"""Test script to verify that the generate.py script can handle the "basic" level.

This script tests that the generate.py script can handle the "basic" level
and that existing functionality for other levels is not broken.
"""
import os
import subprocess
import sys


def test_level(level):
    """
    Test the generate.py script with a specific level.

    Args:
        level: The level to test (e.g., "basic", "a1")

    Returns:
        True if successful, False otherwise
    """
    output_dir = "output"

    # Clean up any existing output files for the level
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.startswith(f"{level}-") and filename.endswith(".apkg"):
                os.remove(os.path.join(output_dir, filename))
                print(f"Removed existing file: {filename}")

    # Run the generate.py script with the specified level
    print(f"Running generate.py with --level {level}...")
    result = subprocess.run(
        [sys.executable, "generate.py", "--level", level], capture_output=True, text=True
    )

    # Print the output
    print("\nCommand output:")
    print(result.stdout)

    if result.stderr:
        print("\nErrors:")
        print(result.stderr)

    # Check if any level files were created
    if os.path.exists(output_dir):
        level_files = [
            f for f in os.listdir(output_dir) if f.startswith(f"{level}-") and f.endswith(".apkg")
        ]
        if level_files:
            print(f"\nSuccess! {len(level_files)} {level} level files were created:")
            for filename in level_files:
                print(f"  - {filename}")
            return True
        else:
            print(f"\nError: No {level} level files were created.")
            return False
    else:
        print(f"\nError: Output directory '{output_dir}' does not exist.")
        return False


def main():
    """Run tests for both basic and a1 levels."""
    # Test basic level
    basic_success = test_level("basic")

    # Test a1 level to ensure existing functionality is not broken
    a1_success = test_level("a1")

    # Report overall success
    if basic_success and a1_success:
        print("\nAll tests passed! The generate script can handle both basic and a1 levels.")
        return 0
    else:
        print("\nSome tests failed. Please check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
