# Italian Anki Decks

A collection of deck files (TOML) and scripts for generating Anki decks to learn Italian at different proficiency levels. Supports Markdown formatting in card content.

## Repository Structure

```
italian-anki/
├── decks/
│   ├── a1/           # A1-level deck files (TOML)
│   └── a2/           # A2-level deck files (TOML)
├── generate.py       # Script to build .apkg Anki decks from TOML
├── validate.py       # Script to validate deck file format
├── lint.py           # Script to run linting checks
├── setup.cfg         # Tool configuration
├── pyproject.toml    # Modern Python packaging and tool configuration
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── requirements.txt  # Python dependencies
└── tests/            # Automated tests
```

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

Generate Anki decks:

```bash
# Build A1 decks:
python generate.py --level a1

# Build A2 decks:
python generate.py --level a2

# Build all levels (if available):
python generate.py --all

# Build decks in different modes:
python generate.py --mode per-level  # One deck per level
python generate.py --mode uber       # One big deck with all cards
python generate.py --mode chunk --chunk-size 10  # Decks with 10 files each

# Automatically discover and build all deck files:
python generate.py --auto-discover

# Automatically discover and build one big deck:
python generate.py --auto-discover --mode uber
```

Validate deck files:

```bash
# Validate A1 decks
python validate.py decks/a1

# Validate A2 decks
python validate.py decks/a2

# Validate a specific file
python validate.py decks/a1/alfabeto.toml
```

## Development Tools

### Code Linting and Formatting

The project uses several tools to maintain code quality and consistency:

```bash
# Check all Python files for linting issues
./lint.py

# Check specific files
./lint.py generate.py validate.py

# Automatically fix issues where possible
./lint.py --fix

# Format code with black
black .
```

The code quality tools include:
- **Flake8**: For code style and quality checks
- **isort**: For consistent import ordering
- **Black**: For automatic code formatting
- **mypy**: For static type checking
- **bandit**: For security vulnerability scanning

Configuration files:
- `setup.cfg`: Configuration for isort, flake8, mypy, and pytest
- `pyproject.toml`: Modern configuration for black, isort, and other tools

### Pre-commit Hooks

The project uses pre-commit hooks to automatically check code quality before commits:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit hooks manually
pre-commit run --all-files
```

The pre-commit hooks include:
- Code formatting with black and isort
- Linting with flake8
- Type checking with mypy
- Security scanning with bandit

### Continuous Integration

The project uses GitHub Actions for continuous integration:

- **Validation**: Automatically validates all deck files
- **Linting**: Checks code style and quality
- **Type Checking**: Verifies type annotations with mypy
- **Security Scanning**: Checks for security vulnerabilities with bandit and safety
- **Testing**: Runs tests with pytest and reports coverage
- **Matrix Testing**: Tests across multiple Python versions (3.8, 3.9, 3.10, 3.11)
- **Artifact Building**: Builds and archives Anki decks

The CI workflow runs on every push to main and on pull requests.

## Contributing

### Adding New Decks

Add new decks in TOML format:

1. Add new TOML file under `decks/<level>/`.
2. Follow naming: `<topic>.toml`.
3. Include deck information:
   ```toml
   deck = "<level>::<topic>"
   model = "basic"  # Default model for all notes
   ```
4. Add notes:
   ```toml
   [[notes]]
   note_id = 10001  # Optional unique ID
   tags = ["<level>", "<topic>"]
   fields = ["Front content", "Back content"]  # For basic model

   [[notes]]
   model = "cloze"  # Override default model
   tags = ["<level>", "<topic>"]
   fields = ["Text with {{c1::cloze}} deletions"]  # For cloze model
   ```
5. Run validation:
   ```bash
   python validate.py decks/<level>/<topic>.toml
   ```

#### Markdown Support

TOML format supports Markdown formatting in card content:

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

### Development Workflow

1. Set up your development environment:
   ```bash
   # Install dependencies
   pip install -r requirements.txt

   # Install pre-commit hooks
   pre-commit install
   ```

2. Make your changes. The pre-commit hooks will automatically check your code when you commit.

3. Run tests to ensure everything works:
   ```bash
   pytest
   ```

4. Run linting manually if needed:
   ```bash
   ./lint.py
   ```

5. Update `generate.py` if adding new levels or modes.

6. Submit a pull request. The CI workflow will automatically validate your changes.
