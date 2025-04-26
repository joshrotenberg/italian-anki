# Italian Anki Decks - Developer Guidelines

This document provides specific information for developers working on the Italian Anki Decks project.

## Build/Configuration Instructions

### Environment Setup

1. **Python Requirements**:
   - Python 3.8+ is required
   - Install dependencies: `pip install -r requirements.txt`

2. **Project Structure**:
   - Deck files are organized by CEFR level (a1, a2, etc.) in the `decks/` directory
   - Each deck file is a JSON file following the schema defined in `deck.schema.json`
   - The `generate.py` script builds Anki decks from these JSON files
   - The `validate.py` script validates the JSON files against the schema

### Building Decks

The project supports multiple build modes:

1. **Per-file mode** (default): Creates a separate deck for each JSON file
   ```bash
   python generate.py --level a1
   ```

2. **Per-level mode**: Combines all JSON files of a level into a single deck
   ```bash
   python generate.py --mode per-level --level a1
   ```

3. **Uber mode**: Creates one big deck with all cards from all levels
   ```bash
   python generate.py --mode uber
   ```

4. **Chunk mode**: Creates decks with a specified number of files each
   ```bash
   python generate.py --mode chunk --chunk-size 10 --level a1
   ```

Output `.apkg` files are created in the `output/` directory with filenames that include the level, topic, and version.

## Testing Information

### Running Tests

The project uses pytest for testing. To run all tests:

```bash
python -m pytest
```

To run specific tests with verbose output:

```bash
python -m pytest tests/test_generate.py -v
```

### Test Structure

Tests are located in the `tests/` directory. The main test file is `test_generate.py`, which tests the different modes of the `generate.py` script:

- `test_per_file_mode_single_card`: Tests per-file mode with a single card
- `test_per_level_mode_combines_files`: Tests per-level mode with multiple files
- `test_chunk_mode_splits_files`: Tests chunk mode with multiple files

### Adding New Tests

When adding new tests:

1. Follow the existing pattern in `test_generate.py`
2. Use pytest fixtures for setup and teardown
3. Use parametrization to test multiple scenarios
4. Ensure tests are isolated and don't depend on each other

### Example Test

Here's a simple test that verifies a JSON file is valid:

```python
import json
import jsonschema
import os

def test_validate_json_file():
    # Load schema
    with open('deck.schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Load a sample deck file
    with open('decks/a1/alfabeto.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate against schema
    jsonschema.validate(data, schema)

    # Additional assertions
    assert 'cards' in data
    assert len(data['cards']) > 0
    assert all(card['tags'][0] == 'a1' for card in data['cards'])
```

## Additional Development Information

### JSON Schema

The `deck.schema.json` file defines the expected structure of the JSON deck files:

- Each deck file should have a "cards" array
- Each card must have:
  - "model": Either "basic" or "cloze"
  - "front": The front content of the card
  - "back": The back content of the card
  - "tags": An array with exactly 2 items:
    - First tag must be the level (a1, a2, b1)
    - Second tag must be the topic (matching the filename without extension)

### Card Models

The project supports two card models:

1. **Basic**: Simple front/back cards
   - Front: Question or prompt
   - Back: Answer or explanation

2. **Cloze**: Fill-in-the-blank cards
   - Text: Contains cloze deletions marked with {{c1::text}}

### Version Control

- The version is stored in the `VERSION` file in the project root
- This version is embedded in deck titles and filenames
- When updating the project, increment the version number in this file

### Stable IDs

The project uses MD5 hashing to generate stable IDs for decks and models:

```python
def stable_id(name: str) -> int:
    digest = hashlib.md5(name.encode('utf-8')).hexdigest()
    return int(digest[:10], 16)
```

This ensures that decks and models have consistent IDs across builds, which is important for Anki's synchronization.

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused on a single task

## Common CI Issues and Solutions

The project uses a CI pipeline that performs various checks to ensure code quality. Here are common issues that might cause CI failures and how to fix them:

### JSON Validation Issues

The `validate.py` script checks that each card in the JSON deck files follows the project's schema requirements:

- **Issue**: Tags don't follow the required structure
  - **Solution**: Each card must have exactly 2 tags:
    1. First tag must match the level directory name (a1, a2, etc.)
    2. Second tag must match the filename (without extension)
  - **Fix**: Run `python fix_tags.py` to automatically fix tag issues

- **Issue**: JSON syntax errors
  - **Solution**: Ensure your JSON files are valid
  - **Fix**: Use a JSON validator or editor with JSON validation

### Code Formatting Issues

The CI runs Black to ensure consistent code formatting:

- **Issue**: Code doesn't follow Black's formatting rules
  - **Solution**: Format your code with Black before committing
  - **Fix**: Run `python format_with_black.py` or `black .`

### Linting Issues

The CI runs flake8 and isort to check for code quality issues:

- **Issue**: Import order is incorrect
  - **Solution**: Organize imports according to isort rules
  - **Fix**: Run `python lint.py --fix` to automatically fix import order

- **Issue**: Code doesn't follow flake8 rules
  - **Solution**: Fix the issues reported by flake8
  - **Fix**: Run `flake8` to see the issues, then fix them manually

### Type Checking Issues

The CI runs mypy to check for type errors:

- **Issue**: Missing type annotations or type errors
  - **Solution**: Add proper type annotations to functions and variables
  - **Fix**: Run `mypy --ignore-missing-imports *.py tests/*.py` to see the issues, then add the missing type annotations

### Security Scanning Issues

The CI runs bandit and safety to check for security issues:

- **Issue**: Security vulnerabilities detected by bandit
  - **Solution**: Fix the security issues or add appropriate comments to ignore false positives
  - **Fix**: Run `bandit -r . -x ./tests` to see the issues

- **Issue**: B324 - Use of weak MD5 hash for security
  - **Solution**: If MD5 is not used for security purposes (e.g., for generating stable IDs), add the `usedforsecurity=False` parameter
  - **Fix**: Change `hashlib.md5(data)` to `hashlib.md5(data, usedforsecurity=False)`
  - **Note**: If mypy reports an error about the `usedforsecurity` parameter, add a `# type: ignore` comment to the line: `hashlib.md5(data, usedforsecurity=False).hexdigest()  # type: ignore`

- **Issue**: Vulnerable dependencies detected by safety
  - **Solution**: Update dependencies to secure versions
  - **Fix**: Run `safety check` to see the issues, then update the requirements.txt file
