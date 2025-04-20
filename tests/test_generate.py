import os
import json
import shutil
import subprocess
import tempfile
import pytest

# Path to the generate script and VERSION file
SCRIPT = 'generate.py'
VERSION_EXPECTED = '1.0.0'

@pytest.fixture(autouse=True)
def setup_project(tmp_path, monkeypatch):
    # Create a temporary project structure
    proj = tmp_path / 'proj'
    proj.mkdir()
    # Copy generate.py and VERSION into temp project
    shutil.copy(SCRIPT, proj / 'generate.py')
    (proj / 'VERSION').write_text(VERSION_EXPECTED)
    # Create decks directory
    (proj / 'decks').mkdir()
    # Monkeypatch cwd to project root
    monkeypatch.chdir(proj)
    return proj


def create_deck_file(proj, level, topic, cards):
    # Ensure the level directory exists
    lvl_dir = proj / 'decks' / level
    lvl_dir.mkdir(parents=True, exist_ok=True)
    file_path = lvl_dir / f"{topic}.json"
    file_path.write_text(json.dumps({'cards': cards}, ensure_ascii=False))
    return file_path


def test_read_version(setup_project):
    # Import generate.py as a module and check VERSION
    import importlib.util
    spec = importlib.util.spec_from_file_location('genmod', setup_project / 'generate.py')
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    assert gen.VERSION == VERSION_EXPECTED


def test_per_file_mode_single_card(setup_project):
    proj = setup_project
    # Create a sample card JSON
    create_deck_file(proj, 'a1', 'testtopic', [
        {'model': 'basic', 'front': '<b>ciao</b>', 'back': 'hello', 'tags': ['a1','testtopic']}
    ])
    # Run generate.py in per-file mode
    result = subprocess.run(['python3', 'generate.py', '--level', 'a1'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    out_file = proj / 'output' / f"a1-testtopic-v{VERSION_EXPECTED}.apkg"
    assert out_file.exists(), f"Expected output file {out_file}"


def test_per_level_mode_combines_files(setup_project):
    proj = setup_project
    # Two JSON files in the same level
    create_deck_file(proj, 'a1', 'one', [
        {'model': 'basic', 'front': '1', 'back': 'uno', 'tags': ['a1','one']}
    ])
    create_deck_file(proj, 'a1', 'two', [
        {'model': 'basic', 'front': '2', 'back': 'due', 'tags': ['a1','two']}
    ])
    # Run in per-level mode
    result = subprocess.run(['python3', 'generate.py', '--mode', 'per-level'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    out_file = proj / 'output' / f"a1-a1-v{VERSION_EXPECTED}.apkg"
    assert out_file.exists(), f"Expected combined deck {out_file}"


def test_uber_mode_all_levels(setup_project):
    proj = setup_project
    # Create files in two different levels
    create_deck_file(proj, 'a1', 'x', [
        {'model': 'basic', 'front': '', 'back': '', 'tags': ['a1','x']}
    ])
    create_deck_file(proj, 'a2', 'y', [
        {'model': 'basic', 'front': '', 'back': '', 'tags': ['a2','y']}
    ])
    # Run in uber mode
    result = subprocess.run(['python3', 'generate.py', '--mode', 'uber'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    out_file = proj / 'output' / f"all-all-v{VERSION_EXPECTED}.apkg"
    assert out_file.exists(), f"Expected uber deck {out_file}"


def test_chunk_mode_splits_files(setup_project):
    proj = setup_project
    # Create three files in a1
    for name in ['a','b','c']:
        create_deck_file(proj, 'a1', name, [
            {'model': 'basic', 'front': name, 'back': name, 'tags': ['a1', name]}
        ])
    # Run in chunk mode with size 2
    result = subprocess.run(['python3', 'generate.py', '--mode', 'chunk', '--chunk-size', '2'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    files = sorted([f.name for f in (proj / 'output').iterdir()])
    expected1 = f"a1-a_b-v{VERSION_EXPECTED}.apkg"
    expected2 = f"a1-c-v{VERSION_EXPECTED}.apkg"
    assert expected1 in files and expected2 in files, f"Expected chunked decks {expected1} and {expected2}, got {files}"
