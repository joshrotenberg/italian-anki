# Italian Anki Decks

A collection of JSON files and scripts for generating Anki decks to learn Italian at different proficiency levels.

## Repository Structure

```
italian-anki/
├── decks/
│   ├── a1/           # A1-level JSON deck files
│   └── a2/           # A2-level JSON deck files
├── generate.py       # Script to build .apkg Anki decks from JSON
├── validate.py       # Script to validate JSON deck format
├── requirements.txt  # Python dependencies
└── tests/            # Automated tests
```

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

Generate Anki decks:

```bash
# Build A1 decks:
python generate.py --level a1

# Build A2 decks (core + extras):
python generate.py --level a2

# Build all levels (if available):
python generate.py --level all
```

Validate JSON files:

```bash
# Validate A1 decks
python validate.py decks/a1

# Validate A2 decks
python validate.py decks/a2
```

## Contributing

1. Add new JSON file under `decks/<level>/`.
2. Follow naming: `<topic>.json`.
3. Each card must include:
   - `model`: `basic` or `cloze`
   - `front` and `back` HTML strings
   - `tags`: `["<level>", "<topic>"]`
4. Run validation:
   ```bash
   python validate.py decks/<level>
   ```
5. Update `generate.py` if adding new levels or modes.
6. Submit a pull request.
