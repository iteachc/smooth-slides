# pptx_fixer

Safe helpers for fixing content in a PowerPoint (.pptx) file with Python. Claude uses them for you;
you can also run them yourself.

## Setup

```
pip install python-pptx pillow
```

## What is in here

| File | What it does |
|---|---|
| `dump_deck.py` | Prints every slide: text, tables, pictures, positions, notes, hidden slides. Run it first |
| `pptx_fixer.py` | The helper functions (below) |
| `example_fix.py` | A small fix script with made-up fixes. Copy it and replace the fix list |

## The helpers

All slide numbers are 1-based, as in PowerPoint. All positions are in inches.

| Function | Use it to |
|---|---|
| `replace_text(slide, old, new, expected=1)` | Change text even when PowerPoint split it across runs. Formatting is kept. `expected` stops the script if the count is wrong |
| `replace_text_in_slides(prs, range(5, 9), old, new, expected_each=1)` | The same change on several slides (a stem repeated on question and solution slides) |
| `set_lines(shape, [...])` | Rewrite a whole text box, keeping its look |
| `find_shape(slide, contains=, geom=, at=)` | Find one shape by its text, its type (`'mathMultiply'`, `'roundRect'`...) or its position |
| `move_shape(shape, top_in=, left_in=)` | Move a shape, for example a tick box that sits on the wrong option row |
| `clone_shape(slide, shape, top_in=)` | Copy a shape with all its formatting, for example another cross mark |
| `animate_with_click(slide, 0, shape)` | Make a shape appear **with** an existing click (0 = first click). It does not add a new click |
| `replace_image(slide, picture, 'new.png')` | Swap the picture inside a picture shape; position, size and animation stay |
| `extract_images(prs, 'out/')` | Save every picture so you can look at it |
| `hidden_slides(prs)`, `pdf_page_for_slide(prs, n)` | Find hidden slides and map a slide number to its PDF page |
| `print_log()` | Print a change report at the end of your script |

## Workflow

1. `python dump_deck.py deck.pptx` to see what is in the deck.
2. Copy `example_fix.py` to `fix_<deckname>.py`, replace the fixes.
3. `python fix_<deckname>.py deck.pptx "deck (reviewed v1 - content fixes).pptx"`
   (the script refuses to overwrite its input).
4. Render the new file to PDF and look at every changed slide:
   ```
   soffice --headless --convert-to pdf "deck (reviewed v1 - content fixes).pptx"
   pdftoppm -r 80 -jpeg "deck (reviewed v1 - content fixes).pdf" check
   ```
5. Put every change in the Fixes Log.

## Notes and limits

- `replace_text` keeps the formatting of the first run the match touches. If a replacement
  spans a bold and a plain run, the result takes the first run's look.
- `set_lines` copies the first paragraph's first run as the template for every line. Mixed
  formatting inside the old text is lost.
- Shapes inside groups have group-relative positions. Add new shapes at the slide root.
- If a slide has no animation, `animate_with_click` stops with a clear message. Add the
  animation in PowerPoint first, or leave the shape visible.
- Always keep the arrow, tick and cross characters in an Arial run (see `GOTCHAS.md`).
- For a worked-out reveal built from a picture plus black masks, edit the picture
  (`replace_image`); do not rebuild it as text.
