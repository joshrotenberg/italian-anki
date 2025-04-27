# 📄 `draft-issues-v4.md`

---

# Issue 1: Migrate Project to TOML and Support Markdown Formatting

**Title:**  
Migrate deck sources to TOML format and support Markdown formatting inside fields

**Description:**  
Migrate all existing Anki deck source files from JSON to TOML format.  
Allow Markdown syntax (e.g., `**bold**`, `*italic*`, lists) inside fields for richer card formatting.

**Checklist:**
- [ ] Convert all `.json` files inside `a1/` and `a2/` to `.toml` format.
- [ ] Allow Markdown inside `fields` arrays.
- [ ] Update `generate.py` to read `.toml` files.
- [ ] Leave `.json` files untouched until manual verification.
- [ ] Update project README to document TOML and Markdown usage.

**Sample TOML Note Structures:**

**Basic Note:**
```toml
deck = "a1::verbs"
model = "basic"
[[notes]]
note_id = 10001
fields = ["**mangiare**", "to eat"]
tags = ["a1", "verbs"]
```

**Cloze Note:**
```toml
deck = "a1::expressions"
model = "cloze"
[[notes]]
note_id = 10002
fields = ["Sono andato al {{c1::cinema}} ieri sera."]
tags = ["a1", "expressions"]
```

**Deliverables:**
- All decks migrated to TOML.
- No functional regressions.
- Updated project documentation.

---

# Issue 2: Add Automatic Deck Discovery to `generate.py`

**Title:**  
Add automatic deck discovery for TOML files in `generate.py`

**Description:**  
Update `generate.py` to automatically discover all `.toml` files recursively.

**Checklist:**
- [ ] Use `glob.glob("*/**/*.toml", recursive=True)`.
- [ ] Parse each deck and build notes as usual.
- [ ] Log discovered decks for debugging.

**Deliverables:**
- Auto-discovery working.
- No hardcoded paths remaining.

---

# Issue 3: Define and Document a Lightweight Schema for Deck Files

**Title:**  
Define and document a schema for TOML deck files and note models

**Description:**  
Formalize the deck structure and optionally add validation inside `generate.py`.

**Checklist:**
- [ ] Document required top-level keys: `deck`, `model`, `notes`.
- [ ] Document structure for each `[[notes]]` block.
- [ ] Create `schema/note_models.toml` for central model definitions.
- [ ] (Optional) Add lightweight schema validation.

**Deliverables:**
- Schema documentation.
- (Optional) Schema validation warnings at generation time.

---

# Issue 4: Create a Target Deck for Passato Prossimo Practice

**Title:**  
Create a Target deck: `target::passato_prossimo`

**Description:**  
Create a focused concept deck under `target/`, drilling passato prossimo auxiliary choice, participio recall, and cloze examples.

**Checklist:**
- [ ] Create `target/` folder.
- [ ] Add `target/passato_prossimo.toml` with at least 10 starter notes.
- [ ] Define the custom model `target_passato_prossimo`.
- [ ] Implement appropriate card templates (auxiliary, participio, cloze).
- [ ] Tag notes appropriately.

**Deliverables:**
- New working Target deck.
- New Anki model created.

---

# Issue 5: Audit and Polish A1 and A2 Decks for Quality and Clarity

**Title:**  
Audit and polish A1 and A2 decks for formatting, consistency, and clarity

**Description:**  
Improve existing notes for clarity, Markdown formatting, proper tagging, and clear prompts.

**Checklist:**
- [ ] Correct typos and normalize Markdown.
- [ ] Ensure notes clearly indicate the part of speech or topic.
- [ ] Improve cloze deletions with proper context.
- [ ] Expand tagging.
- [ ] Move problematic notes to `fixme/` folder if needed.

**Deliverables:**
- Fully cleaned A1 and A2 decks.
- Optional `fixme/` deck created.

---

# Issue 6: Create a PLIDA B1 Exam-Focused Deck Set

**Title:**  
Create a new `plida-b1/` deck group focused on PLIDA B1 exam preparation

**Description:**  
Build exam-targeted decks aligned with the PLIDA B1 test structure: listening, reading, writing, speaking, grammar.

**Checklist:**
- [ ] Create `plida-b1/` directory.
- [ ] Create initial decks:
  - `verbs_passato_prossimo.toml`
  - `speaking_common_questions.toml`
  - `writing_email_templates.toml`
- [ ] Expand with topic-focused decks later.
- [ ] Tag and structure decks cleanly (nested deck names).

**Deliverables:**
- New `plida-b1/` deck group.
- Starter decks populated and ready to study.

---

# Issue 7: Set Up Automated GitHub Release Workflow and Project Versioning

**Title:**  
Set up automated GitHub releases and define project versioning scheme

**Description:**  
Automate project releases using GitHub Actions and define a clear versioning strategy.

**Checklist:**
- [ ] Set up GitHub Actions to create releases automatically.
- [ ] Integrate `release-please` and/or `git-cliff` for versioning + changelogs.
- [ ] Version **internally** (e.g., `version.txt`) but **do not version deck filenames**.
- [ ] Define Semantic Versioning rules:
  - **MAJOR**: Breaking changes (generate.py, deck format)
  - **MINOR**: New decks, models, significant expansions
  - **PATCH**: Typos, tagging, small improvements
- [ ] Write VERSIONING.md or update README.

**Deliverables:**
- Automated GitHub release workflow.
- Semantic versioning policy defined.
- First formal release created.


