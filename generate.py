import genanki
import json
import os
from pathlib import Path

MODEL_ID = 1607392319

my_model = genanki.Model(
    MODEL_ID,
    'Italiano Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
)

def generate_deck(json_path: Path, output_dir: Path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    deck_name = data['name']
    deck_id = abs(hash(deck_name)) % (10 ** 10)
    my_deck = genanki.Deck(deck_id, deck_name)

    for card in data['cards']:
        note = genanki.Note(
            model=my_model,
            fields=[card['front'], card['back']],
            tags=card.get('tags', [])
        )
        my_deck.add_note(note)

    out_file = output_dir / f"{deck_name.replace('::', '_')}.apkg"
    genanki.Package(my_deck).write_to_file(out_file)
    print(f"Deck written to {out_file}")

if __name__ == "__main__":
    decks_dir = Path("decks")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for json_file in decks_dir.glob("*.json"):
        generate_deck(json_file, output_dir)
