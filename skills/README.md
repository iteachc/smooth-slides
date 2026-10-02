# Skills

`olympiad-deck-review/SKILL.md` is the review workflow packaged as a Claude Code skill.

## Install

1. Find (or create) a `skills` folder where Claude Code can see it:
   - **One project only:** `<your project>/.claude/skills/`
   - **Every project:** `~/.claude/skills/` (on Windows, `C:\Users\<you>\.claude\skills\`)
2. Copy the whole `olympiad-deck-review` folder into it, so the file ends up at
   `.../skills/olympiad-deck-review/SKILL.md`.
3. Restart Claude Code.
4. Test it: ask "Which skills do you have?" or say "Use the olympiad-deck-review skill on `deck.pptx`."

The skill is a short summary. For the full manual, also copy `PLAYBOOK.md` into your project folder
and tell Claude to read it.
