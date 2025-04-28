# Contributing

Thanks for helping improve the Italian‑Anki project! Please follow these guidelines:

## 1. Add or update a deck

1. Place your TOML file in the correct folder: `decks/<level>/` (e.g., `decks/a1/` or `decks/a2/`).
2. Name it `<topic>.toml` (e.g., `vocab_alimentari.toml`).
3. Follow the TOML schema:
   ```toml
   deck = "<level>::<topic>"
   model = "basic"  # Default model for all notes (optional)

   [[notes]]
   tags = ["<level>", "<topic>"]
   fields = ["Front content", "Back content"]  # For basic model

   [[notes]]
   model = "cloze"  # Override default model
   tags = ["<level>", "<topic>"]
   fields = ["Text with {{c1::cloze}} deletions"]  # For cloze model
   ```
4. Validate your file:
   ```bash
   python validate.py decks/<level>
   ```

## 2. Generate Anki decks

Use `generate.py` to build `.apkg` files:
```bash
# Default mode (per-file): Creates a separate deck for each TOML file
python generate.py --level <level>
# e.g.
python generate.py --level a1
python generate.py --level a2
python generate.py --all  # All levels

# Per-level mode: Combines all TOML files of a level into a single deck
python generate.py --mode per-level --level a1

# Uber mode: Creates one big deck with all cards from all levels
python generate.py --mode uber

# Chunk mode: Creates decks with a specified number of files each
python generate.py --mode chunk --chunk-size 10 --level a1

# Auto-discover mode: Automatically discovers all deck files
python generate.py --auto-discover

# Auto-discover with uber mode: Discovers all deck files and creates one big deck
python generate.py --auto-discover --mode uber
```

## 3. Run tests

Ensure everything passes:
```bash
pytest
```

## 4. Update scripts

If you add new levels or change output modes, update `generate.py` accordingly.

## 5. Use conventional commits

This project uses [conventional commits](https://www.conventionalcommits.org/) to automate versioning and changelog generation. When making changes, format your commit messages like this:

```
<type>: <description>

[optional body]

[optional footer(s)]
```

Common types:
- `feat`: A new feature (triggers minor version bump)
- `fix`: A bug fix (triggers patch version bump)
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates, etc.

Examples:
```
feat: add new vocabulary deck for food items
fix: correct typo in alfabeto.toml
docs: update README with new usage examples
refactor: improve deck loading performance
```

Breaking changes should be noted with `!` and a footer:
```
feat!: change deck file format

BREAKING CHANGE: The deck file format has changed and requires updates to existing files.
```

Once all checks pass, submit a pull request. Thank you! 🎉
