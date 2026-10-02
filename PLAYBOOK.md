# Practice-Test Deck Playbook

### How to review and fix any Olympiad practice-test deck with Claude Code

**How to start:** give Claude this file and a `.pptx`, and say:
*"Read PLAYBOOK.md, then review `<file>.pptx`. I want <Review / Fixes Log / both>."*

---

## 1. Context

| | |
|---|---|
| **Who uses it** | A teacher or content creator who builds or checks practice-test decks |
| **Typical deck** | About 20 questions: Logical Reasoning, a few science chapters, and a harder "Achievers" section. A question slide is followed by 1-3 solution slides. Your decks may differ: always read the structure from the file in front of you |
| **Two jobs, two audiences** | (a) a **teacher** wants to teach from the deck; (b) the **creator** wants a list of corrections. These need *different documents*. See section 6 |
| **Tone** | Concise and direct. Lead with the finding, not the process. Colleague, not adversary |

---

## 2. The pipeline

```
1. EXTRACT   text, tables, images, italics, hidden slides, shape positions
2. RENDER    convert to PDF, then to images, for any slide whose content is a picture
3. SOLVE     every question from scratch, BEFORE reading the answer key
4. AUDIT     compare with the key; classify each defect by severity
5. WRITE UP  Review + Fixes Log (and teaching notes if asked)
6. FIX       edit a copy of the deck, then render-check it
```

**Step 3 is the one that matters.** Real defects almost always surface because the
question was solved independently first. If you read the key first, you anchor on it and
you will explain away the error instead of catching it.

---

## 3. Extraction

### 3.1 Full dump (always run first)

`tools/pptx_fixer/dump_deck.py` prints every slide: text, tables, pictures with sizes,
positions, speaker notes, and whether the slide is hidden.

```
python tools/pptx_fixer/dump_deck.py deck.pptx
```

The dump lists shapes in **layer order, not on-screen order**. Option letters can come out
shuffled (A, C, B, D). Never read an answer key from the dump. Read it from the rendered slide.

### 3.2 Hidden slides: check every time

A hidden slide is marked `show="0"`. This is not trivia:

- Hidden slides are often complete questions cut for length. They may be worth reusing, or they
  may be a leftover that still has a wrong key.
- **LibreOffice leaves hidden slides out of the PDF**, so PDF page numbers stop matching slide
  numbers. Mapping: `pdf_page = slide_number - (number of hidden slides before it)`.
  Get this wrong and you will describe the wrong slide in a defect report.
  (`pdf_page_for_slide()` in `pptx_fixer.py` does the sum for you.)

### 3.3 Italic and bold runs

Needed whenever a question says "the words in italics". Plain text extraction loses them.

```python
for para in shape.text_frame.paragraphs:
    line = ''.join(r.text for r in para.runs)
    italic = [r.text for r in para.runs if r.font.italic]
```

### 3.4 Shape positions: catch layout defects

Printing each shape's `top` and `left` shows options laid out **column by column** (A and C on
the top row, B and D below), which reads as A, C, B, D to a student.

### 3.5 Embedded images

`extract_images(prs, 'out/')` in `pptx_fixer.py` saves every picture so you can look at it.

---

## 4. Rendering

LR figures, graphs, diagrams and many solution slides are **full-slide images** with no text to extract.

### 4.1 Convert to PDF

LibreOffice can take a while on a big deck. Run it in the background and wait:

```bash
soffice --headless --convert-to pdf deck.pptx
pdfinfo deck.pdf | grep Pages
```

**Always compare `Pages` with the slide count.** A mismatch means hidden slides (3.2).

### 4.2 Turn pages into images

Make a grid of pages so you read ten slides in one look. 60-65 dpi is enough to read a
slide; use about 105 dpi to zoom into a suspected error.

```bash
pdftoppm -r 62 -jpeg -f 13 -l 22 deck.pdf page
```

```python
from PIL import Image; import glob
files = sorted(glob.glob('page-*.jpg')); ims = [Image.open(f) for f in files]
cols = 2                                   # 2 for text-heavy slides, 3 for diagram slides
w = max(i.width for i in ims); h = max(i.height for i in ims)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (w * cols, h * rows), 'white')
for k, im in enumerate(ims):
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
sheet.save('montage.jpg', quality=78)
```

