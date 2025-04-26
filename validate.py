#!/usr/bin/env python3
"""
validate.py.

Validates a JSON deck files to ensure they follow the project's schema requirements.
Specifically, checks that each card has the correct tag structure:
- Tags must be a list with exactly 2 elements
- First tag must match the level directory name (a1, a2, etc.)
- Second tag must match the filename (without extension)

Usage:
  python validate.py # Validate all deck files
  python validate.py <path> # Validate a specific file or directory
  python validate.py <path1> <path2> # Validate multiple files or directories
"""
import argparse
import glob
import json
import os
import sys
from typing import Any, Dict, List, Optional


def validate_card(card: Dict[str, Any], level: str, topic: str, path: str, idx: int) -> List[str]:
    """
    Validate a single card's tags.

    Args:
        card: The card data dictionary
        level: The expected level tag (a1, a2, etc.)
        topic: The expected topic tag
        path: The file path (for error messages)
        idx: The card index (for error messages)

    Returns:
        List of error messages, empty if no errors
    """
    errors = []
    tags = card.get("tags")

    if not (isinstance(tags, list) and len(tags) == 2):
        errors.append(f"ERR {path} [card {idx}]: tags should be 2-element list, got {tags}")
    elif tags[0] != level:
        errors.append(f"ERR {path} [card {idx}]: first tag must be '{level}', got '{tags[0]}'")
    elif tags[1] != topic:
        errors.append(f"ERR {path} [card {idx}]: second tag must be '{topic}', got '{tags[1]}'")

    return errors


def validate_file(path: str) -> List[str]:
    """
    Validate all cards in a deck file.

    Args:
        path: Path to the JSON deck file

    Returns:
        List of error messages, empty if no errors
    """
    errors = []
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"ERR {path}: Failed to parse JSON: {str(e)}"]
    except FileNotFoundError:
        return [f"ERR {path}: File not found"]

    for idx, card in enumerate(data.get("cards", []), start=1):
        card_errors = validate_card(card, level, topic, path, idx)
        errors.extend(card_errors)

    return errors


def find_deck_files(path: Optional[str] = None) -> List[str]:
    """
    Find all deck files to validate.

    Args:
        path: Optional path to a specific file or directory

    Returns:
        List of file paths to validate
    """
    if path:
        if os.path.isfile(path) and path.endswith(".json"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.json"))
        else:
            return glob.glob(os.path.join(path, "**/*.json"), recursive=True)
    else:
        return glob.glob("decks/*/*.json")


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, 1 for validation errors)
    """
    parser = argparse.ArgumentParser(description="Validate deck JSON files")
    parser.add_argument("path", nargs="*", help="Path to a specific file or directory to validate")
    args = parser.parse_args()

    files = []
    if args.path:
        for path in args.path:
            files.extend(find_deck_files(path))
    else:
        files = find_deck_files()

    if not files:
        print("No JSON files found to validate")
        return 0

    print(f"Validating {len(files)} JSON files...")
    all_errors = []

    for path in files:
        errors = validate_file(path)
        all_errors.extend(errors)

    for error in all_errors:
        print(error)

    if all_errors:
        print(f"Found {len(all_errors)} errors in {len(files)} files")
        return 1
    else:
        print(f"All {len(files)} files passed validation")
        return 0


if __name__ == "__main__":
    sys.exit(main())
