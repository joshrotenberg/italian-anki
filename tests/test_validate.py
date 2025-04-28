#!/usr/bin/env python3
"""Test script to verify that validate.py can handle multiple path arguments."""
import os
import subprocess  # nosec B404 - Used for testing validate.py
import sys


def test_multiple_paths():
    """
    Test validate.py with multiple path arguments.

    Verifies that the validate.py script can correctly process
    multiple path arguments provided on the command line.
    """
    print("Testing validate.py with multiple path arguments...")

    # Get absolute path to validate.py
    validate_script = os.path.abspath("validate.py")

    # Verify paths exist
    for path in ["decks/a1", "decks/a2"]:
        if not os.path.exists(path):
            print(f"Error: Path does not exist: {path}")
            return False

    # Run validate.py with two path arguments
    # nosec B603 B607 - Using sys.executable and validated paths
    result = subprocess.run(
        [sys.executable, validate_script, "decks/a1", "decks/a2"],
        capture_output=True,
        text=True,
    )

    # Print the output
    print("Exit code:", result.returncode)
    print("Standard output:")
    print(result.stdout)

    if result.stderr:
        print("Standard error:")
        print(result.stderr)

    # Check if the command was successful
    if result.returncode == 0:
        print("Test passed: validate.py successfully processed multiple path arguments.")
        return True
    else:
        print("Test failed: validate.py could not process multiple path arguments.")
        return False


if __name__ == "__main__":
    success = test_multiple_paths()
    sys.exit(0 if success else 1)
