---
name: olympiad-deck-review
description: Review and verify Olympiad or practice-test slide decks (.pptx). Use for any practice-test deck: checking answer keys, finding errors or contradictions across questions and solution slides, writing a Review and Fixes Log for the deck's creators, applying content fixes to a copy of the deck, or writing verified solutions for teaching.
---

# Olympiad Deck Review

Workflow for reviewing practice-test decks and producing correction feedback or teaching material.
The full manual is `PLAYBOOK.md` in the project folder. If it exists, read it first and follow it.
This skill is the short version.

## How to install this skill

Claude Code looks for skills in a `skills/<name>/SKILL.md` file:

- **For one project:** copy the folder `olympiad-deck-review` into `<your project>/.claude/skills/`.
- **For all your projects:** copy it into `~/.claude/skills/` (on Windows: `C:\Users\<you>\.claude\skills\`).

Restart Claude Code. The skill is then used automatically when you ask to review a practice-test
deck, or you can say "use the olympiad-deck-review skill".

## Ask first

Ask which document is wanted, and the scope (whole deck or one section):

- **Review** (for the creator): what is wrong, with evidence
- **Fixes Log** (for the creator): what was changed, after fixing
- **Verified Solutions** (for a teacher): to teach from
- **Discussion scripts** (optional, for the board)

Never merge audiences into one file.

## Pipeline

```
1. EXTRACT   text, tables, images, italics, hidden slides, shape positions
2. RENDER    PDF, then images, for any slide whose content is a picture
3. SOLVE     every question from scratch, BEFORE reading the answer key
4. AUDIT     compare with the key; classify defects by severity
5. WRITE UP  the requested document(s)
6. FIX       edit a NEW copy of the deck; render-check every changed slide
```

Step 3 matters most. Reading the key first anchors you and you will rationalise its mistakes.

## Cardinal rules

1. Solve every question before looking at the key.
2. Derive answer keys from the **rendered slides**, never from a text export (option letters come out in layer order, not on-screen order).
3. Identify figures from the figure, never from the answer text. Zoom in.
4. Cross-check questions against each other for contradictions.
5. Recompute every number shown on solution slides, not just the boxed answer.
6. Re-derive the deck's structure from the file; do not assume it matches the last deck.
7. Check hidden slides. LibreOffice leaves them out of the PDF: `pdf_page = slide_number - hidden slides before it`.

## Severity

| Level | Meaning |
|---|---|
| Red: content error | Question wrong, ambiguous, or no correct option. Fix before the test |
| Orange: solution-slide error | Key right, working shown to students wrong. Fix before teaching |
| Yellow: cosmetic | Typos, layout, leftover scaffolding. Batch for next revision |

## Fix principles

- Minimum diff: one bad word means one word changed.
- Never fix a cheap question by leaking a higher-mark question's answer.
- Preserve working distractors and say what each tests.
- Only fix content errors. Call out every fix, including image fixes, with an honest "best effort" note where it applies.
- Never overwrite the original. Save versioned copies: `Deck (reviewed v1 - content fixes).pptx`.
- Keep the creator's animations. Add shapes *with* an existing click instead of creating new clicks.
- Do not rebuild picture-plus-black-mask reveal animations as text.
- Arrows and tick marks need an Arial run (other fonts may show empty boxes).

## Review write-up: five parts per defect, in order

1. Evidence table, slides quoted verbatim.
2. Consequence for a student (walk all options if "no correct option").
3. Recommended fix, smallest possible change, and what it does not touch.
4. An alternative considered and rejected (usually because it leaks another answer).
5. Cross-deck warning if the question appears in another file.

Tone: colleague, not adversary. Say what is wrong, show it, propose the fix. Leave out teaching scripts.

## Tools in this repo

- `tools/pptx_fixer/`: `dump_deck.py` (extract), `pptx_fixer.py` (safe text replace, move, clone, animate, replace image), `example_fix.py`.
- `tools/gslides_builder/`: build Google Slides API requests, for small connector-based edits.
- `templates/`: Review, Fixes Log, Verified Solutions.

## Checklist

```
[ ] Ask: which document(s)? scope? depth?
[ ] Dump text/tables/images; check hidden slides; note PDF page offset
[ ] Convert to PDF; compare page count with slide count; render image-only slides
[ ] Solve all questions from scratch, key unread
[ ] Compare with the key; classify red / orange / yellow
[ ] Cross-check questions; recompute arithmetic on solution slides
[ ] Write the Review (and Fixes Log after fixing)
[ ] Fix a NEW copy; render-check every touched slide
```
