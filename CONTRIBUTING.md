# Contributing to the Italian Anki Deck (A1–B1)

Thank you for helping grow this multi‑level Anki resource!

## Folder Structure

```
decks/
├── a1/
├── a2/
└── b1/
```

## Prerequisites

`pip install -r requirements.txt`

Running Validation

After editing JSON files:

`python validate.py`

CI will automatically validate your changes on every PR.
If you need to mass‑reset tags in a folder:

`python fix_tags.py`

✅ Style Guide
	•	Models: use only basic or cloze.
	•	No placeholders: every card must have real, pedagogical content.
	•	Tags: exactly two tags per card:
	1.	The level ("a1", "a2", "b1")
	2.	The topic (filename without .json)
	•	Size: aim for ~20 cards per JSON file for balance.
	•	Whole‑file updates: overwrite complete files—do not submit diffs inside a file.

Adding New Content
	1.	Create a new JSON file under decks/<level>/ (e.g. decks/a2/nuovi_verbi.json).
	2.	Name the file to match the topic tag exactly.
	3.	Structure your file like:

```json
{
  "cards": [
    {
      "model": "basic",
      "front": "<b>parlare</b>",
      "back": "Meaning: to speak<br>Example: Io parlo italiano",
      "tags": ["a1","verbi_presente"]
    }
  ]
}
```

	4.	Validate locally:

`python validate.py`

	5.	Build to preview in Anki:

`python generate.py --level a1`

	6.	Commit and open a PR against main.

Workflow
	1.	Fork & clone this repo.
	2.	Create a branch: feature/<level>-<topic>.
	3.	Add/update JSON files under decks/<level>/.
	4.	Run python validate.py to catch errors.
	5.	Optionally build with python generate.py.
	6.	Commit, push, and open a PR.
	7.	CI will run validation; once it’s green, we’ll merge!

Thank you for contributing, and happy card‑making!
