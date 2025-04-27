
# Migration Plan: JSON to TOML Format with Markdown Support

## Overview

This plan outlines the steps to migrate the Italian Anki Decks project from JSON to TOML format and add support for Markdown formatting inside card fields. The migration will be done in a way that maintains backward compatibility with existing JSON files until manual verification is complete.

## 1. Technical Changes

### 1.1 Add TOML Support to `generate.py`

```python
# Add to imports
import tomli  # For Python < 3.11
# OR
import tomllib  # For Python >= 3.11

def load_deck_file(file_path: str) -> Dict[str, Any]:
    """
    Load a deck file (JSON or TOML).
    
    Args:
        file_path: Path to the deck file
        
    Returns:
        Dictionary containing the deck data
    """
    try:
        if file_path.endswith(".json"):
            with open(file_path, encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
                return data
        elif file_path.endswith(".toml"):
            with open(file_path, "rb") as f:
                # Use tomllib for Python 3.11+, tomli for earlier versions
                if sys.version_info >= (3, 11):
                    data = tomllib.load(f)
                else:
                    data = tomli.load(f)
                
                # Convert TOML structure to match JSON structure
                result = {"cards": []}
                
                # Extract deck and model information
                deck_name = data.get("deck", "")
                model_type = data.get("model", "basic")
                
                # Process notes
                for note in data.get("notes", []):
                    card = {
                        "model": note.get("model", model_type),
                        "tags": note.get("tags", []),
                        "note_id": note.get("note_id", None)
                    }
                    
                    # Handle fields based on model type
                    fields = note.get("fields", [])
                    if card["model"] == "basic" and len(fields) >= 2:
                        card["front"] = fields[0]
                        card["back"] = fields[1]
                    elif card["model"] == "cloze" and len(fields) >= 1:
                        card["front"] = fields[0]
                        card["back"] = note.get("back", "")
                    
                    result["cards"].append(card)
                
                return result
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Failed to parse file {file_path}: {str(e)}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except IOError as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")
```

### 1.2 Update `get_json_files` to Support TOML Files

```python
def get_deck_files(directory: str) -> List[str]:
    """
    Get all deck files (JSON and TOML) in a directory.
    
    Args:
        directory: Directory path
        
    Returns:
        List of filenames (without path)
    """
    try:
        return [
            f for f in sorted(os.listdir(directory)) 
            if f.endswith(".json") or f.endswith(".toml")
        ]
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []
    except PermissionError:
        print(f"Permission denied when accessing directory: {directory}")
        return []
```

### 1.3 Add Markdown Support to `build_deck`

```python
# Add to imports
import markdown

def build_deck(level: str, topic: str, cards: List[Dict[str, Any]]) -> None:
    """
    Build and write one Anki deck.
    
    Args:
        level: Level tag (a1, a2, etc.)
        topic: Topic name
        cards: List of card dictionaries
        
    Raises:
        ValueError: If a card has an unknown model
    """
    # ... existing code ...
    
    for card in cards:
        # ... existing code ...
        
        # Convert Markdown to HTML for front and back fields
        if front:
            front = markdown.markdown(front)
        if back:
            back = markdown.markdown(back)
            
        # ... rest of existing code ...
```

### 1.4 Update `validate.py` to Support TOML Files

