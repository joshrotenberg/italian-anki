#!/usr/bin/env python3
"""
generate.py.

Builds Anki .apkg decks from JSON definitions under decks/<level>/*.json.
Supports per-file, per-level, uber (all-in-one), and chunked modes.
Embeds repo VERSION into deck titles and filenames.

Usage examples:
  python generate.py --level a1                     # per-file on a1
  python generate.py --all                          # per-file on all levels
  python generate.py --mode per-level               # one deck per level
  python generate.py --mode uber                    # one big deck with all cards
  python generate.py --mode chunk --chunk-size 10   # decks of 10 files each
  python generate.py --mode per-file --level a2     # per-file on a2
"""
import argparse
import hashlib
import json
import os
import sys
from typing import Any, Dict, List

import genanki

# Ensure script runs from its own directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)


def read_version() -> str:
    """
    Read version from the VERSION file.

    Returns:
        Version string, or '0.0.0' if file not found
    """
    version_file = os.path.join(SCRIPT_DIR, "VERSION")
    try:
        with open(version_file, encoding="utf-8") as vf:
            return vf.read().strip()
    except FileNotFoundError:
        return "0.0.0"


VERSION = read_version()


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
    Load a JSON deck file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary containing the deck data

    Raises:
        ValueError: If the file cannot be read or parsed
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            return data
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Failed to parse JSON in {file_path}: {str(e)}")
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
    deck_title = f"{deck_name} v{VERSION}"
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
    filename = f"{level}-{topic}-v{VERSION}.apkg"
    path = os.path.join(out_dir, filename)

    try:
        genanki.Package(deck).write_to_file(path)
        print(f"Wrote {path}")
    except Exception as e:
        print(f"Error writing deck to {path}: {str(e)}")


def get_json_files(directory: str) -> List[str]:
    """
    Get all JSON files in a directory.

    Args:
        directory: Directory path

    Returns:
        List of JSON filenames (without path)
    """
    try:
        return [f for f in sorted(os.listdir(directory)) if f.endswith(".json")]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    except PermissionError:
        print(f"Permission denied when accessing directory: {directory}")
        return []


def process_per_file_mode(levels: List[str]) -> None:
    """
    Process decks in per-file mode (one deck per JSON file).

    Args:
        levels: List of levels to process
    """
    for lvl in levels:
        lvl_dir = os.path.join("decks", lvl)
        for fname in get_json_files(lvl_dir):
            topic = os.path.splitext(fname)[0]
            file_path = os.path.join(lvl_dir, fname)

            try:
                data = load_deck_file(file_path)
                cards = data.get("cards", [])
                if cards:
                    build_deck(lvl, topic, cards)
            except ValueError as e:
                print(f"Error processing {file_path}: {str(e)}")


def process_per_level_mode(levels: List[str]) -> None:
    """
    Process decks in per-level mode (one deck per level).

    Args:
        levels: List of levels to process
    """
    for lvl in levels:
        cards = []
        lvl_dir = os.path.join("decks", lvl)

        for fname in get_json_files(lvl_dir):
            file_path = os.path.join(lvl_dir, fname)

            try:
                data = load_deck_file(file_path)
                cards.extend(data.get("cards", []))
            except ValueError as e:
                print(f"Error processing {file_path}: {str(e)}")

        if cards:
            build_deck(lvl, lvl, cards)


def process_uber_mode(levels: List[str]) -> None:
    """
    Process decks in uber mode (one big deck with all cards).

    Args:
        levels: List of levels to process
    """
    cards = []

    for lvl in levels:
        lvl_dir = os.path.join("decks", lvl)

        for fname in get_json_files(lvl_dir):
            file_path = os.path.join(lvl_dir, fname)

            try:
                data = load_deck_file(file_path)
                cards.extend(data.get("cards", []))
            except ValueError as e:
                print(f"Error processing {file_path}: {str(e)}")

    if cards:
        build_deck("all", "all", cards)


def process_chunk_mode(levels: List[str], chunk_size: int) -> None:
    """
    Process decks in chunk mode (decks with a specified number of files each).

    Args:
        levels: List of levels to process
        chunk_size: Number of files per deck

    Raises:
        ValueError: If chunk_size is <= 0
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")

    for lvl in levels:
        lvl_dir = os.path.join("decks", lvl)
        files = get_json_files(lvl_dir)

        for i in range(0, len(files), chunk_size):
            chunk = files[i : i + chunk_size]
            cards = []
            topics = []

            for fname in chunk:
                topic = os.path.splitext(fname)[0]
                topics.append(topic)
                file_path = os.path.join(lvl_dir, fname)

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
        "--level", choices=["a1", "a2", "b1"], help="legacy: per-file on a single level"
    )
    parser.add_argument("--all", action="store_true", help="legacy: per-file on all levels")
    parser.add_argument(
        "--mode", choices=["per-file", "per-level", "uber", "chunk"], help="build mode"
    )
    parser.add_argument(
        "--chunk-size", type=int, default=0, help="number of files per deck in chunk mode"
    )
    args = parser.parse_args()

    try:
        # Determine levels
        all_levels = sorted(
            [d for d in os.listdir("decks") if os.path.isdir(os.path.join("decks", d))]
        )

        if args.level:
            levels = [args.level]
        elif args.all or args.mode:
            levels = all_levels
        else:
            parser.error("Specify --level, --all, or --mode")

        mode = args.mode or "per-file"

        # Process according to mode
        if mode == "per-file":
            process_per_file_mode(levels)
        elif mode == "per-level":
            process_per_level_mode(levels)
        elif mode == "uber":
            process_uber_mode(levels)
        elif mode == "chunk":
            try:
                process_chunk_mode(levels, args.chunk_size)
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
