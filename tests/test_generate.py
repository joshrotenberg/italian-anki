"""Tests for the generate.py script."""

import os
import shutil
import subprocess

import pytest
import tomli_w

# Assume generate.py is in project root
SCRIPT = "generate.py"


@pytest.fixture(autouse=True)
def setup_project(tmp_path, monkeypatch):
    """Set up a temporary project structure for testing."""
    # Create a temporary project structure
    proj = tmp_path / "proj"
    proj.mkdir()
    # Copy the generate script into the project directory
    shutil.copy(os.path.join(os.getcwd(), SCRIPT), proj / SCRIPT)
    # Ensure any working-dir calls happen inside proj
    monkeypatch.chdir(proj)
    return proj


def create_deck_file(proj, level, topic, cards):
    """Create a deck file for testing.

    Args:
        proj: Project directory path
        level: Level directory (a1, a2, etc.)
        topic: Topic name (filename without extension)
        cards: List of card dictionaries to include

    Returns:
        Path to the created file
    """
    lvl_dir = proj / "decks" / level
    lvl_dir.mkdir(parents=True, exist_ok=True)

    file_path = lvl_dir / f"{topic}.toml"

    # Convert to TOML structure
    toml_data = {"deck": f"{level}::{topic}", "model": "basic", "notes": []}  # Default model

    for idx, card in enumerate(cards, start=1):
        note = {
            "note_id": 10000 + idx,
            "tags": card.get("tags", []),
        }

        # Set model
        model = card.get("model", "basic")
        if model != toml_data["model"]:
            note["model"] = model

        # Set fields based on model
        if model == "basic":
            note["fields"] = [card.get("front", ""), card.get("back", "")]
        else:  # cloze
            note["fields"] = [card.get("front", "")]
            if "back" in card:
                note["back"] = card["back"]

        toml_data["notes"].append(note)

    with open(file_path, "wb") as f:
        tomli_w.dump(toml_data, f)

    return file_path


@pytest.mark.parametrize("level", ["a1", "a2"])
def test_per_file_mode_single_card(setup_project, level):
    """Test per-file mode with a single card deck.

    Verifies that running generate.py in per-file mode creates
    a separate deck file for each TOML file.
    """
    proj = setup_project
    # Create a single-card TOML deck
    create_deck_file(
        proj,
        level,
        "testtopic",
        [
            {
                "model": "basic",
                "front": "<b>ciao</b>",
                "back": "hello",
                "tags": [level, "testtopic"],
            }
        ],
    )
    # Run generate.py for this level
    result = subprocess.run(["python3", SCRIPT, "--level", level], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # Check that exactly one .apkg exists matching topic
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 1
    assert "testtopic" in out_files[0].name
    assert level in out_files[0].name


@pytest.mark.parametrize("level", ["a1", "a2"])
def test_per_level_mode_combines_files(setup_project, level):
    """Test per-level mode with multiple deck files.

    Verifies that running generate.py in per-level mode combines
    all TOML files of a level into a single deck.
    """
    proj = setup_project
    # Create two TOML deck files
    create_deck_file(
        proj,
        level,
        "one",
        [{"model": "basic", "front": "1", "back": "uno", "tags": [level, "one"]}],
    )
    create_deck_file(
        proj,
        level,
        "two",
        [{"model": "basic", "front": "2", "back": "due", "tags": [level, "two"]}],
    )
    # Run in per-level mode
    result = subprocess.run(
        ["python3", SCRIPT, "--mode", "per-level", "--level", level],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    # Check exactly one .apkg exists with level in name
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 1
    assert level in out_files[0].name


@pytest.mark.parametrize("level", ["a1", "a2"])
def test_chunk_mode_splits_files(setup_project, level):
    """Test chunk mode with multiple deck files.

    Verifies that running generate.py in chunk mode creates
    decks with a specified number of files each.
    """
    proj = setup_project
    # Create three TOML deck files
    for name in ["a", "b", "c"]:
        create_deck_file(
            proj,
            level,
            name,
            [{"model": "basic", "front": name, "back": name, "tags": [level, name]}],
        )
    # Run chunk mode with size 2
    result = subprocess.run(
        ["python3", SCRIPT, "--mode", "chunk", "--chunk-size", "2", "--level", level],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    # Expect two .apkg files
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 2
    # Filenames should contain level
    for f in out_files:
        assert level in f.name


def test_markdown_formatting(setup_project):
    """Test that Markdown formatting is properly converted to HTML."""
    proj = setup_project
    level = "a1"
    create_deck_file(
        proj,
        level,
        "markdown",
        [
            {
                "model": "basic",
                "front": "**Bold text**",
                "back": "- Item 1\n- Item 2",
                "tags": [level, "markdown"],
            }
        ],
    )
    result = subprocess.run(["python3", SCRIPT, "--level", level], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # We can't easily check the HTML output in the .apkg file,
    # but we can at least verify that the deck was created
    out_files = list((proj / "output").glob("*.apkg"))
    assert len(out_files) == 1
    assert "markdown" in out_files[0].name
