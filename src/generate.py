#!/usr/bin/env python3
"""
generate.py.

Builds Anki .apkg decks from TOML definitions under decks/<level>/*.toml.
Supports per-file, per-level, uber (all-in-one), and chunked modes.
Embeds repo VERSION into deck titles and filenames.
Supports Markdown formatting in card content.
Supports automatic discovery of deck files with the --auto-discover option.

Usage examples:
  python generate.py --level a1                     # per-file on a1
  python generate.py --all                          # per-file on all levels
  python generate.py --mode per-level               # one deck per level
  python generate.py --mode uber                    # one big deck with all cards
  python generate.py --mode chunk --chunk-size 10   # decks of 10 files each
  python generate.py --mode per-file --level a2     # per-file on a2
  python generate.py --auto-discover                # auto-discover all deck files
  python generate.py --auto-discover --mode uber    # auto-discover and build one big deck
"""
import argparse
import glob
import hashlib
import os
import sys
from typing import Any, Dict, List, Optional

import genanki
import markdown  # type: ignore

# Import appropriate TOML library based on Python version
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Ensure script runs from its own directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

# Define the path to the decks directory
# The decks directory is in the parent directory (root)
DECKS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "decks")


def read_version() -> str:
    """
    Read version from the VERSION file.

    Returns:
        Version string, or '0.0.0' if file not found
    """
    # VERSION file is in the parent directory (root)
    version_file = os.path.join(os.path.dirname(SCRIPT_DIR), "VERSION")
    try:
        with open(version_file, encoding="utf-8") as vf:
            return vf.read().strip()
    except FileNotFoundError:
        return "0.0.0"


VERSION = read_version()

# Global variable to store the current mode
CURRENT_MODE = "per-file"  # Default mode


def stable_id(name: str) -> int:
    """
    Generate a stable deck ID based on MD5 of name.

    Note: MD5 is used here for generating stable IDs, not for security purposes.

    Args:
        name: String to hash

    Returns:
        Integer ID derived from first 10 hex digits of MD5 hash
    """
    # The usedforsecurity parameter is available in Python 3.9+
    # but mypy might not recognize it, so we use type: ignore
    # This is explicitly not used for security purposes, only for generating stable IDs
    digest = hashlib.md5(name.encode("utf-8"), usedforsecurity=False).hexdigest()  # type: ignore
    return int(digest[:10], 16)


# Shared models
MODELS = {
    "basic": genanki.Model(
        stable_id("basic-model"),
        "Basic Model",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
            }
        ],
    ),
    "cloze": genanki.Model(
        stable_id("cloze-model"),
        "Cloze Model",
        fields=[{"name": "Text"}],
        templates=[
            {
                "name": "Cloze Card",
                "qfmt": "{{cloze:Text}}",
                "afmt": "{{cloze:Text}}",
            }
        ],
        model_type=genanki.Model.CLOZE,
    ),
}


def load_deck_file(file_path: str) -> Dict[str, Any]:
    """
    Load a deck file (TOML).

    Args:
        file_path: Path to the deck file

    Returns:
        Dictionary containing the deck data

    Raises:
        ValueError: If the file cannot be read or parsed
    """
    try:
        if file_path.endswith(".toml"):
            with open(file_path, "rb") as f:
                data = tomllib.load(f)

                # Convert TOML structure to match internal structure
                result: Dict[str, List[Dict[str, Any]]] = {"cards": []}

                # Extract deck and model information
                model_type = data.get("model", "basic")

                # Process notes
                for note in data.get("notes", []):
                    card = {
                        "model": note.get("model", model_type),
                        "tags": note.get("tags", []),
                        "note_id": note.get("note_id", None),
                    }

                    # Handle fields based on model type
                    fields = note.get("fields", [])
                    if card["model"] == "basic" and len(fields) >= 2:
                        card["front"] = fields[0]
                        card["back"] = fields[1]
                    elif card["model"] == "cloze" and len(fields) >= 1:
                        card["front"] = fields[0]
                        card["back"] = note.get("back", "")

                    result["cards"].append(card)

                return result
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Failed to parse file {file_path}: {str(e)}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except IOError as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")


