# 🇮🇹 Contributing to the Italian Anki Deck Project

This project maintains high-quality, manually curated Anki decks for Italian language learning, beginning with the A1 level.

## 🧠 Deck Philosophy

Each card should:
- Represent **one clear idea** or concept
- Include a **natural Italian example sentence**
- Follow a consistent format across all categories
- Be useful for real-world conversation or comprehension

## 🗂️ Project Structure

```
italian-anki/
├── decks/
│   ├── a1/
│   │   ├── verbi_presente.json
│   │   ├── preposizioni.json
│   │   └── ...
│   └── a2/            ← New levels follow the same layout
├── generate.py        ← Build the `.apkg` deck
├── validate.py        ← Validates structure and formatting
├── output/            ← Build artifacts
```

## 🃏 Card Format

Each `.json` file contains:

```json
{
  "cards": [
    {
      "model": "basic" | "cloze",
      "front": "Front of the card",
      "back": "Back of the card",
      "tags": ["a1", "verb", "presente"]
    }
  ]
}
```

### 🔤 Card Models
- `"basic"` for standard front/back cards
- `"cloze"` for fill-in-the-blank using `{{c1::word}}`

### 🏷️ Tagging Conventions
- `a1`, `a2`, etc.
- One tag for part of speech or grammar (e.g., `verb`, `noun`, `expression`)
- Optionally: specific tense or category (e.g., `presente`, `articolata`)

## ✅ Style Guidelines

- Examples must be **grammatically correct**
- Use **Italian for examples**, **English for definitions**
- Add emoji in the front if helpful
- Capitalize proper names and punctuate sentences
- No duplicate cards (deduped by `model + front`)

## 🆕 Adding New Content

To add A2 or other level decks:
1. Create a new folder: `decks/a2/`
2. Follow the same category layout (one `.json` file per topic)
3. Tag all cards with `"a2"` and relevant grammar tags
4. Run `generate.py --level a2` to build your deck
5. Optionally validate: `python validate.py`

## 💬 Questions or Suggestions?

Open an issue or pull request on GitHub. Contributions are welcome!