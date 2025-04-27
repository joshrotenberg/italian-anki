#!/usr/bin/env python3
"""
json_to_toml.py.

Converts JSON deck files to TOML format.

Usage:
  python json_to_toml.py # Convert all deck files
  python json_to_toml.py <path> # Convert a specific file or directory
"""
import argparse
import glob
import json
import os
import sys
from typing import Any, Dict, List, Optional

import tomli_w  # For writing TOML files


def convert_file(json_path: str) -> str:
    """
    Convert a JSON deck file to TOML format.

    Args:
        json_path: Path to the JSON file

    Returns:
        Path to the created TOML file
    """
    # Extract level and topic from path
    level = os.path.basename(os.path.dirname(json_path))
    topic = os.path.splitext(os.path.basename(json_path))[0]

    # Create TOML file path
    toml_path = os.path.splitext(json_path)[0] + ".toml"

    # Load JSON data
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Create TOML structure
    toml_data: Dict[str, Any] = {"deck": f"{level}::{topic}", "model": "basic", "notes": []}  # Default model

    # Convert cards to notes
    for idx, card in enumerate(data.get("cards", []), start=1):
        note = {
            "note_id": 10000 + idx,  # Generate a unique ID
            "tags": card.get("tags", []),
        }

        # Set model
        model = card.get("model", "basic")
        if model != toml_data["model"]:
            note["model"] = model

        # Set fields based on model
        if model == "basic":
            note["fields"] = [card.get("front", ""), card.get("back", "")]
        else:  # cloze
            note["fields"] = [card.get("front", "")]
            if "back" in card:
                note["back"] = card["back"]

        toml_data["notes"].append(note)

    # Write TOML file
    with open(toml_path, "wb") as f:
        tomli_w.dump(toml_data, f)

    print(f"Converted {json_path} to {toml_path}")
    return toml_path


def find_json_files(path: Optional[str] = None) -> List[str]:
    """
    Find all JSON deck files to convert.

    Args:
        path: Optional path to a specific file or directory

    Returns:
        List of file paths to convert
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
        Exit code (0 for success, 1 for errors)
    """
    parser = argparse.ArgumentParser(description="Convert JSON deck files to TOML format")
    parser.add_argument("path", nargs="*", help="Path to a specific file or directory to convert")
    args = parser.parse_args()

    files = []
    if args.path:
        for path in args.path:
            files.extend(find_json_files(path))
    else:
        files = find_json_files()

    if not files:
        print("No JSON files found to convert")
        return 0

    print(f"Converting {len(files)} JSON files to TOML format...")
    converted = []
    errors = []

    for path in files:
        try:
            toml_path = convert_file(path)
            converted.append(toml_path)
        except Exception as e:
            print(f"Error converting {path}: {str(e)}")
            errors.append(path)

    print(f"Converted {len(converted)} files successfully")
    if errors:
        print(f"Failed to convert {len(errors)} files")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
