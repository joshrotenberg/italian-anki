# HTML to Markdown Conversion

## Overview

This document describes the conversion of HTML formatting to Markdown in the Italian Anki Decks project's TOML files. The conversion was done to improve readability and maintainability of the deck files, and to leverage the Markdown support that was added to the project.

## Changes Made

1. **Converted HTML tags to Markdown syntax**:
   - `<br>` tags → Newlines (`\n`)
   - `<b>...</b>` tags → Bold text (`**...**`)

2. **Files Affected**:
   - All 52 TOML files in the project
   - 1651 fields were converted across these files

3. **Implementation**:
   - Created a script (`html_to_markdown.py`) to automate the conversion
   - The script preserves the original structure of the TOML files
   - Only HTML formatting was converted; other content remained unchanged

## Benefits

1. **Improved Readability**:
   - Markdown is more readable than HTML in plain text files
   - Consistent formatting across all deck files

2. **Better Maintainability**:
   - Easier for contributors to add new content using Markdown
   - Reduces the need to remember HTML syntax

3. **Consistency with Project Direction**:
   - Aligns with the project's support for Markdown formatting
   - Leverages the Markdown to HTML conversion in the generate.py script

## Validation

The conversion was validated through several steps:

1. **Syntax Validation**:
   - All converted TOML files passed validation with the project's validate.py script

2. **Visual Inspection**:
   - Sample files were manually inspected to verify correct conversion

3. **Functional Testing**:
   - Anki decks were successfully generated from the converted files
   - Both basic and cloze card types were tested

## Future Considerations

1. **Additional Markdown Features**:
   - Consider supporting more Markdown features (tables, code blocks, etc.)
   - Add examples of advanced Markdown usage in documentation

2. **HTML Fallback**:
   - For cases where Markdown doesn't support required formatting, HTML can still be used
   - The generate.py script will pass HTML through unchanged when converting Markdown to HTML

3. **Documentation Updates**:
   - Update contributing guidelines to recommend Markdown over HTML
   - Provide examples of Markdown formatting in documentation