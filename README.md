# Italian Anki Decks

A collection of deck files (TOML) and scripts for generating Anki decks to learn Italian at different proficiency levels. Supports Markdown formatting in card content.

## Repository Structure

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
python src/generate.py --level a1

# Build A2 decks:
python src/generate.py --level a2

# Build B1 decks:
python src/generate.py --level b1

# Build basic decks:
python src/generate.py --level basic

# Build all levels:
python src/generate.py --all

# Build decks in different modes:
python src/generate.py --mode per-level  # One deck per level
python src/generate.py --mode uber       # One big deck with all cards
python src/generate.py --mode chunk --chunk-size 10  # Decks with 10 files each

# Automatically discover and build all deck files:
python src/generate.py --auto-discover

# Automatically discover and build one big deck:
python src/generate.py --auto-discover --mode uber
```

Validate deck files:

```bash
# Validate A1 decks
python src/validate.py decks/a1

# Validate A2 decks
python src/validate.py decks/a2

# Validate B1 decks
python src/validate.py decks/b1

# Validate basic decks
python src/validate.py decks/basic

# Validate a specific file
python src/validate.py decks/a1/alfabeto.toml
```

## Development Tools

### Code Linting and Formatting

The project uses several tools to maintain code quality and consistency:

```bash
# Check all Python files for linting issues
python src/lint.py

# Check specific files
python src/lint.py src/generate.py src/validate.py

# Automatically fix issues where possible
python src/lint.py --fix

# Format code with black
python src/format_with_black.py
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

1. Add new TOML file under `decks/<level>/` (e.g., `decks/a1/`, `decks/a2/`, `decks/b1/`, or `decks/basic/`).
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
   python src/validate.py decks/<level>/<topic>.toml
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
   python src/lint.py
   ```

5. Update `src/generate.py` if adding new levels or modes.

6. Fix tags in deck files if needed:
   ```bash
   python src/fix_tags.py
   ```

7. Submit a pull request. The CI workflow will automatically validate your changes.

### Release Process

The project uses [release-please](https://github.com/googleapis/release-please) for automated version management and release creation, combined with [git-cliff](https://github.com/orhun/git-cliff) for structured changelog generation.

1. **Conventional Commits**: Use [conventional commit messages](https://www.conventionalcommits.org/) when making changes:
   - `feat: add new feature` – for new features (triggers minor version bump)
   - `feature(deck): add new deck` – for new deck-specific features
   - `fix: resolve bug` – for bug fixes (triggers patch version bump)
   - `docs: update documentation` – for documentation changes
   - `refactor: improve code structure` – for code refactoring
   - `chore: update dependencies` – for maintenance tasks

2. **Automated Release PRs**: When commits are pushed to the `main` branch, release-please automatically:
   - Determines the next version based on commit types
   - Creates or updates a release PR with:
     - Updated `VERSION` file
     - Updated `CHANGELOG.md` (generated by git-cliff)

3. **CHANGELOG Validation**: The GitHub Actions workflow automatically regenerates and validates the `CHANGELOG.md` file on every pull request.
   - PRs will fail CI if the changelog is outdated
   - Run `git-cliff --config config/cliff.toml --output CHANGELOG.md` locally to update it before committing

4. **Creating Releases**: When a release PR is merged:
   - A new GitHub Release is automatically created
   - The release workflow generates and attaches `.apkg` Anki deck files to the release artifacts

5. **Manual Rebuilds**: A manual workflow (`Release`) is available under GitHub Actions to manually rebuild and reattach deck files without requiring a new version bump.

---

This automated process ensures consistent versioning, changelog quality, and artifact publishing with minimal manual intervention.
