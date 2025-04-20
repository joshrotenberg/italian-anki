import sys, glob, os, json

exit_code = 0
for path in glob.glob("decks/*/*.json"):
    level = os.path.basename(os.path.dirname(path))
    topic = os.path.splitext(os.path.basename(path))[0]
    data = json.load(open(path, encoding="utf-8"))
    for idx, card in enumerate(data.get("cards", []), start=1):
        tags = card.get("tags")
        if not (isinstance(tags, list) and len(tags) == 2):
            print(f"ERR {path} [card {idx}]: tags should be 2‑element list, got {tags}")
            exit_code = 1
        elif tags[0] != level:
            print(f"ERR {path} [card {idx}]: first tag must be '{level}', got '{tags[0]}'")
            exit_code = 1
        elif tags[1] != topic:
            print(f"ERR {path} [card {idx}]: second tag must be '{topic}', got '{tags[1]}'")
            exit_code = 1

sys.exit(exit_code)