def build_deck(level: str, topic: str, cards: List[Dict[str, Any]]) -> None:
    """
    Build and write one Anki deck.

    Args:
        level: Level tag (a1, a2, etc.)
        topic: Topic name
        cards: List of card dictionaries

    Raises:
        ValueError: If a card has an unknown model
    """
    deck_name = f"Italiano::{level}/{topic}"
    deck_id = stable_id(deck_name)
    # Don't include version in deck title to ensure Anki treats it as the same deck across versions
    deck_title = deck_name
    deck = genanki.Deck(deck_id, deck_title)

    for card in cards:
        model_key = card.get("model", "")  # Default to empty string if model is missing
        model = MODELS.get(model_key)
        if not model:
            raise ValueError(f"Unknown model '{model_key}' in card: {card}")

        # Validate that both front and back fields exist for all cards
        front = card.get("front", "")
        back = card.get("back", "")

        if not front:
            raise ValueError(f"Missing 'front' field in card: {card}")
        if not back:
            raise ValueError(f"Missing 'back' field in card: {card}")

        # Convert Markdown to HTML for front and back fields
        # Use nl2br extension to convert newlines to HTML break tags
        # This ensures that line breaks in the text (e.g., "Meaning: one\nExample: Ho uno libro")
        # are properly rendered as visual line breaks in the HTML output
        if front:
            front = markdown.markdown(front, extensions=["nl2br"])
        if back:
            back = markdown.markdown(back, extensions=["nl2br"])

        if model_key == "basic":
            fields = [front, back]
        else:  # cloze
            # For cloze cards, we only use the front field in Anki
            # but we still validate both front and back fields exist
            fields = [front]

        note = genanki.Note(model=model, fields=fields, tags=card.get("tags", []))
        deck.add_note(note)

    out_dir = os.path.join(SCRIPT_DIR, "output")
    os.makedirs(out_dir, exist_ok=True)
    # Use different filename formats based on the mode
    if CURRENT_MODE == "per-level" or CURRENT_MODE == "uber":
        # For per-level and uber modes, use a simple filename without topic
        filename = f"italian-{level}-v{VERSION}.apkg"
    else:
        # For per-file and chunk modes, include the topic to avoid overwriting
        filename = f"italian-{level}-{topic}-v{VERSION}.apkg"

    path = os.path.join(out_dir, filename)

    try:
        genanki.Package(deck).write_to_file(path)
        print(f"Wrote {path}")
    except Exception as e:
        print(f"Error writing deck to {path}: {str(e)}")


def get_deck_files(directory: str) -> List[str]:
    """
    Get all deck files (TOML) in a directory.

    Args:
        directory: Directory path

    Returns:
        List of filenames (without path)
    """
    try:
        return [f for f in sorted(os.listdir(directory)) if f.endswith(".toml")]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    except PermissionError:
        print(f"Permission denied when accessing directory: {directory}")
        return []


def discover_deck_files() -> Dict[str, List[str]]:
    """
    Automatically discover all TOML deck files recursively.

    Returns:
        Dictionary mapping level names to lists of file paths
    """
    # Get all TOML files in the decks directory and its subdirectories
    all_files = glob.glob(os.path.join(DECKS_DIR, "**/*.toml"), recursive=True)

    # Group files by level
    levels_dict: Dict[str, List[str]] = {}

    for file_path in sorted(all_files):
        # Extract level from path (e.g., "/path/to/decks/a1/file.toml" -> "a1")
        # Get the relative path from DECKS_DIR
        rel_path = os.path.relpath(file_path, DECKS_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) >= 1:  # Ensure there's at least one part (the level)
            level = parts[0]  # "a1/file.toml" -> parts = ["a1", "file.toml"]
            if level:  # Ensure level is not empty
                if level not in levels_dict:
                    levels_dict[level] = []
                levels_dict[level].append(file_path)
            else:
                print(f"Warning: Skipping file with invalid level in path: {file_path}")
        else:
            print(f"Warning: Skipping file with unexpected path structure: {file_path}")

    # Log discovered decks for debugging
    for level, files in levels_dict.items():
        print(f"Discovered {len(files)} deck files for level '{level}'")

    return levels_dict


def process_per_file_mode(
    levels: List[str], discovered_files: Optional[Dict[str, List[str]]] = None
) -> None:
    """
    Process decks in per-file mode (one deck per TOML file).

    Args:
        levels: List of levels to process
        discovered_files: Optional dictionary mapping level names to lists of file paths
    """
    for lvl in levels:
        if discovered_files and lvl in discovered_files:
            # Use discovered files
            for file_path in discovered_files[lvl]:
                topic = os.path.splitext(os.path.basename(file_path))[0]
                try:
                    data = load_deck_file(file_path)
                    cards = data.get("cards", [])
                    if cards:
                        build_deck(lvl, topic, cards)
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")
        else:
            # Use traditional directory listing
            lvl_dir = os.path.join(DECKS_DIR, lvl)
            for fname in get_deck_files(lvl_dir):
                topic = os.path.splitext(fname)[0]
                file_path = os.path.join(lvl_dir, fname)

                try:
                    data = load_deck_file(file_path)
                    cards = data.get("cards", [])
                    if cards:
                        build_deck(lvl, topic, cards)
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")


def process_per_level_mode(
    levels: List[str], discovered_files: Optional[Dict[str, List[str]]] = None
) -> None:
    """
    Process decks in per-level mode (one deck per level).

    Args:
        levels: List of levels to process
        discovered_files: Optional dictionary mapping level names to lists of file paths
    """
    for lvl in levels:
        cards = []

        if discovered_files and lvl in discovered_files:
            # Use discovered files
            for file_path in discovered_files[lvl]:
                try:
                    data = load_deck_file(file_path)
                    cards.extend(data.get("cards", []))
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")
        else:
            # Use traditional directory listing
            lvl_dir = os.path.join(DECKS_DIR, lvl)
            for fname in get_deck_files(lvl_dir):
                file_path = os.path.join(lvl_dir, fname)

                try:
                    data = load_deck_file(file_path)
                    cards.extend(data.get("cards", []))
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")

        if cards:
            build_deck(lvl, lvl, cards)


