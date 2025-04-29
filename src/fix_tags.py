#!/usr/bin/env python3
"""
fix_tags.py.

Fixes tags in TOML deck files to ensure they follow the project's schema requirements.
For each note, sets the tags to [level, topic], where:
- level is the directory name (a1, a2, etc.)
- topic is the filename (without extension)

Usage:
  python fix_tags.py                  # Fix all deck files
  python fix_tags.py --level a1       # Fix only a1 level decks
  python fix_tags.py --level a1 a2    # Fix a1 and a2 level decks
  python fix_tags.py --dry-run        # Show what would be changed without making changes
  python fix_tags.py --path decks/a1/alfabeto.toml  # Fix a specific TOML file
"""
import argparse
import glob
import os
import sys
from typing import List, Optional

# Import appropriate TOML library based on Python version
if sys.version_info >= (3, 11):
    import tomllib

    import tomli_w
else:
    import tomli as tomllib
    import tomli_w


def fix_tags_in_file(path: str, dry_run: bool = False) -> int:
    """
    Fix tags in a single deck file.

    Args:
        path: Path to the deck file (TOML)
        dry_run: If True, don't actually write changes

    Returns:
        Number of notes fixed
    """
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]

    try:
        if path.endswith(".toml"):
            with open(path, "rb") as f:
                data = tomllib.load(f)

            fixed_count = 0
            for note in data.get("notes", []):
                old_tags = note.get("tags", [])
                new_tags = [level, topic]

                if old_tags != new_tags:
                    if dry_run:
                        print(f"Would fix tags in {path}: {old_tags} -> {new_tags}")
                    else:
                        note["tags"] = new_tags
                    fixed_count += 1

            if fixed_count > 0 and not dry_run:
                try:
                    with open(path, "wb") as f:
                        tomli_w.dump(data, f)
                    print(f"Fixed {fixed_count} notes in {path}")
                except IOError as e:
                    print(f"Error writing to {path}: {str(e)}")
                    return 0
        else:
            print(f"Unsupported file format: {path}")
            return 0

    except UnicodeDecodeError as e:
        print(f"Error parsing {path}: {str(e)}")
        return 0
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0
    except Exception as e:
        print(f"Error processing {path}: {str(e)}")
        return 0

    return fixed_count


def find_deck_files(
    levels: Optional[List[str]] = None, path: Optional[str] = None
) -> List[str]:
    """
    Find all deck files to fix.

    Args:
        levels: Optional list of levels to fix (a1, a2, etc.)
        path: Optional path to a specific file or directory

    Returns:
        List of file paths to fix
    """
    if path:
        if os.path.isfile(path) and path.endswith(".toml"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.toml"))
        else:
            return glob.glob(os.path.join(path, "**/*.toml"), recursive=True)
    elif levels:
        files = []
        for level in levels:
            level_files = glob.glob(f"decks/{level}/*.toml")
            files.extend(level_files)
        return files
    else:
        return glob.glob("decks/*/*.toml")


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(description="Fix tags in deck files (TOML)")
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
        print("No deck files found to fix")
        return 0

    action = "Checking" if args.dry_run else "Fixing"
    print(f"{action} tags in {len(files)} files...")

    total_fixed = 0
    for path in files:
        fixed = fix_tags_in_file(path, args.dry_run)
        total_fixed += fixed

    if args.dry_run:
        print(f"Would fix {total_fixed} cards/notes in {len(files)} files")
    else:
        print(f"Fixed {total_fixed} cards/notes in {len(files)} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
