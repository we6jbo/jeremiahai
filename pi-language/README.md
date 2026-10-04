# JeremiahAI Pi Language Coach

Marker: `zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD`

This directory is the lightweight, persistent writing-coach knowledge base for the Ladybug Pi.

Files:
- `learned_rules.json` — Vibe-editable, human-readable recurring spelling/grammar/punctuation rules.
- `personal_dictionary.txt` — local words/names that should not be treated as ordinary misspellings.
- `mistakes.db` — SQLite history of matched recurring mistakes.
- `analyze.py` — combines learned rules with installed Hunspell/Aspell, LanguageTool, and Vale when available.
- `sync_vale_rules.py` — converts simple learned substitution rules into a Vale style when Vale is available.

Vibe may add rules when Jeremiah makes recurring mistakes, but should preserve the JSON structure,
keep rules narrowly targeted, and prefer disabling a bad rule over deleting history.

The tools do not run continuously. They are invoked only when analysis is requested.
