# Gotchas

Mistakes that cost real time. Each one bit someone once. Skim this before you start.

## Reading the deck

1. **Option letters come out wrong from a text export.**
   python-pptx and similar tools list shapes in layer (z-order) order, not the order you see.
   An option "B" can be listed after "D". **Derive answer keys from the rendered slides**
   (PDF to image), never from the text dump.

2. **Figures hide the real errors. Look at the picture.**
   A Venn diagram with a label drawn in the wrong region, a chemistry picture showing the wrong
   material: neither shows up in text. Render the slide, then zoom in. Identify a figure from the
   figure itself, not from what the answer slide says about it.

3. **Hidden slides shift the PDF page numbers.**
   LibreOffice leaves hidden slides out of the PDF. `pdf_page = slide_number - hidden slides before it`.
   Always compare the PDF page count with the slide count.

4. **Solve before you read the key.** Otherwise you will rationalise its mistakes.

## Editing the deck

5. **Keep originals; save versioned copies.**
   Never overwrite. `Deck (reviewed v1 - content fixes).pptx`, then `v2`. If someone hands you a
   file back, open it and check the slide count before building on it: truncated downloads happen.

6. **Only fix content errors, and call out every fix.**
   Do not restyle or "improve" slides. List every change in the Fixes Log, including image
   fixes. Be honest about image fixes ("best effort: redrawn, label positions checked by eye
   only").

7. **Don't rebuild creator animations as text.**
   Creators often build "reveal" effects as a full-slide picture with black mask shapes that
   exit on click. The picture holds the content. Do not extract it and retype it as text
   boxes: you will break the animation and lose the layout. Edit around it, fix the picture
   if the picture is wrong, and keep the click count the same (add shapes *with* an existing
   click, not as a new click).

8. **Text in PowerPoint is split into runs.**
   One sentence can be five runs with different formatting, so a naive find-and-replace misses it
   or flattens the formatting. Use `replace_text` in `tools/pptx_fixer`, which works across runs.

9. **Large edits to slide XML: do whole-file read, replace, write.**
   Some editing tools silently cut large XML files. If you edit raw XML, do it with a script that
   reads the whole file, changes it, validates it parses, and writes it back.

10. **Arrows, ticks and crosses need an Arial run.**
    Arrow (`→`, `↔`) and tick (`✔`) characters set in a font that does not have them (for example
    a subsetted Lato) show as empty boxes. Put them in their own run set to Arial.
    Digits as subscripts (CO2, Fe2O3) render fine as normal digits.

11. **Group-transformed coordinates are unreliable.**
    Shapes inside a group have positions relative to the group. When you add a shape, place it at
    the slide root and use slide coordinates.

12. **Recaps and added slides must match the deck's template exactly**: background, title shape,
    section colours, bullet style. Copy an existing slide rather than designing a new one.

## Google Slides specifics

13. **API shapes use a 3,000,000 EMU base size plus a scale.**
    The Slides API stores a shape at a base size and a `scaleX` / `scaleY`. When you move a shape,
    **keep its current scale**. Setting scale to 1 makes the shape jump to the huge base size.

14. **Google export of large decks fails over about 10 MB.**
    The connector cannot export the file, so ask the user to download the .pptx by hand
    (File > Download > Microsoft PowerPoint) and work from that.

15. **The connector is slow for whole slides.**
    Every shape and every style is a separate request. Use it for small edits. For anything bigger,
    fix the downloaded .pptx locally and re-upload.

16. **Text positions are in UTF-16 code units**, not characters. `tools/gslides_builder/lib.py`
    handles this (`u16`). If you hand-write requests, an emoji or symbol counts as 2.

17. **Send each batch with a fresh `revisionId`** as the required revision, or the update is rejected.

## Judgment

18. **Never fix a cheap question by leaking an expensive one.** Check what the fix gives away.
19. **Smallest possible diff.** One wrong noun is one word changed.
20. **Check numbering after any removal.** A deleted question leaves a gap that students notice.
21. **When a student could be right, say so,** and prepare the reply in advance.
