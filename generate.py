import genanki
import json
import argparse
import hashlib
from pathlib import Path

# Load styling from styles.css if it exists
styles_path = Path("styles.css")
card_style = styles_path.read_text(encoding="utf-8") if styles_path.exists() else ""

BASIC_MODEL_ID = 1607392319
CLOZE_MODEL_ID = 1378438319

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    'Italiano Basic Model',
    css=card_style,
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[{
        "name": "Basic Card",
        "qfmt": "{{Front}}",
        "afmt": "{{FrontSide}}<hr id='answer'>{{Back}}",
    }],
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    'Italiano Cloze Model',
    css=card_style,
    fields=[{"name": "Text"}, {"name": "Extra"}],
    templates=[{
        "name": "Cloze Card",
        "qfmt": "{{cloze:Text}}",
        "afmt": "{{cloze:Text}}<br><br>{{Extra}}",
    }],
    model_type=genanki.Model.CLOZE,
)

def load_cards_from_directory(directory: Path):
    cards = []
    for json_file in sorted(directory.glob("*.json")):
        print(f"📄 Reading file: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            count = len(data.get("cards", []))
            print(f"  → Loaded {count} cards from {json_file.name}")
            cards.extend(data["cards"])
    return cards

def generate_deck(deck_name: str, cards: list, output_path: Path):
    if not cards:
        print(f"⚠️ No cards found for {deck_name}. Skipping.")
        return

    digest = hashlib.md5(deck_name.encode("utf‑8")).hexdigest()
    deck_id = int(digest[:10], 16)
    deck = genanki.Deck(deck_id, deck_name)

    for card in cards:
        model_type = card.get("model", "basic")
        if model_type == "cloze":
            note = genanki.Note(
                model=CLOZE_MODEL,
                fields=[card["front"], card.get("back", "")],
                tags=card.get("tags", []),
            )
        else:
            note = genanki.Note(
                model=BASIC_MODEL,
                fields=[card["front"], card["back"]],
                tags=card.get("tags", []),
            )
        deck.add_note(note)

    output_file = output_path / f"{deck_name.replace('::', '_')}.apkg"
    genanki.Package(deck).write_to_file(output_file)
    print(f"✅ Wrote {len(deck.notes)} notes to {output_file}")

def build_all_levels(decks_base: Path, output_path: Path):
    for level_dir in sorted(decks_base.glob("*")):
        if level_dir.is_dir():
            level = level_dir.name
            print(f"📘 Building deck for level '{level}'...")
            cards = load_cards_from_directory(level_dir)
            generate_deck(f"Italiano::{level.upper()}", cards, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", "-l", help="CEFR level (e.g. a1, a2)")
    parser.add_argument("--all", action="store_true", help="Build all levels")
    args = parser.parse_args()

    decks_dir = Path("decks")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if args.all:
        build_all_levels(decks_dir, output_dir)
    elif args.level:
        level_path = decks_dir / args.level.lower()
        if not level_path.exists():
            print(f"❌ Deck folder not found: {level_path}")
            exit(1)
        cards = load_cards_from_directory(level_path)
        generate_deck(f"Italiano::{args.level.upper()}", cards, output_dir)
    else:
        print("❌ You must specify either --level or --all")
        exit(1)
