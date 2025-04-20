#!/usr/bin/env python3
"""
generate.py

Builds Anki .apkg decks from JSON definitions under decks/<level>/*.json.
Supports per-file, per-level, uber (all-in-one), and chunked modes.
Embeds repo VERSION into deck titles and filenames.
Usage examples:
  python generate.py --level a1                     # per-file on a1
  python generate.py --all                         # per-file on all levels
  python generate.py --mode per-level              # one deck per level
  python generate.py --mode uber                   # one big deck with all cards
  python generate.py --mode chunk --chunk-size 10  # decks of 10 files each
  python generate.py --mode per-file --level a2    # per-file on a2
"""
import os
import json
import argparse
import hashlib
import genanki

# Ensure script runs from its own directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

# Read version from the VERSION file
def read_version():
    version_file = os.path.join(SCRIPT_DIR, 'VERSION')
    try:
        with open(version_file, encoding='utf-8') as vf:
            return vf.read().strip()
    except FileNotFoundError:
        return '0.0.0'

VERSION = read_version()

# Stable deck ID based on MD5 of name
def stable_id(name: str) -> int:
    digest = hashlib.md5(name.encode('utf-8')).hexdigest()
    return int(digest[:10], 16)

# Shared models
MODELS = {
    'basic': genanki.Model(
        stable_id('basic-model'), 'Basic Model',
        fields=[{'name': 'Front'}, {'name': 'Back'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        }]
    ),
    'cloze': genanki.Model(
        stable_id('cloze-model'), 'Cloze Model',
        fields=[{'name': 'Text'}],
        templates=[{
            'name': 'Cloze Card',
            'qfmt': '{{cloze:Text}}',
            'afmt': '{{cloze:Text}}',
        }],
        model_type=genanki.Model.CLOZE
    )
}

# Build and write one deck
def build_deck(level: str, topic: str, cards: list):
    deck_name = f"Italiano::{level}/{topic}"
    deck_id = stable_id(deck_name)
    deck_title = f"{deck_name} v{VERSION}"
    deck = genanki.Deck(deck_id, deck_title)

    for card in cards:
        model_key = card.get('model')
        model = MODELS.get(model_key)
        if not model:
            raise ValueError(f"Unknown model '{model_key}' in card: {card}")
        fields = [card.get('front', ''), card.get('back', '')] if model_key=='basic' else [card.get('front','')]
        note = genanki.Note(model=model, fields=fields, tags=card.get('tags', []))
        deck.add_note(note)

    out_dir = os.path.join(SCRIPT_DIR, 'output')
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{level}-{topic}-v{VERSION}.apkg"
    path = os.path.join(out_dir, filename)
    genanki.Package(deck).write_to_file(path)
    print(f"Wrote {path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Anki decks')
    parser.add_argument('--level', choices=['a1','a2','b1'], help='legacy: per-file on a single level')
    parser.add_argument('--all', action='store_true', help='legacy: per-file on all levels')
    parser.add_argument('--mode', choices=['per-file','per-level','uber','chunk'], help='build mode')
    parser.add_argument('--chunk-size', type=int, default=0, help='number of files per deck in chunk mode')
    args = parser.parse_args()

    # Determine levels
    all_levels = sorted([d for d in os.listdir('decks') if os.path.isdir(os.path.join('decks', d))])
    if args.level:
        levels = [args.level]
    elif args.all or args.mode:
        levels = all_levels
    else:
        parser.error('Specify --level, --all, or --mode')

    mode = args.mode or ('per-file')

    # Per-file mode
    if mode=='per-file':
        for lvl in levels:
            lvl_dir = os.path.join('decks', lvl)
            for fname in sorted(os.listdir(lvl_dir)):
                if not fname.endswith('.json'): continue
                topic = os.path.splitext(fname)[0]
                data = json.load(open(os.path.join(lvl_dir, fname), encoding='utf-8'))
                cards = data.get('cards', [])
                if cards: build_deck(lvl, topic, cards)

    # Per-level mode
    elif mode=='per-level':
        for lvl in levels:
            cards=[]
            for fname in sorted(os.listdir(os.path.join('decks', lvl))):
                if not fname.endswith('.json'): continue
                data = json.load(open(os.path.join('decks', lvl, fname), encoding='utf-8'))
                cards.extend(data.get('cards', []))
            if cards: build_deck(lvl, lvl, cards)

    # Uber mode
    elif mode=='uber':
        cards=[]
        for lvl in levels:
            for fname in sorted(os.listdir(os.path.join('decks', lvl))):
                if not fname.endswith('.json'): continue
                data = json.load(open(os.path.join('decks', lvl, fname), encoding='utf-8'))
                cards.extend(data.get('cards', []))
        if cards: build_deck('all', 'all', cards)

    # Chunk mode
    elif mode=='chunk':
        n = args.chunk_size
        if n<=0:
            parser.error('--chunk-size must be >0 for chunk mode')
        for lvl in levels:
            files = [f for f in sorted(os.listdir(os.path.join('decks', lvl))) if f.endswith('.json')]
            for i in range(0, len(files), n):
                chunk = files[i:i+n]
                cards=[]
                topics=[]
                for fname in chunk:
                    topic = os.path.splitext(fname)[0]
                    topics.append(topic)
                    data = json.load(open(os.path.join('decks', lvl, fname), encoding='utf-8'))
                    cards.extend(data.get('cards', []))
                deck_topic = '_'.join(topics)
                if cards: build_deck(lvl, deck_topic, cards)

    else:
        parser.error(f"Unknown mode '{mode}'")
