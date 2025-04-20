## 🧱 JSON Format & Schemas by Category

Each `.json` file under `decks/a1/` should have this structure:

```json
{
  "cards": [ ... ]
}
```

Each card can be of `model` type `basic` or `cloze`. Below are examples for each major category.

---

### 🔤 Sostantivi (Nouns)

```json
{
  "model": "basic",
  "front": "🍎 <b>mela</b>",
  "back": "Meaning: apple<br>Example: Mangio una mela = I eat an apple",
  "tags": ["a1", "noun", "sostantivo"]
}
```

---

### 🧠 Modi di dire (Idioms)

```json
{
  "model": "basic",
  "front": "🐺 <b>In bocca al lupo</b>",
  "back": "Meaning: Good luck (literally: into the wolf's mouth)<br>Response: <b>Crepi!</b>",
  "tags": ["a1", "expression", "idiom"]
}
```

---

### 🛒 Espressioni con “fare”

```json
{
  "model": "basic",
  "front": "🍽 <b>Fare colazione</b>",
  "back": "Meaning: to have breakfast<br>Example: Faccio colazione alle otto.",
  "tags": ["a1", "expression", "fare"]
}
```

---

### ⚖️ Antonimi (Antonyms)

```json
{
  "model": "basic",
  "front": "🔁 <b>alto</b> ↔ <b>basso</b>",
  "back": "alto = tall/high<br>basso = short/low<br>Example: La montagna è alta, la valle è bassa.",
  "tags": ["a1", "vocabulary", "antonym"]
}
```

---

### 🗣 Verbi (Presente)

```json
{
  "model": "basic",
  "front": "🗣 <b>parlare</b>",
  "back": "Definition: to speak<br>Present tense:<br><b>io parlo</b><br>Example: Io parlo italiano = I speak Italian",
  "tags": ["a1", "verb", "presente"]
}
```

---

### 🧩 Preposizioni (Cloze format)

```json
{
  "model": "cloze",
  "front": "Vado {{c1::al}} mercato.",
  "back": "al = a + il = to the<br>Example: Vado al mercato = I go to the market.",
  "tags": ["a1", "preposition", "cloze"]
}
```

---

### 🏷 Tagging Conventions

- CEFR Level: `a1`, `a2`, etc.
- Part of Speech: `verb`, `noun`, `adjective`, `expression`
- Subcategories: `presente`, `fare`, `idiom`, `antonym`, `sostantivo`, etc.
- Format tags: `cloze` for cloze-deletion cards

## 🚀 Build Decks

```bash
python generate.py --level a1
python generate.py --all
```
