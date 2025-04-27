#!/usr/bin/env python3
"""
html_to_markdown.py.

Converts HTML formatting in TOML deck files to Markdown.
Specifically, converts:
- <br> tags to newlines
- <b>...</b> tags to **...**

Usage:
  python html_to_markdown.py                  # Convert all TOML files
  python html_to_markdown.py --path <path>    # Convert a specific file or directory
  python html_to_markdown.py --dry-run        # Show what would be changed without making changes
"""
import argparse
import glob
import os
import re
import sys
from typing import List, Optional, Tuple

# Import appropriate TOML library based on Python version
if sys.version_info >= (3, 11):
    import tomllib

    import tomli_w
else:
    import tomli as tomllib
    import tomli_w


def convert_html_to_markdown(text: str) -> str:
    """
    Convert HTML formatting to Markdown.

    Args:
        text: Text containing HTML formatting

    Returns:
        Text with HTML converted to Markdown
    """
    # Convert <br> to newline
    text = text.replace("<br>", "\n")

    # Convert <b>...</b> to **...**
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)

    return text


def process_toml_file(path: str, dry_run: bool = False) -> Tuple[int, int]:
    """
    Process a single TOML file, converting HTML to Markdown.

    Args:
        path: Path to the TOML file
        dry_run: If True, don't actually write changes

    Returns:
        Tuple of (number of fields changed, number of notes processed)
    """
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)

        changed_fields = 0
        processed_notes = 0

        # Process each note
        for note in data.get("notes", []):
            processed_notes += 1

            # Process fields
            if "fields" in note:
                for i, field in enumerate(note["fields"]):
                    converted = convert_html_to_markdown(field)
                    if converted != field:
                        if dry_run:
                            note_info = f"[note {processed_notes}, field {i + 1}]"
                            print(f"Would convert in {path} {note_info}:")
                            print(f"  From: {field[:80]}...")
                            print(f"  To:   {converted[:80]}...")
                        else:
                            note["fields"][i] = converted
                        changed_fields += 1

            # Process back field if present
            if "back" in note:
                back = note["back"]
                converted = convert_html_to_markdown(back)
                if converted != back:
                    if dry_run:
                        print(f"Would convert in {path} [note {processed_notes}, back field]:")
                        print(f"  From: {back}")
                        print(f"  To:   {converted}")
                    else:
                        note["back"] = converted
                    changed_fields += 1

        # Write changes if not dry run and there were changes
        if changed_fields > 0 and not dry_run:
            with open(path, "wb") as f:
                tomli_w.dump(data, f)
            print(f"Converted {changed_fields} fields in {path}")

        return changed_fields, processed_notes

    except Exception as e:
        print(f"Error processing {path}: {str(e)}")
        return 0, 0


def find_toml_files(path: Optional[str] = None) -> List[str]:
    """
    Find all TOML files to process.

    Args:
        path: Optional path to a specific file or directory

    Returns:
        List of file paths to process
    """
    if path:
        if os.path.isfile(path) and path.endswith(".toml"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.toml"))
        else:
            return glob.glob(os.path.join(path, "**/*.toml"), recursive=True)
    else:
        return glob.glob("decks/**/*.toml", recursive=True)


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown in TOML deck files")
    parser.add_argument("--path", help="Path to a specific file or directory to process")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    args = parser.parse_args()

    files = find_toml_files(args.path)
    if not files:
        print("No TOML files found to process")
        return 0

    action = "Checking" if args.dry_run else "Converting"
    print(f"{action} HTML to Markdown in {len(files)} files...")

    total_changed = 0
    total_processed = 0

    for path in files:
        changed, processed = process_toml_file(path, args.dry_run)
        total_changed += changed
        total_processed += processed

    if args.dry_run:
        print(f"Would convert {total_changed} fields in {len(files)} files")
    else:
        print(f"Converted {total_changed} fields in {len(files)} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