```python
# Add to imports
import tomli  # For Python < 3.11
# OR
import tomllib  # For Python >= 3.11

def validate_file(path: str) -> List[str]:
    """
    Validate all cards in a deck file.
    
    Args:
        path: Path to the deck file
        
    Returns:
        List of error messages, empty if no errors
    """
    errors = []
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]
    
    try:
        if path.endswith(".json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                
            for idx, card in enumerate(data.get("cards", []), start=1):
                card_errors = validate_card(card, level, topic, path, idx)
                errors.extend(card_errors)
                
        elif path.endswith(".toml"):
            with open(path, "rb") as f:
                # Use tomllib for Python 3.11+, tomli for earlier versions
                if sys.version_info >= (3, 11):
                    data = tomllib.load(f)
                else:
                    data = tomli.load(f)
                
            # Validate deck and model
            if "deck" not in data:
                errors.append(f"ERR {path}: Missing 'deck' field")
            elif not data["deck"].startswith(f"{level}::"):
                errors.append(f"ERR {path}: Deck name should start with '{level}::'")
                
            # Validate notes
            for idx, note in enumerate(data.get("notes", []), start=1):
                if "tags" not in note:
                    errors.append(f"ERR {path} [note {idx}]: Missing 'tags' field")
                elif not isinstance(note["tags"], list):
                    errors.append(f"ERR {path} [note {idx}]: 'tags' should be a list")
                elif len(note["tags"]) < 2:
                    errors.append(f"ERR {path} [note {idx}]: 'tags' should have at least 2 elements")
                elif note["tags"][0] != level:
                    errors.append(f"ERR {path} [note {idx}]: First tag must be '{level}', got '{note['tags'][0]}'")
                elif note["tags"][1] != topic:
                    errors.append(f"ERR {path} [note {idx}]: Second tag must be '{topic}', got '{note['tags'][1]}'")
                
                # Validate fields
                if "fields" not in note:
                    errors.append(f"ERR {path} [note {idx}]: Missing 'fields' field")
                elif not isinstance(note["fields"], list):
                    errors.append(f"ERR {path} [note {idx}]: 'fields' should be a list")
                elif len(note["fields"]) < 1:
                    errors.append(f"ERR {path} [note {idx}]: 'fields' should have at least 1 element")
                
                # Validate model
                model = note.get("model", data.get("model", "basic"))
                if model not in ["basic", "cloze"]:
                    errors.append(f"ERR {path} [note {idx}]: Unknown model '{model}'")
                elif model == "basic" and len(note.get("fields", [])) < 2:
                    errors.append(f"ERR {path} [note {idx}]: Basic model requires at least 2 fields")
                
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"ERR {path}: Failed to parse file: {str(e)}"]
    except FileNotFoundError:
        return [f"ERR {path}: File not found"]
    
    return errors

def find_deck_files(path: Optional[str] = None) -> List[str]:
    """
    Find all deck files to validate.
    
    Args:
        path: Optional path to a specific file or directory
        
    Returns:
        List of file paths to validate
    """
    if path:
        if os.path.isfile(path) and (path.endswith(".json") or path.endswith(".toml")):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.json")) + glob.glob(os.path.join(path, "*.toml"))
        else:
            return (
                glob.glob(os.path.join(path, "**/*.json"), recursive=True) + 
                glob.glob(os.path.join(path, "**/*.toml"), recursive=True)
            )
    else:
        return glob.glob("decks/*/*.json") + glob.glob("decks/*/*.toml")
```

### 1.5 Create a Conversion Script (`json_to_toml.py`)

```python
#!/usr/bin/env python3
"""
json_to_toml.py

Converts JSON deck files to TOML format.

Usage:
  python json_to_toml.py # Convert all deck files
  python json_to_toml.py <path> # Convert a specific file or directory
"""
import argparse
import glob
import json
import os
import sys
from typing import Any, Dict, List, Optional

import tomli_w  # For writing TOML files

def convert_file(json_path: str) -> str:
    """
    Convert a JSON deck file to TOML format.
    
    Args:
        json_path: Path to the JSON file
        
    Returns:
        Path to the created TOML file
    """
    # Extract level and topic from path
    level = os.path.basename(os.path.dirname(json_path))
    topic = os.path.splitext(os.path.basename(json_path))[0]
    
    # Create TOML file path
    toml_path = os.path.splitext(json_path)[0] + ".toml"
    
    # Load JSON data
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    # Create TOML structure
    toml_data = {
        "deck": f"{level}::{topic}",
        "model": "basic",  # Default model
        "notes": []
    }
    
    # Convert cards to notes
    for idx, card in enumerate(data.get("cards", []), start=1):
        note = {
            "note_id": 10000 + idx,  # Generate a unique ID
            "tags": card.get("tags", []),
        }
        
        # Set model
        model = card.get("model", "basic")
        if model != toml_data["model"]:
            note["model"] = model
        
        # Set fields based on model
        if model == "basic":
            note["fields"] = [card.get("front", ""), card.get("back", "")]
        else:  # cloze
            note["fields"] = [card.get("front", "")]
            if "back" in card:
                note["back"] = card["back"]
        
        toml_data["notes"].append(note)
    
    # Write TOML file
    with open(toml_path, "wb") as f:
        tomli_w.dump(toml_data, f)
    
    print(f"Converted {json_path} to {toml_path}")
    return toml_path

def find_json_files(path: Optional[str] = None) -> List[str]:
    """
    Find all JSON deck files to convert.
    
    Args:
        path: Optional path to a specific file or directory
        
    Returns:
        List of file paths to convert
    """
    if path:
        if os.path.isfile(path) and path.endswith(".json"):
            return [path]
        elif os.path.isdir(path):
            return glob.glob(os.path.join(path, "*.json"))
        else:
            return glob.glob(os.path.join(path, "**/*.json"), recursive=True)
    else:
        return glob.glob("decks/*/*.json")

def main() -> int:
    """
    Execute the main script functionality.
    
    Returns:
        Exit code (0 for success, 1 for errors)
    """
    parser = argparse.ArgumentParser(description="Convert JSON deck files to TOML format")
    parser.add_argument("path", nargs="*", help="Path to a specific file or directory to convert")
    args = parser.parse_args()
    
    files = []
    if args.path:
        for path in args.path:
            files.extend(find_json_files(path))
    else:
        files = find_json_files()
    
    if not files:
        print("No JSON files found to convert")
        return 0
    
    print(f"Converting {len(files)} JSON files to TOML format...")
    converted = []
    errors = []
    
    for path in files:
        try:
            toml_path = convert_file(path)
            converted.append(toml_path)
        except Exception as e:
            print(f"Error converting {path}: {str(e)}")
            errors.append(path)
    
    print(f"Converted {len(converted)} files successfully")
    if errors:
        print(f"Failed to convert {len(errors)} files")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 1.6 Update Tests to Support TOML Files

```python
# Add to imports in tests/test_generate.py
import tomli_w

