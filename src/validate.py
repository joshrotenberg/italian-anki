#!/usr/bin/env python3
"""
validate.py.

Validates deck files (TOML) to ensure they follow the project's schema requirements.
Specifically, checks that each note has the correct tag structure:
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
import os
import sys
from typing import List, Optional

# Import appropriate TOML library based on Python version
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def validate_file(path: str) -> List[str]:
    """
    Validate all notes in a deck file.

    Args:
        path: Path to the deck file (TOML)

    Returns:
        List of error messages, empty if no errors
    """
    errors = []
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]

    try:
        if path.endswith(".toml"):
            with open(path, "rb") as f:
                # Use tomllib for Python 3.11+, tomli for earlier versions
                data = tomllib.load(f)

            # Validate deck and model
            if "deck" not in data:
                errors.append(f"ERR {path}: Missing 'deck' field")
            elif not data["deck"].startswith(f"{level}::"):
                errors.append(f"ERR {path}: Deck name should start with '{level}::'")

            # Validate notes
            for idx, note in enumerate(data.get("notes", []), start=1):
                if "tags" not in note:
                    errors.append(f"ERR {path} [note {idx}]: Missing 'tags' field")
                elif not isinstance(note["tags"], list):
                    errors.append(f"ERR {path} [note {idx}]: 'tags' should be a list")
                elif len(note["tags"]) < 2:
                    errors.append(
                        f"ERR {path} [note {idx}]: 'tags' should have at least 2 elements"
                    )
                elif note["tags"][0] != level:
                    first_tag = note["tags"][0]
                    errors.append(
                        f"ERR {path} [note {idx}]: First tag must be '{level}', got '{first_tag}'"
                    )
                elif note["tags"][1] != topic:
                    second_tag = note["tags"][1]
                    errors.append(
                        f"ERR {path} [note {idx}]: Second tag must be '{topic}', got '{second_tag}'"
                    )

                # Validate fields
                if "fields" not in note:
                    errors.append(f"ERR {path} [note {idx}]: Missing 'fields' field")
                elif not isinstance(note["fields"], list):
                    errors.append(f"ERR {path} [note {idx}]: 'fields' should be a list")
                elif len(note["fields"]) < 1:
                    errors.append(
                        f"ERR {path} [note {idx}]: 'fields' should have at least 1 element"
                    )

                # Validate model
                model = note.get("model", data.get("model", "basic"))
                if model not in ["basic", "cloze"]:
                    errors.append(f"ERR {path} [note {idx}]: Unknown model '{model}'")
                elif model == "basic" and len(note.get("fields", [])) < 2:
                    errors.append(
                        f"ERR {path} [note {idx}]: Basic model requires at least 2 fields"
                    )
        else:
            return [f"ERR {path}: Unsupported file format"]
    except UnicodeDecodeError as e:
        return [f"ERR {path}: Failed to parse file: {str(e)}"]
    except FileNotFoundError:
        return [f"ERR {path}: File not found"]
    except IOError as e:
        return [f"ERR {path}: Error reading file: {str(e)}"]

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
        if os.path.isfile(path) and path.endswith(".toml"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.toml"))
        else:
            return glob.glob(os.path.join(path, "**/*.toml"), recursive=True)
    else:
        return glob.glob("decks/*/*.toml")


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, 1 for validation errors)
    """
    parser = argparse.ArgumentParser(description="Validate deck files (TOML)")
    parser.add_argument(
        "path", nargs="*", help="Path to a specific file or directory to validate"
    )
    args = parser.parse_args()

    files = []
    if args.path:
        for path in args.path:
            files.extend(find_deck_files(path))
    else:
        files = find_deck_files()

    if not files:
        print("No deck files found to validate")
        return 0

    print(f"Validating {len(files)} deck files...")
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
