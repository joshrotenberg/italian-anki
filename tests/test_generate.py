import os
import json
import shutil
import subprocess
import pytest

# Assume generate.py is in project root
SCRIPT = 'generate.py'

@pytest.fixture(autouse=True)
def setup_project(tmp_path, monkeypatch):
    # Create a temporary project structure
    proj = tmp_path / 'proj'
    proj.mkdir()
    # Copy the generate script into the project directory
    shutil.copy(os.path.join(os.getcwd(), SCRIPT), proj / SCRIPT)
    # Ensure any working-dir calls happen inside proj
    monkeypatch.chdir(proj)
    return proj


def create_deck_file(proj, level, topic, cards):
    # Helper: write a JSON deck file
    lvl_dir = proj / 'decks' / level
    lvl_dir.mkdir(parents=True, exist_ok=True)
    file_path = lvl_dir / f"{topic}.json"
    file_path.write_text(json.dumps({'cards': cards}, ensure_ascii=False, indent=2))
    return file_path

@pytest.mark.parametrize("level", ["a1", "a2"])
def test_per_file_mode_single_card(setup_project, level):
    proj = setup_project
    # Create a single-card JSON deck
    create_deck_file(proj, level, 'testtopic', [
        {'model': 'basic', 'front': '<b>ciao</b>', 'back': 'hello', 'tags': [level, 'testtopic']}
    ])
    # Run generate.py for this level
    result = subprocess.run(['python3', SCRIPT, '--level', level], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # Check that exactly one .apkg exists matching topic
    out_files = list((proj / 'output').glob('*.apkg'))
    assert len(out_files) == 1
    assert 'testtopic' in out_files[0].name
    assert level in out_files[0].name

@pytest.mark.parametrize("level", ["a1", "a2"])
def test_per_level_mode_combines_files(setup_project, level):
    proj = setup_project
    # Create two JSON deck files
    create_deck_file(proj, level, 'one', [
        {'model': 'basic', 'front': '1', 'back': 'uno', 'tags': [level, 'one']}
    ])
    create_deck_file(proj, level, 'two', [
        {'model': 'basic', 'front': '2', 'back': 'due', 'tags': [level, 'two']}
    ])
    # Run in per-level mode
    result = subprocess.run([
        'python3', SCRIPT, '--mode', 'per-level', '--level', level
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # Check exactly one .apkg exists with level in name
    out_files = list((proj / 'output').glob('*.apkg'))
    assert len(out_files) == 1
    assert level in out_files[0].name

@pytest.mark.parametrize("level", ["a1", "a2"])
def test_chunk_mode_splits_files(setup_project, level):
    proj = setup_project
    # Create three JSON deck files
    for name in ['a', 'b', 'c']:
        create_deck_file(proj, level, name, [
            {'model': 'basic', 'front': name, 'back': name, 'tags': [level, name]}
        ])
    # Run chunk mode with size 2
    result = subprocess.run([
        'python3', SCRIPT,
        '--mode', 'chunk', '--chunk-size', '2', '--level', level
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    # Expect two .apkg files
    out_files = list((proj / 'output').glob('*.apkg'))
    assert len(out_files) == 2
    # Filenames should contain level
    for f in out_files:
        assert level in f.name
