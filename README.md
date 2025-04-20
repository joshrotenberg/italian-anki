# Italian Anki Deck: A1–B1 Vocabulary & Grammar

This repository contains a structured and taggable set of Anki decks for Italian learners, from **A1 through B1**.  
Each level lives under `decks/{a1,a2,b1}/` with ~20‑card JSON files per topic.

## Structure

Each Anki subdeck lives in:

```
decks/a1/
  ├── verbi_presente.json
  ├── aggettivi.json
  └── …
decks/a2/
  ├── passato_prossimo.json
  ├── imperfetto.json
  └── …
decks/b1/
  └── …
```

## Tags

Each card **must** have **exactly two** tags:
1. The level tag: `a1`, `a2`, or `b1`  
2. The topic tag: the filename without `.json` (e.g. `verbi_presente`)

## Dependencies

Install the pinned versions:

```bash
pip install -r requirements.txt
```

This brings in:

- **genanki** (for building `.apkg` files)  
- **jsonschema** (for JSON schema validation)  

## Validation

Run:

```bash
python validate.py
```

- Checks JSON structure against `deck.schema.json`  
- Enforces the two‑tag convention (level + topic)  
- Exits nonzero on any error  

CI automatically invokes this on every push/PR touching `decks/**/*.json`.

## Building Decks

To generate `.apkg` files:

```bash
# Build only A1 decks
python generate.py --level a1

# Build all levels (A1–B1)
python generate.py --all
```

Outputs appear in `output/`.

## Releases

We publish `.apkg` files automatically on GitHub releases via CI.  
Tag a new version (e.g. `v1.1.0`) to trigger a release with all decks for download.

## Helpers

- **fix_tags.py**: auto‑resets all card tags to `[level, topic]` for decks in any `decks/<level>/` folder.  
- **requirements.txt**: pins dependencies for consistent CI builds.

---
