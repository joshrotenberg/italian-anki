# Italian Anki Decks - Developer Guidelines

This document provides specific information for developers working on the Italian Anki Decks project.

## Repository Information

- **Repository URL**: https://github.com/joshrotenberg/italian-anki
- **Additional Context**: For more context, you can check the repository's Issues, Pull Requests, and commit history.

## Build/Configuration Instructions

### Environment Setup

1. **Python Requirements**:
   - Python 3.8+ is required
   - Install dependencies: `pip install -r requirements.txt`

2. **Project Structure**:
   - Deck files are organized by CEFR level (a1, a2, etc.) in the `decks/` directory
   - Each deck file is a TOML file following the schema requirements enforced by `validate.py`
   - The `generate.py` script builds Anki decks from these TOML files
   - The `validate.py` script validates the TOML files against the schema requirements

### Building Decks

The project supports multiple build modes:

1. **Per-file mode** (default): Creates a separate deck for each TOML file
   ```bash
   python generate.py --level a1
   ```

2. **Per-level mode**: Combines all TOML files of a level into a single deck
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

Here's a simple test that verifies a TOML file is valid:

```python
import os
import sys

# Import appropriate TOML library based on Python version
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

def test_validate_toml_file():
    # Load a sample deck file
    with open('decks/a1/alfabeto.toml', 'rb') as f:
        data = tomllib.load(f)

    # Validate structure
    assert 'deck' in data
    assert data['deck'].startswith('a1::')
    assert 'notes' in data
    assert len(data['notes']) > 0

    # Validate notes
    for note in data['notes']:
        assert 'tags' in note
        assert len(note['tags']) >= 2
        assert note['tags'][0] == 'a1'
        assert note['tags'][1] == 'alfabeto'
        assert 'fields' in note
        assert len(note['fields']) >= 2 if note.get('model', 'basic') == 'basic' else 1
```

## Additional Development Information

### TOML Schema

The schema requirements enforced by `validate.py` define the expected structure of the TOML deck files:

- Each deck file should have:
  - "deck": The deck name (must start with the level followed by "::")
  - "notes": An array of note objects
- Each note must have:
  - "model": Either "basic" or "cloze" (defaults to "basic" if not specified)
  - "fields": An array with the content of the card (at least 2 fields for "basic" model)
  - "tags": An array with exactly 2 items:
    - First tag must be the level (a1, a2, b1)
    - Second tag must be the topic (matching the filename without extension)

### Markdown Support

The project supports Markdown formatting in TOML files:

- **Basic Formatting**:
  - Bold text: `**bold**`
  - Italic text: `*italic*`
  - Lists: Use `-` or `*` for bullet points, and `1.`, `2.`, etc. for numbered lists
  - Line breaks: Use a blank line to create a new paragraph

- **Usage in Cards**:
  - Markdown is automatically converted to HTML when generating Anki decks
  - Use Markdown instead of HTML for better readability and maintainability
  - For cases where Markdown doesn't support required formatting, HTML can still be used

- **Examples**:
  ```toml
  fields = [
    "Come si dice **hello** in italiano?",
    "Si dice *ciao* in italiano."
  ]
  ```

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
- **Always run tests and linting tools after making changes to any code files**

### CI Test Requirements

**Important**: All CI tests must be run manually before completing any work on Python scripts. This ensures that your changes meet the project's quality standards and don't introduce new issues.

Run the following tests in order:

1. **Validation**: Ensure all deck files are valid
   ```bash
   python validate.py
   ```

2. **Formatting**: Check and fix code formatting
   ```bash
   python format_with_black.py
   ```

3. **Linting**: Check and fix linting issues
   ```bash
   python lint.py --fix
   ```

4. **Type Checking**: Verify type annotations
   ```bash
   mypy --ignore-missing-imports *.py tests/*.py
   ```

5. **Security Scanning**: Check for security issues
   ```bash
   bandit -r . -x ./tests
   safety check
   ```

6. **Unit Tests**: Run all tests to ensure functionality
   ```bash
   python -m pytest
   ```

Only after all these tests pass should you consider your work complete and ready for submission.

## Common CI Issues and Solutions

The project uses a CI pipeline that performs various checks to ensure code quality. Here are common issues that might cause CI failures and how to fix them:

### TOML Validation Issues

The `validate.py` script checks that each note in the TOML deck files follows the project's schema requirements:

- **Issue**: Tags don't follow the required structure
  - **Solution**: Each note must have exactly 2 tags:
    1. First tag must match the level directory name (a1, a2, etc.)
    2. Second tag must match the filename (without extension)
  - **Fix**: Run `python fix_tags.py` to automatically fix tag issues

- **Issue**: TOML syntax errors
  - **Solution**: Ensure your TOML files are valid
  - **Fix**: Use a TOML validator or editor with TOML validation

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
