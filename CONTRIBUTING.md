# Contributing

Thanks for helping improve the Italian‑Anki project! Please follow these guidelines:

## 1. Add or update a deck

1. Place your JSON file in the correct folder: `decks/<level>/` (e.g., `decks/a1/` or `decks/a2/`).
2. Name it `<topic>.json` (e.g., `vocab_alimentari.json`).
3. Follow the JSON schema:
   ```json
   {
     "cards": [
       {
         "model": "basic" | "cloze",
         "front": "...",
         "back": "...",
         "tags": ["<level>", "<topic>"]
       }
     ]
   }
   ```
4. Validate your file:
   ```bash
   python validate.py decks/<level>
   ```

## 2. Generate Anki decks

Use `generate.py` to build `.apkg` files:
```bash
python generate.py --level <level>
# e.g.
python generate.py --level a1
python generate.py --level a2
python generate.py --level all
```

## 3. Run tests

Ensure everything passes:
```bash
pytest
```

## 4. Update scripts

If you add new levels or change output modes, update `generate.py` accordingly.

Once all checks pass, submit a pull request. Thank you! 🎉