def create_deck_file(proj, level, topic, cards, format="json"):
    """Create a deck file for testing.
    
    Args:
        proj: Project directory path
        level: Level directory (a1, a2, etc.)
        topic: Topic name (filename without extension)
        cards: List of card dictionaries to include
        format: File format ("json" or "toml")
        
    Returns:
        Path to the created file
    """
    lvl_dir = proj / "decks" / level
    lvl_dir.mkdir(parents=True, exist_ok=True)
    
    if format == "json":
        file_path = lvl_dir / f"{topic}.json"
        file_path.write_text(json.dumps({"cards": cards}, ensure_ascii=False, indent=2))
    elif format == "toml":
        file_path = lvl_dir / f"{topic}.toml"
        
        # Convert to TOML structure
        toml_data = {
            "deck": f"{level}::{topic}",
            "model": "basic",
            "notes": []
        }
        
        for idx, card in enumerate(cards, start=1):
            note = {
                "note_id": 10000 + idx,
                "tags": card.get("tags", []),
            }
            
            # Set model
            model = card.get("model", "basic")
            if model != toml_data["model"]:
                note["model"] = model
            
            # Set fields based on model
            if model == "basic":
                note["fields"] = [card.get("front", ""), card.get("back", "")]
            else:  # cloze
                note["fields"] = [card.get("front", "")]
                if "back" in card:
                    note["back"] = card["back"]
            
            toml_data["notes"].append(note)
        
        with open(file_path, "wb") as f:
            tomli_w.dump(toml_data, f)
    
    return file_path

