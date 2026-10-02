---
name: deck-builder
description: Build a new Olympiad-style class deck (.pptx) from a topic and grade. Use when asked to create, generate or draft a practice-test or teaching deck on a topic, e.g. "make a G7 acids and bases deck". Writes original questions, verifies every key with the olympiad-deck-review method, and builds click-by-click solution slides in the creators' house style, with every image need flagged for the art team or a diagram bot.
---

# Deck Builder

Turns a **topic + grade** into a class deck with questions, theory, worked solutions and revision.
Pair it with the `olympiad-deck-review` skill: this skill **builds** decks, and that one **checks** them.
Every question goes through that review before you see the deck.

> ⚠️ **This is a rudimentary pilot.** It shows that Claude can do the build and review loop; it is not a
> finished-art pipeline. The diagrams it draws are deliberately basic. **Better diagrams can be made by prompting a
> separate image or diagram bot** (or the art team) with the ART NEEDED briefs the deck produces.
> Say this plainly in every set of deliverables.

Scripts live in this skill's `scripts/` folder:

- `deckkit.py`: the slide builders (house slides, question/solution layout, click reveals, art placeholders).
- `figs.py`: example draft SVG figures (test tubes, beaker + dropper).
- `example_acids_bases.py`: a complete worked example (Grade 7 Acids, Bases and Neutralisation: 34 slides,
  9 questions). Copy it and change the content for a new topic.

Requirements: `pip install python-pptx pymupdf pillow lxml`, plus LibreOffice for render checks.

## Ask first

1. Grade, topic and syllabus chapter (e.g. NCERT Class 7, "Acids, Bases and Salts").
2. How many sub-topics (usually 3–4), and is it conceptual or numerical-heavy?
3. Which deck is the style reference? Always use the creators' **most recent** deck; older decks may be outdated.
4. Are there existing decks on this topic? Read them so you **don't repeat their questions**.

## How a class deck flows

Per sub-topic:

```
Section slide → hook question → its solution → theory (1–2 slides) → 2–3 more questions (each: ask + solve) → revision slide
```

- **Pace:** 3–4 sub-topics per class. Aim for about 8–10 conceptual questions an hour, or 5–6 if numerical-heavy.
- **One thing at a time:** every theory card, table row, solution step, ✖ and ✔ appears on its own click.
- **Visual anchoring:** a solution slide repeats its question slide exactly (same box, same option rows). Only the
  steps column changes, and statements turn green (true) or red (false) where they are, so students always
  know where to look.
- **Front and back:** title slide, plan slide (sub-topics + "what we'll do"), and an answer-key slide at the end.

## Step 1: Match the house style

`deckkit.py` ships with a dark Olympiad style: black background, Lato, a blue/pink/teal section band, a navy
question box with a blue border, grey option rows with orange (A)–(D), red ✖ and green ✔. To match a real
deck, render it and dump its shape geometry, then adjust:

- the `C` colour table, `title_slide`, `section_slide`, `concept_header`, `Q._base` positions;
- `assets/logo.png` and `assets/bulb.png` (optional). Without them, plain shapes stand in. **Brand assets belong
  to the creators: keep them out of any public repo.**

## Step 2: Write the questions

- **Original only.** Don't copy questions from the creators' decks or from past papers.
- **Mix the formats:** match-the-column, statement sets (I–IV), Assertion–Reason, figure-based, "which is NOT",
  "which plan works", and numerical where the topic allows.
- **Every distractor needs one specific flaw** you can name in the solution (wrong pairing, missing statement,
  true but irrelevant reason, incomplete method).
- **Traps worth using:** "all bases are alkalis", "gets cold" instead of warm, a neutral substance that only masks
  a property, and indicators that only change in one direction.
- **Balance the answer letters** across the deck (no AAAA).
- **No giveaways.** Theory teaches the rule; the questions must use different examples or numbers from the
  theory slides.
- **Stay inside the grade's syllabus.** Put any stretch fact in the key idea.

## Step 3: Verify before building (use `olympiad-deck-review`)

Solve every question cold, as if you had never seen the key:

- Check that exactly one option survives.
- Check every distractor fails for the stated reason.
- Recompute all arithmetic.
- Check that no theory slide gives the answer away.

Fix the question before you build, not after.

