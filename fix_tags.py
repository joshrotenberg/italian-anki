#!/usr/bin/env python3
"""
fix_tags.py.

Fixes tags in JSON deck files to ensure they follow the project's schema requirements.
For each card, sets the tags to [level, topic], where:
- level is the directory name (a1, a2, etc.)
- topic is the filename (without extension)

Usage:
  python fix_tags.py                  # Fix all deck files
  python fix_tags.py --level a1       # Fix only a1 level decks
  python fix_tags.py --level a1 a2    # Fix a1 and a2 level decks
  python fix_tags.py --dry-run        # Show what would be changed without making changes
  python fix_tags.py --path decks/a1/alfabeto.json  # Fix a specific file
"""
import argparse
import glob
import json
import os
import sys
from typing import List, Optional


def fix_tags_in_file(path: str, dry_run: bool = False) -> int:
    """
    Fix tags in a single deck file.

    Args:
        path: Path to the JSON deck file
        dry_run: If True, don't actually write changes

    Returns:
        Number of cards fixed
    """
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error parsing {path}: {str(e)}")
        return 0
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0

    fixed_count = 0
    for card in data.get("cards", []):
        old_tags = card.get("tags", [])
        new_tags = [level, topic]

        if old_tags != new_tags:
            if dry_run:
                print(f"Would fix tags in {path}: {old_tags} -> {new_tags}")
            else:
                card["tags"] = new_tags
            fixed_count += 1

    if fixed_count > 0 and not dry_run:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Fixed {fixed_count} cards in {path}")
        except IOError as e:
            print(f"Error writing to {path}: {str(e)}")
            return 0

    return fixed_count


def find_deck_files(levels: Optional[List[str]] = None, path: Optional[str] = None) -> List[str]:
    """
    Find all deck files to fix.

    Args:
        levels: Optional list of levels to fix (a1, a2, etc.)
        path: Optional path to a specific file or directory

    Returns:
        List of file paths to fix
    """
    if path:
        if os.path.isfile(path) and path.endswith(".json"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.json"))
        else:
            return glob.glob(os.path.join(path, "**/*.json"), recursive=True)
    elif levels:
        files = []
        for level in levels:
            level_files = glob.glob(f"decks/{level}/*.json")
            files.extend(level_files)
        return files
    else:
        return glob.glob("decks/*/*.json")


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(description="Fix tags in deck JSON files")
    parser.add_argument("--level", nargs="+", help="Level(s) to fix (a1, a2, etc.)")
    parser.add_argument("--path", help="Path to a specific file or directory to fix")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    args = parser.parse_args()

    files = find_deck_files(args.level, args.path)
    if not files:
        print("No JSON files found to fix")
        return 0

    action = "Checking" if args.dry_run else "Fixing"
    print(f"{action} tags in {len(files)} files...")

    total_fixed = 0
    for path in files:
        fixed = fix_tags_in_file(path, args.dry_run)
        total_fixed += fixed

    if args.dry_run:
        print(f"Would fix {total_fixed} cards in {len(files)} files")
    else:
        print(f"Fixed {total_fixed} cards in {len(files)} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
