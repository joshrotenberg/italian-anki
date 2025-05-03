# Italian Anki Decks

Welcome to the documentation for the Italian Anki Decks project!

## Overview

This project provides a collection of deck files (TOML) and scripts for generating Anki decks to learn Italian at different proficiency levels. The decks are organized by CEFR level (A1, A2, B1) and include vocabulary, grammar, and phrases for each level.

## Features

- **Multiple Proficiency Levels**: Decks for A1, A2, B1, and basic levels
- **Flexible Generation Modes**: Generate decks per file, per level, or as one big deck
- **Markdown Support**: Use Markdown formatting in card content
- **Customizable**: Add your own decks or modify existing ones
- **Quality Assurance**: Automated validation, testing, and linting

## Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/joshrotenberg/italian-anki.git
   cd italian-anki
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Generate Anki Decks

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
```

The generated `.apkg` files will be in the `output/` directory.

## Documentation Sections

- **[User Guide](user-guide/getting-started.md)**: Instructions for using the Anki decks
- **[Developer Guide](developer-guide/contributing.md)**: Information for contributors
- **[Reference](reference/cli.md)**: Detailed reference for the command-line interface and API
- **[About](about/release-notes.md)**: Project information and release notes

## License

This project is licensed under the MIT License - see the [LICENSE](about/license.md) file for details.