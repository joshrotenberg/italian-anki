#!/usr/bin/env python3
"""Test script to verify that the generate.py script can handle the "basic" level.

This script tests that the generate.py script can handle the "basic" level
and that existing functionality for other levels is not broken.
"""
import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize("level", ["basic", "a1"])
def test_level(level):
    """
    Test the generate.py script with a specific level.

    Args:
        level: The level to test (e.g., "basic", "a1")

    Returns:
        True if successful, False otherwise
    """
    # Create src directory if it doesn't exist
    if not os.path.exists("src"):
        os.makedirs("src")

    # Create src/decks directory if it doesn't exist
    if not os.path.exists("src/decks"):
        os.makedirs("src/decks")

    # Create src/decks/level directory if it doesn't exist
    if not os.path.exists(f"src/decks/{level}"):
        os.makedirs(f"src/decks/{level}")

    # Create a sample TOML file in the level directory
    sample_toml_path = f"src/decks/{level}/test_sample.toml"
    with open(sample_toml_path, "w") as f:
        f.write(f"""
deck = "{level}::test_sample"
model = "basic"

[[notes]]
note_id = 10001
tags = ["{level}", "test_sample"]
fields = ["Sample front", "Sample back"]
""")

    output_dir = "src/output"

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clean up any existing output files for the level
    for filename in os.listdir(output_dir):
        if filename.startswith(f"{level}-") and filename.endswith(".apkg"):
            os.remove(os.path.join(output_dir, filename))
            print(f"Removed existing file: {filename}")

    # Run the generate.py script with the specified level
    print(f"Running generate.py with --level {level}...")
    result = subprocess.run(
        [sys.executable, "src/generate.py", "--level", level],
        capture_output=True,
        text=True,
    )

    # Print the output
    print("\nCommand output:")
    print(result.stdout)

    if result.stderr:
        print("\nErrors:")
        print(result.stderr)

    # Check if any level files were created
    assert os.path.exists(output_dir), f"Output directory '{output_dir}' does not exist."

    level_files = [
        f
        for f in os.listdir(output_dir)
        if f.startswith(f"{level}-") and f.endswith(".apkg")
    ]

    assert level_files, f"No {level} level files were created."

    print(f"\nSuccess! {len(level_files)} {level} level files were created:")
    for filename in level_files:
        print(f"  - {filename}")


# This function is no longer needed when using pytest
# def main():
#     """Run tests for both basic and a1 levels."""
#     # Test basic level
#     basic_success = test_level("basic")
#
#     # Test a1 level to ensure existing functionality is not broken
#     a1_success = test_level("a1")
#
#     # Report overall success
#     if basic_success and a1_success:
#         print(
#             "\nAll tests passed! The generate script can handle both basic and a1 levels."
#         )
#         return 0
#     else:
#         print("\nSome tests failed. Please check the output above for details.")
#         return 1
#
#
# if __name__ == "__main__":
#     sys.exit(main())
