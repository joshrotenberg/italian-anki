#!/usr/bin/env python3
import glob, json, os, sys

# Script to fix tags for all decks in decks/a1/
for path in glob.glob('decks/a1/*.json'):
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    # Set tags to [level, topic]
    for card in data.get('cards', []):
        card['tags'] = [level, topic]
    # Write back the file
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Tags fixed for all decks in decks/a1/")