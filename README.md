# 🇮🇹 Italian Anki Deck: A1 Vocabulary & Grammar

This repository contains a structured and taggable set of Anki decks for Italian learners, starting at the A1 level.

## 📁 Structure

Each Anki subdeck lives in:

```
decks/a1/
  ├── verbi_presente.json
  ├── aggettivi.json
  └── ...
```

Each JSON file includes a single object with a `cards` array. Each card must include:
- a `model`: "basic" or "cloze"
- a `front`: front side HTML
- a `back`: back side HTML
- a `tags` array with `a1` and the subcategory

## 🃏 Card Models

### Basic

```json
{
  "model": "basic",
  "front": "🎨 <b>bello</b>",
  "back": "Meaning: beautiful<br>Example: Questo quadro è <b>bello</b>",
  "tags": ["a1", "aggettivi"]
}
```

### Cloze

```json
{
  "model": "cloze",
  "front": "Vado {{c1::al}} mercato.",
  "back": "<b>al</b> = a + il = to the<br>Example: Vado al mercato = I go to the market.",
  "tags": ["a1", "preposizioni_articolate", "cloze"]
}
```

## 🏷 Tags

Each card must have:
- `"a1"` (or `"a2"`, etc. when we expand)
- A second tag matching its subdeck: e.g. `"verbi_presente"`, `"avverbi"`, etc.

You can optionally add part-of-speech or grammar function tags like `"verb"`, `"expression"`, `"cloze"`, `"noun"`, etc.

## 🚀 Build Tools

- `generate.py` — Builds `.apkg` from folders by level (`--level a1`, `--all`)
- `validate.py` — Ensures all `.json` files are valid
- GitHub Actions workflow validates structure and builds `.apkg` from each push

## ✅ Writing Guidelines

- Use simple vocabulary and grammar (A1 level)
- One concept per card
- Use natural, full-sentence examples in Italian
- Use emojis, bold, and line breaks to aid readability
- Avoid duplicate examples or overloading the same term

## 🤖 Model Integration Tips

If you're using a new model like `o3-mini-high`, read all `*.json` files and continue adding new cards in the same format. You can regenerate any file with a complete overwrite — we do not merge. All card text must be realistic and well-formed.