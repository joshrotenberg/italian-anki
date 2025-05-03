# Command Line Interface

This reference guide provides detailed information about the command-line interface (CLI) tools available in the Italian Anki Decks project.

## Generate Script

The `generate.py` script is used to build Anki decks from TOML files.

### Usage

```bash
python src/generate.py [options]
```

### Options

| Option | Description |
| ------ | ----------- |
| `--level LEVEL` | Specify the level to build (a1, a2, b1, basic) |
| `--all` | Build all levels |
| `--mode MODE` | Specify the build mode (per-file, per-level, uber, chunk) |
| `--chunk-size SIZE` | Specify the number of files per chunk (for chunk mode) |
| `--auto-discover` | Automatically discover and build all deck files |
| `--output-dir DIR` | Specify the output directory for the generated decks |
| `--verbose` | Enable verbose output |
| `--help` | Show help message and exit |

### Build Modes

The `generate.py` script supports multiple build modes:

#### Per-file Mode (Default)

Creates a separate deck for each TOML file:

```bash
python src/generate.py --level a1
```

Output: Multiple `.apkg` files, one for each TOML file in the specified level.

#### Per-level Mode

Combines all TOML files of a level into a single deck:

```bash
python src/generate.py --mode per-level --level a1
```

Output: One `.apkg` file containing all cards from the specified level.

#### Uber Mode

Creates one big deck with all cards from all levels:

```bash
python src/generate.py --mode uber
```

Output: One `.apkg` file containing all cards from all levels.

#### Chunk Mode

Creates decks with a specified number of files each:

```bash
python src/generate.py --mode chunk --chunk-size 10 --level a1
```

Output: Multiple `.apkg` files, each containing cards from up to 10 TOML files.

### Examples

```bash
# Build A1 decks in per-file mode
python src/generate.py --level a1

# Build A2 decks in per-level mode
python src/generate.py --mode per-level --level a2

# Build all levels in uber mode
python src/generate.py --mode uber --all

# Build B1 decks in chunk mode with 5 files per chunk
python src/generate.py --mode chunk --chunk-size 5 --level b1

# Auto-discover and build all deck files
python src/generate.py --auto-discover

# Auto-discover and build one big deck
python src/generate.py --auto-discover --mode uber

# Specify a custom output directory
python src/generate.py --level a1 --output-dir ./my-decks
```

## Validate Script

The `validate.py` script is used to validate TOML deck files against the schema requirements.

### Usage

```bash
python src/validate.py [paths...]
```

### Arguments

| Argument | Description |
| -------- | ----------- |
| `paths` | One or more paths to validate (files or directories) |

### Examples

```bash
# Validate a specific file
python src/validate.py decks/a1/alfabeto.toml

# Validate all files in a level
python src/validate.py decks/a1

# Validate multiple levels
python src/validate.py decks/a1 decks/a2

# Validate all deck files
python src/validate.py decks
```

## Fix Tags Script

The `fix_tags.py` script is used to automatically fix tags in deck files.

### Usage

```bash
python src/fix_tags.py [options]
```

### Options

| Option | Description |
| ------ | ----------- |
| `--dry-run` | Show what would be changed without making changes |
| `--verbose` | Enable verbose output |
| `--help` | Show help message and exit |

### Examples

```bash
# Fix tags in all deck files
python src/fix_tags.py

# Show what would be changed without making changes
python src/fix_tags.py --dry-run

# Fix tags with verbose output
python src/fix_tags.py --verbose
```

## Lint Script

The `lint.py` script is used to run linting checks on the Python code.

### Usage

```bash
python src/lint.py [options] [files...]
```

### Options

| Option | Description |
| ------ | ----------- |
| `--fix` | Automatically fix issues where possible |
| `--help` | Show help message and exit |

### Arguments

| Argument | Description |
| -------- | ----------- |
| `files` | One or more files to lint (optional) |

### Examples

```bash
# Lint all Python files
python src/lint.py

# Lint specific files
python src/lint.py src/generate.py src/validate.py

# Automatically fix issues
python src/lint.py --fix
```

## Format with Black Script

The `format_with_black.py` script is used to format Python code with Black.

### Usage

```bash
python src/format_with_black.py [options]
```

### Options

| Option | Description |
| ------ | ----------- |
| `--check` | Check if files are formatted without modifying them |
| `--help` | Show help message and exit |

### Examples

```bash
# Format all Python files
python src/format_with_black.py

# Check if files are formatted without modifying them
python src/format_with_black.py --check
```

## HTML to Markdown Script

The `html_to_markdown.py` script is used to convert HTML to Markdown.

### Usage

```bash
python src/html_to_markdown.py [options] [input_file] [output_file]
```

### Arguments

| Argument | Description |
| -------- | ----------- |
| `input_file` | Input HTML file |
| `output_file` | Output Markdown file |

### Examples

```bash
# Convert HTML to Markdown
python src/html_to_markdown.py input.html output.md
```