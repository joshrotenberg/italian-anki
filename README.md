# 🇮🇹 Italian Anki Decks

This project contains structured Anki decks for learning Italian, organized by CEFR levels (A1, A2, etc.). Each deck is built from a JSON file and converted to `.apkg` using [`genanki`](https://github.com/kerrickstaley/genanki).

## 📦 Project Structure

```
italian-anki/
├── decks/              # JSON source files
│   └── a1.json
├── output/             # Exported Anki decks (.apkg)
├── generate.py         # Deck generator script
└── .github/workflows/  # Validation CI (see below)
```

## 🃏 Deck Format

- Each card uses either a **basic** or **cloze** model
- Cards support **bold**, *italic*, and 🎉 emoji for clarity and fun
- Cards are tagged with CEFR level and part of speech (e.g. `a1`, `verb`, `presente`)

## 🚀 Usage

```bash
pip install genanki
python generate.py
```

## ✅ Validation

This repo includes a GitHub Action to ensure your deck JSON files are valid before merging. See below.

## 📋 License

MIT License unless otherwise noted.
