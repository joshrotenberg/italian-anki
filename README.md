# Italian Anki Decks

A collection of JSON files and scripts for generating Anki decks to learn Italian at different proficiency levels.

## Repository Structure

```
italian-anki/
├── decks/
│   ├── a1/           # A1-level JSON deck files
│   └── a2/           # A2-level JSON deck files
├── generate.py       # Script to build .apkg Anki decks from JSON
├── validate.py       # Script to validate JSON deck format
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

# Build A2 decks (core + extras):
python generate.py --level a2

# Build all levels (if available):
python generate.py --level all
```

Validate JSON files:

```bash
# Validate A1 decks
python validate.py decks/a1

# Validate A2 decks
python validate.py decks/a2
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
- JSON deck validation

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

1. Add new JSON file under `decks/<level>/`.
2. Follow naming: `<topic>.json`.
3. Each card must include:
   - `model`: `basic` or `cloze`
   - `front` and `back` HTML strings
   - `tags`: `["<level>", "<topic>"]`
4. Run validation:
   ```bash
   python validate.py decks/<level>
   ```

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
