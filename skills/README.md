# Skills

Two Claude Code skills:

- `olympiad-deck-review/`: review and fix existing decks.
- `deck-builder/` (pilot): build a new class deck from a topic and grade. Its `scripts/` need
  `pip install python-pptx pymupdf pillow lxml`.

## Install

**Easiest:** install the plugin (see the main README):
`/plugin marketplace add iteachc/smooth-slides` then `/plugin install smooth-slides@smooth-slides`.

**By hand:**


1. Find (or create) a `skills` folder where Claude Code can see it:
   - **One project only:** `<your project>/.claude/skills/`
   - **Every project:** `~/.claude/skills/` (on Windows, `C:\Users\<you>\.claude\skills\`)
2. Copy the whole `olympiad-deck-review` folder (and `deck-builder`, if you want it) into it, so the file ends up at
   `.../skills/olympiad-deck-review/SKILL.md`.
3. Restart Claude Code.
4. Test it: ask "Which skills do you have?" or say "Use the olympiad-deck-review skill on `deck.pptx`."

The folder is self-contained: the playbook, gotchas, templates and tools travel with the skill.