# Add new tests for TOML format
@pytest.mark.parametrize("level", ["a1", "a2"])
@pytest.mark.parametrize("format", ["json", "toml"])
def test_per_file_mode_with_format(setup_project, level, format):
    """Test per-file mode with different file formats."""
    proj = setup_project
    create_deck_file(
        proj,
        level,
        "testtopic",
        [
            {
                "model": "basic",
                "front": "<b>ciao</b>",
                "back": "hello",
                "tags": [level, "testtopic"],
            }
        ],
        format=format
    )
    result = subprocess.run(["python3", SCRIPT, "--level", level], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 1
    assert "testtopic" in out_files[0].name
    assert level in out_files[0].name

# Add test for Markdown support
def test_markdown_formatting(setup_project):
    """Test that Markdown formatting is properly converted to HTML."""
    proj = setup_project
    level = "a1"
    create_deck_file(
        proj,
        level,
        "markdown",
        [
            {
                "model": "basic",
                "front": "**Bold text**",
                "back": "- Item 1\n- Item 2",
                "tags": [level, "markdown"],
            }
        ],
        format="toml"
    )
    result = subprocess.run(["python3", SCRIPT, "--level", level], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # We can't easily check the HTML output in the .apkg file,
    # but we can at least verify that the deck was created
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 1
    assert "markdown" in out_files[0].name
```

## 2. Implementation Plan

### 2.1 Phase 1: Add TOML Support

1. **Add dependencies**:
   - Add `tomli` (for Python < 3.11) or use `tomllib` (for Python >= 3.11) to requirements.txt
   - Add `tomli-w` for writing TOML files
   - Add `markdown` for Markdown to HTML conversion

2. **Update `generate.py`**:
   - Modify `load_deck_file` to support both JSON and TOML formats
   - Rename `get_json_files` to `get_deck_files` and update to include TOML files
   - Add Markdown to HTML conversion in `build_deck`

3. **Update `validate.py`**:
   - Modify `validate_file` to support TOML format
   - Update `find_deck_files` to include TOML files

4. **Create conversion script**:
   - Implement `json_to_toml.py` to convert existing JSON files to TOML

5. **Update tests**:
   - Modify `tests/test_generate.py` to test both JSON and TOML formats
   - Add tests for Markdown formatting

### 2.2 Phase 2: Convert Existing Decks

1. **Convert all JSON files**:
   - Run `python json_to_toml.py` to convert all JSON files to TOML
   - Manually verify a sample of converted files

2. **Update documentation**:
   - Update README.md to document TOML and Markdown usage
   - Add examples of TOML deck files
   - Update contributing guidelines

### 2.3 Phase 3: Testing and Verification

1. **Run tests**:
   - Run all tests to ensure both JSON and TOML formats work
   - Verify Markdown formatting works correctly

2. **Manual verification**:
   - Import generated decks into Anki
   - Verify cards display correctly
   - Verify Markdown formatting is properly rendered

## 3. Documentation Updates

### 3.1 Update README.md

Add a new section about TOML format and Markdown support:

```markdown
## Deck File Format

The project supports two formats for deck files:

### TOML Format (Recommended)

TOML files provide a more readable and maintainable format for deck definitions:

```toml
deck = "a1::verbs"
model = "basic"  # Default model for all notes

[[notes]]
note_id = 10001
fields = ["**mangiare**", "to eat"]
tags = ["a1", "verbs"]

[[notes]]
note_id = 10002
model = "cloze"  # Override default model
fields = ["Sono andato al {{c1::cinema}} ieri sera."]
tags = ["a1", "verbs"]
```

### JSON Format (Legacy)

The project still supports the original JSON format:

```json
{
  "cards": [
    {
      "model": "basic",
      "front": "mangiare",
      "back": "to eat",
      "tags": ["a1", "verbs"]
    }
  ]
}
```

### Markdown Support

Card content can include Markdown formatting:

- **Bold text**: `**bold**`
- *Italic text*: `*italic*`
- Lists:
  ```
  - Item 1
  - Item 2
  ```
- Links: `[text](url)`
- And other standard Markdown syntax

The Markdown is automatically converted to HTML when generating Anki decks.
```

### 3.2 Update Contributing Guidelines

Update the contributing section in README.md:

```markdown
## Contributing

### Adding New Decks

1. Add new TOML file under `decks/<level>/`.
2. Follow naming: `<topic>.toml`.
3. Each note must include:
   - `fields`: Array of strings (front and back for basic, text with cloze for cloze)
   - `tags`: `["<level>", "<topic>"]`
   - Optional `model`: `"basic"` or `"cloze"` (defaults to deck's model)
   - Optional `note_id`: Unique identifier for the note
4. Run validation:
   ```bash
   python validate.py decks/<level>
   ```
```

## 4. Dependencies

- **tomli** (for Python < 3.11): TOML parser
- **tomli-w**: TOML writer
- **markdown**: Markdown to HTML converter
- **genanki**: Existing dependency for Anki deck generation

## 5. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Maintain backward compatibility with JSON files |
| Markdown rendering issues | Add tests for various Markdown constructs |
| TOML parsing errors | Add robust error handling and validation |
| Performance impact | Benchmark and optimize if necessary |

## 6. Timeline

1. **Phase 1 (Add TOML Support)**: 2-3 days
2. **Phase 2 (Convert Existing Decks)**: 1-2 days
3. **Phase 3 (Testing and Verification)**: 1-2 days

Total estimated time: 4-7 days

## 7. Success Criteria

- All existing JSON files successfully converted to TOML
- All tests pass with both JSON and TOML formats
- Markdown formatting correctly rendered in Anki cards
- Documentation updated to reflect new formats
- No regression in existing functionality

## 8. Future Considerations

- Add a linting tool for TOML files
- Create a web-based editor for TOML deck files
- Support additional Markdown extensions (tables, code blocks, etc.)
- Add a migration script to convert existing Anki decks to TOML format
```