---

## 5. Solve, then audit

### 5.1 Cardinal rules

1. **Solve every question before looking at the key.** No exceptions.
2. **Identify figures from the figure**, never from the answer text. Answer slides sometimes
   quietly leave out the bad item in their prose.
3. **Cross-check questions against each other.** A common defect is one question contradicting
   another in the same deck. Ask: does any other question here assert the opposite?
4. **Recompute every number on solution slides**, not just the boxed answer. Slides have been seen
   showing two different values for the same quantity.
5. **Never assume this deck is built like the last one.** Re-derive section boundaries and
   question counts from the current file.

### 5.2 Severity

| Level | Meaning | Action |
|---|---|---|
| 🔴 **Content error** | The question is wrong, ambiguous, or has no correct option | Must fix before the test |
| 🟠 **Solution-slide error** | The key is right, but the working shown to students is wrong or contradicts itself | Fix before teaching: it is on screen |
| 🟡 **Cosmetic** | Typos, layout, leftover scaffolding | Batch for the next revision |

### 5.3 Defect patterns to look for on purpose

| Pattern | What it looks like |
|---|---|
| Two questions assert opposite facts | Q3 says a cell type lines organ X; Q17's answer says it does not |
| Stem contradicts its own keyed answer | Stem says the object "stays at rest", the key says the forces are unbalanced |
| Option set has no correct member | Every listed calculation gives a value different from the one in the stem |
| Arithmetic slip in a solution slide | A factor dropped between two lines of working |
| Draft reasoning left in | "Wait, actually..." on a student-facing slide |
| Authoring scaffolding left visible | "Question Text:", "Q_ of 10", "[insert figure]" |
| Answer on the question slide | The correct option already highlighted before the reveal |
| Options laid out column by column | Reads A, C, B, D |
| Option letter missing on the answer slide | Slide shows the value but not "(B)" |
| A recall or hint slide that gives the answer away | A "revise this first" slide that uses the question's exact numbers |
| Question stem relies on an unstated assumption | "Can be dissolved by heating" without saying solubility rises with temperature |
| Language slips | a/an, missing spaces, unmatched brackets, wrong plural |
| Question numbering | A skipped or repeated number after a question was removed |

### 5.4 Fix principles

- **Minimum diff.** A good question with one bad noun needs one word changed, not a rewrite.
- **Never fix a cheap question by leaking an expensive one.** Before proposing a fix, check
  whether it gives away a later or higher-mark question. If it does, choose the fix that keeps
  the harder question intact, and *say why you rejected the alternative*. It gets changes accepted faster.
- **Preserve working distractors.** State what each one tests, to show a rewrite is not needed.
- **Give an evidence table with slide numbers** so the creator can verify without trusting the reviewer.
- **Only fix content errors.** Do not restyle, re-layout or reword for taste. Each change is
  called out in the Fixes Log.
- **Honest about images.** If a fix means editing or redrawing a picture, say it is a best-effort
  fix and what was and was not checked.

---

## 6. The deliverables

Pick by audience. **Never merge audiences into one file.** Teaching notes are mostly noise to a creator.

### A. Review *(for the creator)*

Short, actionable, and checkable without trusting the reviewer. Template: `templates/review.md`.

#### Anatomy of a defect write-up: five parts, in this order

1. **Evidence table.** Slide by slide, quoted word for word, so the creator can confirm it in
   under a minute. Close with one line joining the contradiction.
2. **Consequence.** What it does to a student. If the claim is "no option is correct", walk
   through all four options. Then concede where the key still stands.
3. **Recommended fix: the smallest possible change.** Quote the exact replacement. Say what
   it does *not* touch.
4. **An alternative considered and rejected.** Never skip this. It shows the fix was reasoned,
   and it stops the creator proposing the worse option. Often the reason is that it leaks the answer to another question.
5. **Cross-deck warning.** If the same question appears in another file: "Both files need the edit."

#### Tone

Say what is wrong, show it, propose the fix. Credit what works ("the distractors do real work").
Do not hedge a real defect into vagueness.

#### Leave out

