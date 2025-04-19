import genanki
import json
import os
from pathlib import Path

# Model IDs should be consistent across runs
BASIC_MODEL_ID = 1607392319
CLOZE_MODEL_ID = 1378438319

# Basic front/back model
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

# Cloze deletion model
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

def generate_deck(json_path: Path, output_dir: Path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    deck_name = data['name']
    deck_id = abs(hash(deck_name)) % (10 ** 10)
    deck = genanki.Deck(deck_id, deck_name)

    for card in data['cards']:
        model_type = card.get("model", "basic")

        if model_type == "cloze":
            note = genanki.Note(
                model=CLOZE_MODEL,
                fields=[card['front'], card.get('back', '')],
                tags=card.get('tags', [])
            )
        else:
            note = genanki.Note(
                model=BASIC_MODEL,
                fields=[card['front'], card['back']],
                tags=card.get('tags', [])
            )

        deck.add_note(note)

    out_file = output_dir / f"{deck_name.replace('::', '_')}.apkg"
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ Deck written to {out_file}")

if __name__ == "__main__":
    decks_dir = Path("decks")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for json_file in decks_dir.glob("*.json"):
        generate_deck(json_file, output_dir)
