# 🇮🇹 Italian Anki Decks

This project contains structured Anki decks for learning Italian, organized by CEFR levels (A1, A2, etc.). Each deck is built from a JSON file and converted to `.apkg` using [`genanki`](https://github.com/kerrickstaley/genanki).

## 📦 Project Structure

```
italian-anki/
├── decks/
│   └── a1/
│       ├── verbi_presente.json
│       ├── idiomi.json
│       ├── fare.json
├── output/
├── generate.py
└── README.md
```

## 🧱 JSON Format & Schema

Each file in `decks/a1/` should look like:

```json
{
  "cards": [
    {
      "model": "basic",
      "front": "🍎 <b>mela</b>",
      "back": "Meaning: apple<br>Example: Mangio una mela = I eat an apple",
      "tags": ["a1", "noun", "sostantivo"]
    },
    {
      "model": "basic",
      "front": "🗣 <b>parlare</b>",
      "back": "Definition: to speak<br>Present tense:<br><b>io parlo</b><br>Example: Io parlo italiano = I speak Italian",
      "tags": ["a1", "verb", "presente"]
    },
    {
      "model": "cloze",
      "front": "Io {{c1::mangio}} una mela.",
      "back": "Verb: mangiare (to eat)<br>Translation: I eat an apple.",
      "tags": ["a1", "verb", "presente", "cloze"]
    }
  ]
}
```

## 🚀 Build Decks

```bash
python generate.py --level a1
```
