#!/bin/bash
# Format Python files using Black

# Install Black if not already installed
pip install black

# Format the files
black tests/test_validate.py fix_tags.py validate.py generate.py

# Check if all files are properly formatted
echo "Checking if all files are properly formatted..."
black --check tests/test_validate.py fix_tags.py validate.py generate.py

echo "Formatting complete!"
