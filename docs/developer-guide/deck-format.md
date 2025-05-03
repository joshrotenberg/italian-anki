# Deck Format

This guide explains the format of the deck files used in the Italian Anki Decks project.

## TOML Format

Deck files are written in [TOML](https://toml.io/) (Tom's Obvious, Minimal Language), a config file format designed to be easy to read and write.

## File Structure

Each deck file must follow this structure:

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

### File Location and Naming

- Deck files should be placed in the appropriate level directory: `decks/<level>/`
- File names should follow the pattern: `<topic>.toml`
- Example: `decks/a1/alfabeto.toml`

### Deck Header

The deck header defines the deck name and optional default model:

```toml
deck = "<level>::<topic>"
model = "basic"  # Default model for all notes (optional)
```

- `deck`: The deck name, which must start with the level followed by "::" and the topic
- `model`: (Optional) The default model for all notes in the deck (can be overridden by individual notes)

### Notes

Each note is defined as an array item using the `[[notes]]` syntax:

```toml
[[notes]]
tags = ["<level>", "<topic>"]
fields = ["Front content", "Back content"]  # For basic model
```

#### Required Fields

- `tags`: An array with exactly 2 items:
  - First tag must be the level (a1, a2, b1, basic)
  - Second tag must be the topic (matching the filename without extension)
- `fields`: An array with the content of the card:
  - For "basic" model: At least 2 fields (front and back)
  - For "cloze" model: At least 1 field with cloze deletions

#### Optional Fields

- `model`: Override the default model for this note (either "basic" or "cloze")
- `note_id`: A unique identifier for the note (optional, will be generated if not provided)

## Card Models

The project supports two card models:

### Basic Model

Simple front/back cards:

```toml
[[notes]]
model = "basic"
tags = ["a1", "alfabeto"]
fields = [
    "Come si dice **hello** in italiano?",
    "Si dice *ciao* in italiano."
]
```

- Front: Question or prompt
- Back: Answer or explanation

### Cloze Model

Fill-in-the-blank cards:

```toml
[[notes]]
model = "cloze"
tags = ["a1", "alfabeto"]
fields = [
    "La lettera A si pronuncia come {{c1::ah}}."
]
```

- Text: Contains cloze deletions marked with `{{c1::text}}`

## Markdown Support

The project supports Markdown formatting in card content:

### Basic Formatting

- **Bold text**: `**bold**`
- *Italic text*: `*italic*`
- Lists:
  ```
  - Item 1
  - Item 2
  ```
- Links: `[text](url)`

### Example

```toml
[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "Come si dice **hello** in italiano?",
    "Si dice *ciao* in italiano.\n\nAltri saluti:\n- Buongiorno\n- Buonasera\n- Arrivederci"
]
```

## Validation

The `validate.py` script checks that each deck file follows the schema requirements:

```bash
python src/validate.py decks/<level>
```

Common validation issues:

- Tags don't follow the required structure
- Missing required fields
- Incorrect model type
- TOML syntax errors

## Examples

### Basic Example

```toml
deck = "a1::alfabeto"
model = "basic"

[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "Come si pronuncia la lettera A in italiano?",
    "La lettera A si pronuncia 'ah'."
]

[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "Come si pronuncia la lettera B in italiano?",
    "La lettera B si pronuncia 'bi'."
]
```

### Cloze Example

```toml
deck = "a1::alfabeto"
model = "cloze"

[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "La lettera A si pronuncia {{c1::ah}}."
]

[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "La lettera B si pronuncia {{c1::bi}}."
]
```

### Mixed Models Example

```toml
deck = "a1::alfabeto"
model = "basic"  # Default model

[[notes]]
tags = ["a1", "alfabeto"]
fields = [
    "Come si pronuncia la lettera A in italiano?",
    "La lettera A si pronuncia 'ah'."
]

[[notes]]
model = "cloze"  # Override default model
tags = ["a1", "alfabeto"]
fields = [
    "La lettera B si pronuncia {{c1::bi}}."
]
```