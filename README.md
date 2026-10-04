# JeremiahAI v1.5.1 — Pi Analyze Bridge

This is a completion/bug-fix bridge for v1.5.0.

The Pi Writing Lab `Analyze / Teach` button now calls:
`/home/jeremiahai/language/analyze.py`

That analyzer combines:
- Jeremiah-specific learned rules
- Hunspell when available
- Aspell as installed/fallback context
- LanguageTool when available
- Vale when available

Current known Pi state from the v1.5.0 deployment:
- Hunspell: installed
- Aspell: installed
- LanguageTool: unavailable from configured apt repositories
- Vale: unavailable from configured apt repositories
- disk use: 17%

The portal status card now shows the custom coach plus individual tool availability.
No background service is added.

Marker: `zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD`
