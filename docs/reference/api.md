# API Reference

This reference guide provides information about the internal API of the Italian Anki Decks project. This is primarily useful for developers who want to extend or modify the project.

## Generate Module

The `generate.py` module contains functions for generating Anki decks from TOML files.

### Main Functions

#### `generate_deck(deck_file, output_dir, version)`

Generates an Anki deck from a single TOML file.

**Parameters:**
- `deck_file` (str): Path to the TOML deck file
- `output_dir` (str): Directory where the generated deck will be saved
- `version` (str): Version string to include in the deck name

**Returns:**
- `str`: Path to the generated .apkg file

#### `generate_level_deck(level, deck_files, output_dir, version)`

Generates a single Anki deck from multiple TOML files of the same level.

**Parameters:**
- `level` (str): Level name (a1, a2, b1, basic)
- `deck_files` (list): List of paths to TOML deck files
- `output_dir` (str): Directory where the generated deck will be saved
- `version` (str): Version string to include in the deck name

**Returns:**
- `str`: Path to the generated .apkg file

#### `generate_uber_deck(deck_files, output_dir, version)`

Generates a single Anki deck from all TOML files across all levels.

**Parameters:**
- `deck_files` (list): List of paths to TOML deck files
- `output_dir` (str): Directory where the generated deck will be saved
- `version` (str): Version string to include in the deck name

**Returns:**
- `str`: Path to the generated .apkg file

#### `generate_chunk_decks(level, deck_files, chunk_size, output_dir, version)`

Generates multiple Anki decks, each containing a chunk of TOML files.

**Parameters:**
- `level` (str): Level name (a1, a2, b1, basic)
- `deck_files` (list): List of paths to TOML deck files
- `chunk_size` (int): Number of files per chunk
- `output_dir` (str): Directory where the generated decks will be saved
- `version` (str): Version string to include in the deck names

**Returns:**
- `list`: List of paths to the generated .apkg files

### Helper Functions

#### `load_deck_file(deck_file)`

Loads a TOML deck file.

**Parameters:**
- `deck_file` (str): Path to the TOML deck file

**Returns:**
- `dict`: Parsed TOML data

#### `create_anki_deck(deck_name, deck_id=None)`

Creates an Anki deck object.

**Parameters:**
- `deck_name` (str): Name of the deck
- `deck_id` (int, optional): ID for the deck

**Returns:**
- `genanki.Deck`: Anki deck object

#### `create_anki_package(deck, output_file)`

Creates an Anki package file (.apkg) from a deck.

**Parameters:**
- `deck` (genanki.Deck): Anki deck object
- `output_file` (str): Path where the .apkg file will be saved

**Returns:**
- `str`: Path to the generated .apkg file

## Validate Module

The `validate.py` module contains functions for validating TOML deck files.

### Main Functions

#### `validate_file(file_path)`

Validates a single TOML deck file.

**Parameters:**
- `file_path` (str): Path to the TOML deck file

**Returns:**
- `bool`: True if the file is valid, False otherwise

#### `validate_directory(directory_path)`

Validates all TOML files in a directory.

**Parameters:**
- `directory_path` (str): Path to the directory containing TOML files

**Returns:**
- `bool`: True if all files are valid, False otherwise

### Validation Functions

#### `validate_deck_name(deck_data, file_path)`

Validates the deck name in a TOML deck file.

**Parameters:**
- `deck_data` (dict): Parsed TOML data
- `file_path` (str): Path to the TOML deck file

**Returns:**
- `bool`: True if the deck name is valid, False otherwise

#### `validate_notes(notes, file_path)`

Validates the notes in a TOML deck file.

**Parameters:**
- `notes` (list): List of notes from the TOML data
- `file_path` (str): Path to the TOML deck file

**Returns:**
- `bool`: True if all notes are valid, False otherwise

#### `validate_tags(tags, file_path)`

Validates the tags in a note.

**Parameters:**
- `tags` (list): List of tags from a note
- `file_path` (str): Path to the TOML deck file

**Returns:**
- `bool`: True if the tags are valid, False otherwise

## Models

The project defines two Anki note models:

### Basic Model

A basic front/back card model.

**Fields:**
- Front
- Back

**Templates:**
- Card 1:
  - Front: `{{Front}}`
  - Back: `{{FrontSide}}<hr id="answer">{{Back}}`

### Cloze Model

A cloze deletion card model.

**Fields:**
- Text

**Templates:**
- Cloze:
  - Front: `{{cloze:Text}}`
  - Back: `{{cloze:Text}}`

## Utilities

### Stable ID Generation

The project uses MD5 hashing to generate stable IDs for decks and models:

```python
def stable_id(name: str) -> int:
    """Generate a stable ID from a name using MD5 hashing."""
    digest = hashlib.md5(name.encode('utf-8'), usedforsecurity=False).hexdigest()
    return int(digest[:10], 16)
```

This ensures that decks and models have consistent IDs across builds, which is important for Anki's synchronization.

### Markdown to HTML Conversion

The project converts Markdown to HTML for card content:

```python
def markdown_to_html(text: str) -> str:
    """Convert Markdown text to HTML."""
    return markdown.markdown(text)
```

This allows deck authors to use Markdown formatting in their card content, which is then converted to HTML for display in Anki.

## Extension Points

If you want to extend the project, here are some key points to consider:

### Adding a New Card Model

To add a new card model:

1. Define the model in `generate.py`:
   ```python
   MY_MODEL = genanki.Model(
       stable_id('my-model'),
       'My Model',
       fields=[
           {'name': 'Field1'},
           {'name': 'Field2'},
       ],
       templates=[
           {
               'name': 'Card 1',
               'qfmt': '{{Field1}}',
               'afmt': '{{FrontSide}}<hr id="answer">{{Field2}}',
           },
       ],
       css=CSS,
   )
   ```

2. Update the `create_note` function to handle the new model type.

### Adding a New Build Mode

To add a new build mode:

1. Add a new function in `generate.py` that implements the build logic.
2. Update the `main` function to handle the new mode.
3. Update the command-line argument parser to accept the new mode.

### Adding Validation Rules

To add new validation rules:

1. Add a new validation function in `validate.py`.
2. Update the appropriate validation function to call your new function.