## Step 4: Build with deckkit

```python
from deckkit import *
prs = new_deck()
title_slide(prs, ['Acids, Bases and', 'Neutralisation'], 7)
plan_slide(prs, 'Acids, Bases and Neutralisation', ['Topic 1', 'Topic 2', 'Topic 3'], 'Solve first, then learn the idea…')
section_slide(prs, 1, 'Acids and Bases Around Us')

q = Q(1, ['Match the substances in Column I with the acids they contain.',   # one stem line per entry
          'Column I:   P. Curd   Q. Vinegar ...', 'Which option matches them correctly?'],
      ['P–1, Q–3 ...', 'P–2, ...', 'P–3, ...', 'P–3, ...'], 'C', opt_w=2.6)
q.ask(prs, notes)
q.solve(prs, [
    dict(y=2.45, h=0.55, lines=['Curd → lactic acid. So P–3.'], cross='AB'),   # click 1: text + crosses
    dict(y=3.05, h=0.55, lines=['Ant sting → formic acid. So R–2.'], cross='D'),
    dict(y=3.65, h=0.4, lines=[[S('Answer: (C)', color='green', bold=True)]], tick=True),
], notes, key_idea=(['Start with the pair you are surest of, then eliminate.'], 0.8))
revision(prs, 'Quick Revision', 'Acids & Bases', [('Acids', 'yellow', 'Sour …'), ...], 'Key takeaway …')
prs.save('out.pptx')
```

Layout rules that keep slides clean:

- **Stem:** each stem entry is one line (about 105 characters full width, about 70 beside a figure). The box height is automatic.
- **Short options** (`opt_w` 2.6): steps go in the right-hand column.
- **Long options** (`opt_w` 8.3, `opt_h` 0.5): pass `x=0.33, w=9.4` in each click so the steps run under the options.
- **Statement questions:** `hl=[(line_index, 'green'|'red')]` recolours a statement in place on that click.
- **Too many steps:** split them over two `solve()` slides and pass `crossed='B'` so earlier ✖ marks carry over.
- **Speaker notes:** put the full worked solution in the notes of both the ask and solve slides.
- **Arrows:** `→` is split into an Arial run automatically (Lato has no arrow glyph).

## Step 5: Art (be honest about it)

- Wherever a slide needs a picture, call `art_needed(sl, x, y, w, h, 'one-line brief')`. This draws an orange dashed box.
- **Only a few figures can be drawn well enough** to be draft placeholders, e.g. glassware, test tubes, simple
  circuits and Venn diagrams. Draw them as SVG in `figs.py`, convert with `svg_to_png`, and pass them to `Q(fig=(png, w, h, True, None))`.
  Each one gets a **DRAFT** tag automatically.
- In the notes file, list every ART NEEDED box and draft figure by slide. Say that each brief can be used as a
  prompt for a diagram or image bot (ask for a black or transparent background and the same labels), or handed to the
  art team.

## Step 6: Render-check

Convert the deck to PDF with LibreOffice, render the pages to PNG and read every slide. Look for:

- text overflowing its box;
- the key-idea box colliding with options or a figure;
- ✖ marks on the wrong row;
- the tick on the wrong option.

Also re-open the deck with python-pptx and confirm that every animation target id exists on its slide.

## Step 7: Deliverables

1. `<Deck name> (generated pilot vN).pptx`: never overwrite an earlier version.
2. `<Deck name> — Pilot Notes.md`, containing:
   - the pilot disclaimer and the diagram-bot note;
   - a structure table;
   - the answer key;
   - the art table (slide, item, draft or needed);
   - known limits.

## Checklist

```
[ ] Ask: grade, topic, chapter, sub-topics, style reference (latest deck), existing decks on the topic
[ ] Questions written: original, mixed formats, named flaw per distractor, balanced letters, no giveaways
[ ] Every key verified cold (olympiad-deck-review)
[ ] Built: hook → theory → 2-3 Qs → revision per sub-topic; one-at-a-time clicks; anchored solution layout
[ ] Art: ART NEEDED boxes + DRAFT tags; briefs usable as diagram-bot prompts
[ ] Render-checked every slide; animation targets valid
[ ] Deck + Pilot Notes delivered, with the "rudimentary pilot / better diagrams via a bot" callout
```
