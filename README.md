# 🇮🇹 Italian Anki Decks

This project contains structured Anki decks for learning Italian, organized by CEFR levels (A1, A2, etc.). Each deck is built from a JSON file and converted to `.apkg` using [`genanki`](https://github.com/kerrickstaley/genanki).

## 🧱 JSON Format & Schema

Each JSON file must contain a top-level object with a `cards` array.

### Basic Card

```json
{
  "model": "basic",
  "front": "🍎 <b>mela</b>",
  "back": "Meaning: apple<br>Example: Mangio una mela = I eat an apple",
  "tags": ["a1", "noun", "sostantivo"]
}
```

### Cloze Card

```json
{
  "model": "cloze",
  "front": "Io {{c1::mangio}} una mela.",
  "back": "Verb: mangiare (to eat)<br>Translation: I eat an apple.",
  "tags": ["a1", "verb", "presente", "cloze"]
}
```

## 🏷 Tagging Guidelines

- CEFR Level: `a1`, `a2`, etc.
- Part of Speech: `verb`, `noun`, `adjective`, `expression`
- Category Tags: `presente`, `fare`, `idiom`, `antonym`, etc.
- Format Tags: `cloze` for cloze-deletion cards

## 🚀 Build All Decks

```bash
python generate.py --all
```