def process_uber_mode(
    levels: List[str], discovered_files: Optional[Dict[str, List[str]]] = None
) -> None:
    """
    Process decks in uber mode (one big deck with all cards).

    Args:
        levels: List of levels to process
        discovered_files: Optional dictionary mapping level names to lists of file paths
    """
    cards = []

    for lvl in levels:
        if discovered_files and lvl in discovered_files:
            # Use discovered files
            for file_path in discovered_files[lvl]:
                try:
                    data = load_deck_file(file_path)
                    cards.extend(data.get("cards", []))
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")
        else:
            # Use traditional directory listing
            lvl_dir = os.path.join(DECKS_DIR, lvl)
            for fname in get_deck_files(lvl_dir):
                file_path = os.path.join(lvl_dir, fname)

                try:
                    data = load_deck_file(file_path)
                    cards.extend(data.get("cards", []))
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")

    if cards:
        build_deck("all", "all", cards)


def process_chunk_mode(
    levels: List[str],
    chunk_size: int,
    discovered_files: Optional[Dict[str, List[str]]] = None,
) -> None:
    """
    Process decks in chunk mode (decks with a specified number of files each).

    Args:
        levels: List of levels to process
        chunk_size: Number of files per deck
        discovered_files: Optional dictionary mapping level names to lists of file paths

    Raises:
        ValueError: If chunk_size is <= 0
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")

    for lvl in levels:
        if discovered_files and lvl in discovered_files:
            # Use discovered files
            files = [os.path.basename(f) for f in discovered_files[lvl]]
            file_paths = discovered_files[lvl]
        else:
            # Use traditional directory listing
            lvl_dir = os.path.join(DECKS_DIR, lvl)
            files = get_deck_files(lvl_dir)
            file_paths = [os.path.join(lvl_dir, f) for f in files]

        for i in range(0, len(files), chunk_size):
            chunk_files = files[i : i + chunk_size]
            chunk_paths = file_paths[i : i + chunk_size]
            cards = []
            topics = []

            for j, fname in enumerate(chunk_files):
                topic = os.path.splitext(fname)[0]
                topics.append(topic)
                file_path = chunk_paths[j]

                try:
                    data = load_deck_file(file_path)
                    cards.extend(data.get("cards", []))
                except ValueError as e:
                    print(f"Error processing {file_path}: {str(e)}")

            deck_topic = "_".join(topics)
            if cards:
                build_deck(lvl, deck_topic, cards)


def main() -> int:
    """
    Execute the main script functionality.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(description="Generate Anki decks")
    parser.add_argument(
        "--level",
        choices=["a1", "a2", "b1", "basic"],
        help="legacy: per-file on a single level",
    )
    parser.add_argument(
        "--all", action="store_true", help="legacy: per-file on all levels"
    )
    parser.add_argument(
        "--mode", choices=["per-file", "per-level", "uber", "chunk"], help="build mode"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=0,
        help="number of files per deck in chunk mode",
    )
    parser.add_argument(
        "--auto-discover",
        action="store_true",
        help="automatically discover all deck files",
    )
    args = parser.parse_args()

    try:
        # Determine levels
        if args.auto_discover:
            # Use automatic discovery
            discovered_decks = discover_deck_files()
            all_levels = sorted(discovered_decks.keys())

            if args.level:
                if args.level in discovered_decks:
                    levels = [args.level]
                else:
                    print(
                        f"Warning: Level '{args.level}' not found in discovered decks"
                    )
                    levels = []
            else:
                levels = all_levels
        else:
            # Use traditional directory listing
            all_levels = sorted(
                [
                    d
                    for d in os.listdir(DECKS_DIR)
                    if os.path.isdir(os.path.join(DECKS_DIR, d))
                ]
            )

            if args.level:
                levels = [args.level]
            elif args.all or args.mode:
                levels = all_levels
            else:
                parser.error("Specify --level, --all, --mode, or --auto-discover")

        if not levels:
            print("No levels to process")
            return 0

        mode = args.mode or "per-file"

        # Set the global mode variable
        global CURRENT_MODE
        CURRENT_MODE = mode

        # Process according to mode
        discovered_files = discovered_decks if args.auto_discover else None

        if mode == "per-file":
            process_per_file_mode(levels, discovered_files)
        elif mode == "per-level":
            process_per_level_mode(levels, discovered_files)
        elif mode == "uber":
            process_uber_mode(levels, discovered_files)
        elif mode == "chunk":
            try:
                process_chunk_mode(levels, args.chunk_size, discovered_files)
            except ValueError as e:
                parser.error(str(e))
        else:
            parser.error(f"Unknown mode '{mode}'")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
