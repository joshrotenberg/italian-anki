# Development Setup

This guide will help you set up your development environment for working on the Italian Anki Decks project.

## Prerequisites

- Python 3.8 or higher
- Git
- A text editor or IDE (e.g., VS Code, PyCharm, etc.)

## Setting Up Your Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/joshrotenberg/italian-anki.git
cd italian-anki
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Install Pre-commit Hooks

The project uses pre-commit hooks to automatically check code quality before commits:

```bash
pre-commit install
```

This will install hooks that run the following checks before each commit:
- Code formatting with black and isort
- Linting with flake8
- Type checking with mypy
- Security scanning with bandit

You can also run the pre-commit hooks manually:

```bash
pre-commit run --all-files
```

## Development Workflow

### 1. Create or Update Deck Files

Deck files are stored in the `decks/` directory, organized by level (a1, a2, b1, basic). Each deck file is a TOML file with a specific structure. See the [Deck Format](deck-format.md) guide for details.

### 2. Validate Deck Files

Use the `validate.py` script to validate your deck files:

```bash
python src/validate.py decks/<level>
```

### 3. Generate Anki Decks

Use the `generate.py` script to generate Anki decks from your TOML files:

```bash
python src/generate.py --level <level>
```

### 4. Run Tests

Run the tests to ensure everything works:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=. --cov-report=term
```

### 5. Code Quality Tools

The project uses several tools to maintain code quality:

#### Linting

```bash
python src/lint.py
```

To automatically fix issues where possible:

```bash
python src/lint.py --fix
```

#### Formatting

```bash
python src/format_with_black.py
```

#### Type Checking

```bash
mypy --ignore-missing-imports src/*.py tests/*.py
```

#### Security Scanning

```bash
bandit -r . -x ./tests
safety check
```

## Project Structure

```
italian-anki/
├── decks/
│   ├── a1/           # A1-level deck files (TOML)
│   ├── a2/           # A2-level deck files (TOML)
│   ├── b1/           # B1-level deck files (TOML)
│   └── basic/        # Basic-level deck files (TOML)
├── src/              # Python scripts
│   ├── generate.py   # Script to build .apkg Anki decks from TOML
│   ├── validate.py   # Script to validate deck file format
│   ├── lint.py       # Script to run linting checks
│   ├── fix_tags.py   # Script to fix tags in deck files
│   └── format_with_black.py # Script to format code with black
├── config/           # Configuration files
│   └── cliff.toml    # Configuration for git-cliff
├── media/            # Media files for Anki decks
├── output/           # Generated Anki decks (.apkg files)
├── styles.css        # CSS styles for Anki cards
├── VERSION           # Current version of the project
├── setup.cfg         # Tool configuration
├── pyproject.toml    # Modern Python packaging and tool configuration
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── requirements.txt  # Python dependencies
└── tests/            # Automated tests
```

## Continuous Integration

The project uses GitHub Actions for continuous integration:

- **Validation**: Automatically validates all deck files
- **Linting**: Checks code style and quality
- **Type Checking**: Verifies type annotations with mypy
- **Security Scanning**: Checks for security vulnerabilities with bandit and safety
- **Testing**: Runs tests with pytest and reports coverage
- **Matrix Testing**: Tests across multiple Python versions (3.8, 3.9, 3.10, 3.11)
- **Artifact Building**: Builds and archives Anki decks

The CI workflow runs on every push to main and on pull requests.