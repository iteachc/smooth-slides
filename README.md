# Smooth Slides

A free, shareable workflow for reviewing and fixing Olympiad practice-test slide decks
(Google Slides or PowerPoint) with [Claude Code](https://claude.com/claude-code).

It was put together by a teacher who reviews practice-test decks for content creators, and is
shared pro bono. If you build question decks, you can use it to check your own work before
it reaches students.

**This repo contains no decks, no questions and no student data.** Every example in it is
made up. Bring your own deck.

---

## Who it is for

Content creators and teachers who:

- build practice-test decks (questions, answer keys, worked-solution slides), and
- want a second pair of eyes that solves every question from scratch, finds wrong keys,
  wrong working and unclear wording, and then fixes the deck.

You do **not** need to be a programmer. You need Claude Code, and you will mostly talk to it in
plain English. The scripts in `tools/` are used by Claude on your behalf; they are there so
the fixes are safe and repeatable.

---

## The loop, end to end

```
1. DOWNLOAD   Get the deck as .pptx (Google Slides: File > Download > Microsoft PowerPoint)
      |
2. REVIEW     Claude follows the skill's PLAYBOOK.md:
      |         - solves EVERY question first, before reading the answer key
      |         - reads figures from RENDERED slide images, never from the text export
      |         - checks hidden slides, layout, arithmetic on solution slides
      |
3. WRITE UP   Two short documents for the creators (templates/):
      |         - Review       what is wrong, with slide-by-slide evidence
      |         - Fixes Log    what was changed, slide by slide, so everyone can check it
      |
4. FIX        Claude edits a COPY of the deck locally with python-pptx (tools/pptx_fixer)
      |         - original is never touched; each pass is saved as a new versioned file
      |
5. CHECK      Claude renders the fixed copy to PDF with LibreOffice and looks at every
      |         slide it changed
      |
6. RE-UPLOAD  Upload the fixed .pptx to Google Drive (or send it on), and share the Fixes Log
```

Two rules sit above everything else:

1. **Solve before you read the key.** Reading the key first makes you rationalise its mistakes.
2. **Only fix content errors, and call out every fix.** Do not redesign slides. Every change,
   including image changes, is listed in the Fixes Log, with an honest "best effort" note
   where an image fix could not be checked perfectly.

---

## Quick start

1. Install Claude Code and open it in a new, empty project folder.
2. Install the plugin (once per computer). In Claude Code, type:

   ```
   /plugin marketplace add iteachc/smooth-slides
   /plugin install smooth-slides@smooth-slides
   ```

   This brings in the whole workflow (playbook, gotchas, templates, tools) as one skill.
   Restart Claude Code if it asks.
3. Optional: copy `CLAUDE.md.template` into your folder as `CLAUDE.md` and fill in the blanks.
4. Install the tools Claude needs:
   - Python 3 and `pip install python-pptx pillow`
   - LibreOffice (to turn the deck into a PDF) and `pdftoppm` (from Poppler) to turn PDF pages into images
5. Put the downloaded `.pptx` in the folder and tell Claude:

   > Use the olympiad-deck-review skill on `my-deck.pptx`. I want a Review and a Fixes Log for the creators.

6. Read what Claude found. Then say which fixes you want applied. Claude writes a fix script
   (starting from the skill's `tools/pptx_fixer/example_fix.py`), saves a new file, and renders it for checking.

---

## What is in this repo

| Path | What it is |
|---|---|
| `.claude-plugin/` | Makes this repo installable as a Claude Code plugin |
| `skills/olympiad-deck-review/SKILL.md` | The workflow Claude follows (short version) |
| `skills/olympiad-deck-review/PLAYBOOK.md` | The full operating manual: extraction, rendering, solving, auditing, write-ups |
| `skills/olympiad-deck-review/GOTCHAS.md` | Short list of mistakes that bite everyone once. Read this first |
| `skills/olympiad-deck-review/templates/` | Fill-in templates: Review, Fixes Log, Verified Solutions (each with a made-up example) |
| `skills/olympiad-deck-review/tools/pptx_fixer/` | Safe python-pptx helpers: fix text split across runs, move or clone shapes, add click animations, swap images |
| `skills/olympiad-deck-review/tools/gslides_builder/` | Helpers that build Google Slides API requests, for the Google Slides connector route |
| `skills/README.md` | Installing without the plugin system (copy the folder by hand) |
| `CLAUDE.md.template` | Starter project instructions for Claude Code |

---

## Two ways to apply fixes

**Route A: local .pptx (recommended).** Download, fix on your computer, re-upload. It is fast,
works on whole decks, keeps your animations, and never touches the original.

**Route B: Google Slides connector.** Claude can read and edit a Google Slides file directly
through a connector. Worth it for **small edits only** (a typo, a number, one text box).
It is slow for whole slides: every shape is a separate request, and big decks are
awkward to export. For anything bigger, use Route A. The skill's `tools/gslides_builder/` is for the
cases where you do need to build a new slide through the connector.

---

## Sharing and privacy

Decks and question banks are usually the creator's property. Keep your own decks out of any
public copy of this repo. The `.gitignore` already blocks `.pptx`, `.pdf`, images and exports.

## Licence

MIT. See `LICENSE`. Use it, change it, share it.
