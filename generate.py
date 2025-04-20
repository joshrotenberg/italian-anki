import genanki
import json
import argparse
from pathlib import Path

# Models
BASIC_MODEL_ID = 1607392319
CLOZE_MODEL_ID = 1378438319

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    'Italiano Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Basic Card',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    'Italiano Cloze Model',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
    ],
    templates=[
        {
            'name': 'Cloze Card',
            'qfmt': '{{cloze:Text}}',
            'afmt': '{{cloze:Text}}<br><br>{{Extra}}',
        },
    ],
    model_type=genanki.Model.CLOZE,
)

def load_cards_from_directory(directory: Path):
    cards = []
    for json_file in sorted(directory.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            cards.extend(data["cards"])
    return cards

def generate_deck(deck_name: str, cards: list, output_path: Path):
    deck_id = abs(hash(deck_name)) % (10 ** 10)
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

    safe_name = deck_name.replace("::", "_")
    output_file = output_path / f"{safe_name}.apkg"
    genanki.Package(deck).write_to_file(output_file)
    print(f"✅ Deck written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", "-l", required=True, help="CEFR level (e.g. a1, a2)")
    args = parser.parse_args()

    level = args.level.lower()
    decks_dir = Path(f"decks/{level}")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if not decks_dir.exists():
        print(f"❌ Deck folder not found: {decks_dir}")
        exit(1)

    cards = load_cards_from_directory(decks_dir)
    generate_deck(f"Italiano::{level.upper()}", cards, output_dir)