Teaching scripts, "say this" lines, student-question prep, concept tables, mnemonics.

### B. Fixes Log *(for the creators, after the deck has been corrected)*

A change-by-change record: what changed, on which slides, why, and what was deliberately
left alone. Template: `templates/fixes-log.md`.

### C. Verified Solutions *(for the teacher)*

All questions independently solved, with the reasoning, the trap in each, and the likely
student questions. Template: `templates/verified-solutions.md`.

### D. Discussion scripts *(optional, for the board)*

Per question: the answer, the one thing worth the time, the words to say, anticipated hands.
End with a one-line-per-question pocket card. At 2-3 minutes a question: state the answer,
isolate what is wrong, spend all the time there, stop.

---

## 7. Applying the fixes

1. **Never overwrite.** Save each pass as a new file with a clear tag:
   `Deck (reviewed v1 - content fixes).pptx`, then `... v2 ...`. Leave the original untouched.
2. Write a fix script (start from `tools/pptx_fixer/example_fix.py`). Python makes the edits
   repeatable, and the script itself is a record of what changed.
3. **Render-check** the new file: convert to PDF, look at every slide you touched, and check
   the page count matches the slide count.
4. **Keep the existing animations.** Add to them (see `animate_with_click`) instead of
   rebuilding them. Many decks hide answers behind click animations.
5. List every change in the Fixes Log.
6. If you were handed a file back from someone else, **check that it opens and the slide count
   is right before building on it**. Truncated downloads happen.

---

## 8. Standing decisions

1. **Ask first:** which documents, what scope, how deep. Do not assume.
2. **Honest provenance.** State what was actually checked. Never imply independent verification
   that did not happen. A defect provable from the file itself is stronger than any reviewer's authority.
3. **Concede well.** When someone is right, say so plainly and explain why the answer still stands.
4. **Flag contestable content** even when the key is right. A sharp student may have a point; prepare the reply.
5. **Own errors directly.** If an earlier claim was wrong, say which and why, then correct it.
6. **Save deliverables to the project folder**, not a scratch directory.

---

## 9. Reference: question archetypes and the move that solves them

| Archetype | The move |
|---|---|
| Statement set "(i)-(iv), which are correct?" | Find the false one; spend all the time there |
| 3-column matching | One complete chain beats four half-chains. Anchor on a row you are sure of. Watch for the distractor whose categories are all right but whose roles are rotated |
| Table completion | Read the **constraint column** before the options |
| Assertion and Reason | Judge A alone, then R alone, then the link between them |
| Stem with stated conditions | Try to eliminate options using the stem itself |
| Coding with conditions | Conditions are conjunctions: test each half |
| Cube / dice | List adjacencies until one face has 4 neighbours; the sixth face is opposite it |
| Direction sense | Convert to bearings (N = 0 degrees, clockwise positive) and do arithmetic |
| Graph area | Use **signed** area: a block below the axis counts as negative |
| Spring vs string cut | A spring force cannot change instantly; a string's tension vanishes instantly |

### Common science traps worth a check

- Spaces between particles are **empty**, not filled with air (air is itself particles).
- The cell wall is fully permeable; the cell **membrane** is the selective one.
- -ide vs -ate: sulphide is K2S, sulphate is K2SO4.
- Antibiotics have **zero** effect on viruses.
- Solubility does not always rise with temperature: a stem that relies on it must say so.
- A mixture's "solute" and "solvent" depend on which component is present in the larger amount, not on which one you name first.

Add your own recurring findings here as you go.

---

## 10. Session checklist

```
[ ] Ask: which documents? scope? depth?
[ ] Full text/table/image dump
[ ] Check hidden slides, note the PDF page offset
[ ] Extract italics if any question depends on them
[ ] Check shape positions for layout defects
[ ] Convert to PDF; compare page count with slide count
[ ] Render every image-only slide; read the montages
[ ] Solve all questions from scratch, key unread
[ ] Compare with the key; classify red / orange / yellow
[ ] Cross-check questions against each other for contradictions
[ ] Recompute all arithmetic on solution slides
[ ] Write the Review and the Fixes Log
[ ] Apply fixes to a NEW copy; render-check every touched slide
[ ] Add any new recurring finding to section 9
```
