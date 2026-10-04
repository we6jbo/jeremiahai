# Vibe maintenance guide — JeremiahAI Pi Language Coach

Marker: `zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD`

When Jeremiah asks you to learn a recurring spelling, grammar, punctuation, or writing problem:

1. Read `/home/jeremiahai/language/learned_rules.json`.
2. Add or update one narrow rule. Do not rewrite the whole file.
3. Increment `seen_count` when the same recurring problem is confirmed.
4. Keep a human-readable explanation and suggestion.
5. Prefer `"enabled": false` over deleting a bad historical rule.
6. Run:
   `python3 /home/jeremiahai/language/sync_vale_rules.py`
7. Test the rule against a small sample before calling it done.
8. Append a short note to `/home/jeremiahai/language/changes.md`.

Do not automatically change Jeremiah's writing. The coach should tell him the correction and why.
