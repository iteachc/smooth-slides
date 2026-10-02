# gslides_builder

Helpers that generate Google Slides API `batchUpdate` requests, for building a **solution slide**
through the Google Slides connector when you cannot (or would rather not) edit a downloaded .pptx.

**When it is worth it:** small edits, or one new slide. **When it is not:** whole decks. Every
shape and every style is a separate request, so a full slide is dozens of calls and the process is slow.
For bigger work, download the .pptx and use `tools/pptx_fixer` instead.

## Files

| File | What it does |
|---|---|
| `lib.py` | `shape`, `pill`, `divider`, `grid` and text helpers (`P`, `B`, `C`, `TICK`). Everything appends to `lib.reqs`. Positions are in inches |
| `compact.py` | Merges repeated style requests to make a batch smaller: `python compact.py batch.json 0 40` prints requests 0 to 40 |
| `example_solution_slide.py` | A complete, made-up 3-pane solution slide. Run it to see the pattern. Writes `example_slide.json` |

The look is a dark solution slide (black background, Lato, navy labels with a blue outline,
yellow "Correct Option" box, Key Idea box). Change the colour constants at the top of `lib.py` to
match your deck.

## How to use

1. Read the deck with the connector and find the **page object id** of the slide to fill. Put it in
   `PAGE_ID` in your copy of `example_solution_slide.py`.
2. Replace the example content with your own, run the script, and you get a JSON list of requests.
3. Shrink it if needed: `python compact.py example_slide.json 0 40`.
4. Send it in chunks through the connector's `update_presentation` call, with a **fresh
   `revisionId`** each time as `writeControl.requiredRevisionId`.
5. Read the slide back (or its thumbnail) and check it.

## Gotchas

- **The API stores each shape at a 3,000,000 EMU base size plus a scale factor.** To move an
  existing shape, keep its current `scaleX` and `scaleY`. Setting them to 1 blows the shape up.
- Text positions are UTF-16 units; `lib.u16` handles this.
- Tick marks and arrows need an Arial run (`TICK` does this). Other fonts may show an empty box.
- Object ids must be unique in the deck. Use a prefix per slide (`s9_title`, `s9_steps`).
- If a slide holds a picture-plus-black-mask reveal built by the creators, do not rebuild it
  with these helpers. Fix the picture and leave the animation alone.
- Exports of large decks fail above about 10 MB, so ask the user to download the .pptx by hand.
