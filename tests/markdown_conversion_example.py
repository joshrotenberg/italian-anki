"""Example script demonstrating Markdown to HTML conversion with different options.

This script shows how to convert Markdown text to HTML with and without the nl2br extension,
which affects how line breaks are handled.
"""

import markdown  # type: ignore

# Sample text with line breaks
sample_text = "Meaning: How are you?\nExample: Ciao, **come stai**?"

# Convert with standard Markdown (without nl2br)
html_standard = markdown.markdown(sample_text)

# Convert with nl2br extension
html_with_nl2br = markdown.markdown(sample_text, extensions=["nl2br"])

print("Original text:")
print(sample_text)
print("\nHTML with standard Markdown:")
print(html_standard)
print("\nHTML with nl2br extension:")
print(html_with_nl2br)
