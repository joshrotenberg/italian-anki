# 🧠 Contributing to the Italian Anki Deck (A1–B1)

We welcome expansions and new cards, especially for levels A1 and A2. This project is optimized for Anki learners who want high-quality, realistic, and well-structured decks.

## ✅ Style Guide

* Use only `"basic"` or `"cloze"` models
* Do not use placeholders — all cards must be real, useful examples
* Tag all cards with their level and category
* Tag cards with the correct level (`"a1"`, `"a2"`, `"b1"`) **and** the subcategory
* Each file should contain the **full content** for that category (not diffs)

## 🧱 Folder Structure

```
decks/
  └── a1/
        aggettivi.json
        verbi_presente.json
        ...
```

## 🗂 File Format

```json
{
  "cards": [
    {
      "model": "basic",
      "front": "📚 <b>libro</b>",
      "back": "Meaning: book<br>Example: Ho letto un <b>libro</b>",
      "tags": ["a1", "sostantivi"]
    }
  ]
}
```

## 🧪 Validation

You can run:

```
python validate.py
```

Or just push — CI will check and reject invalid JSON, missing tags, or bad card shapes.

## 🧠 Tips for Expanding

- Add new categories in `decks/a1/`
- Match the file and tag to the topic
- Try to get ~20 quality cards per category

## 🔄 Replacements, Not Diffs

All PRs should replace full files. This avoids merge conflicts and keeps the deck consistent.

Grazie!
