# JeremiahAI Vibe Instructions

JeremiahAI is a personal AI continuity and orchestration system.

## Ladybug policy
The Raspberry Pi is a delicate recovery appliance. Protect port 80, port 8080,
SSH/Tailscale, the Ladybug health reporter, and keep Pi disk usage below 50%.
Do not turn the Pi into a workstation and do not reinstall broad Node/npm,
X11/desktop, sync, or build stacks without explicit owner approval.

## Family work
Use:
- ~/.jeremiahai/family/tg_registry.db
- ~/.jeremiahai/family/family_seed.json

Preserve names, birth/death wording, identifiers, parents, children, provenance,
confidence, and provisional status. Never silently turn uncertain research into
permanent fact.

## Writing Lab / j03.page
JeremiahAI writing documents use the custom `.jaiw` extension.

T14 cache:
- ~/.jeremiahai/writing-cache/

Pi canonical writing store:
- /home/jeremiahai/www/writing/documents/

The purpose is to TEACH Jeremiah to improve spelling, grammar, clarity, and
writing habits. Do not simply rewrite everything for him unless he explicitly
asks for a rewrite. Prefer:
1. identify the issue,
2. explain the rule/pattern,
3. show the relevant phrase,
4. give one or two examples,
5. ask him to revise it,
6. re-check the revision.

Vale and LanguageTool are advisory tools. Do not auto-install them on the Pi.
If unavailable, report that clearly. Do not weaken the Ladybug policy merely to
add writing tools.

Writing sync uses the existing SSH service/alias. Do not create a new custom
client/server or listener for writing sync.

The Pi 8080 Writing Lab is a lightweight recovery editor. Prefer lightweight
HTML/PHP and do not introduce recursive HTTP requests.

If Pi disk use reaches 50%, stop saving nonessential new writing data there.
Keep the T14 cache and request another approved storage destination.

## Project provenance
Selected project TG identifier: TG333041.


## Writing metadata defaults
`.jaiw` documents should use these defaults:
- author: Jeremiah Burke O'Neal
- site: j03.page
- status: draft unless explicitly changed
- filename: suggest from a confident title or from the first meaningful words of a nonblank draft
- never overwrite a different new document just because the suggested filename collides; append `-2`, `-3`, etc.
- tags: suggest from the actual draft and let Jeremiah edit them
- intended publish date: leave blank unless Jeremiah supplies it

When the subject is obvious, suggest a short title. Example: a draft mainly about Vibe helping assemble genealogy can reasonably suggest `Family Tree`. When the subject is not clear, leave the title blank instead of inventing one.

New j03.page drafts may start from a two-paragraph scaffold in Jeremiah's normal concise style. Treat it as a starter, not final prose.

## JeremiahAI writing time policy
For blog metadata and the Writing Lab date/time display:
- Monday-Friday from 7:00 AM up to 11:00 AM: use 7:00 AM.
- Thursday from 7:00 AM up to 11:00 AM: use 6:30 AM instead.
- Monday and Tuesday from 11:00 AM up to 2:30 PM: do not display or write a time.
- Wednesday and Friday from 11:00 AM up to 5:30 PM: do not display or write a time.
- Thursday from 11:00 AM up to 4:00 PM: do not display or write a time.
- Outside those windows, use the actual local time.
- Date may still be displayed when time is hidden.


## Mistral writing-expansion support
The Writing Lab can create `/tmp/oct3-writing/run.sh` and `/tmp/oct3-writing/current-draft.jaiw`.
The user manually pastes/runs that launcher in a terminal.

For expansion sessions:
- read the handoff draft first;
- explain what it already says;
- offer concrete directions to expand it;
- preserve Jeremiah's voice;
- use `/home/jeremiahai/writing-draft/` on the Pi for ideas only when the Pi is reachable and healthy;
- use lightweight tools under `/home/jeremiahai/writing-tools/`;
- do not install packages merely to improve writing assistance.

### Public Moltbook privacy gate
Any Moltbook question is public and must pass the privacy checker before posting.
Use `/home/jeremiahai/writing-tools/privacy_check.py` when available, otherwise use
`~/.jeremiahai/tools/public_privacy_check.py` on the T14.

Never post the unsanitized source text.
Never expand opaque PH-* privacy codes in a public post.
If Moltbook access is unavailable, save the sanitized question and tell Jeremiah.


## File identity / integrity
JeremiahAI-created files should carry this marker when the file format safely supports metadata/comments:

`zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD`

At minimum, `.jaiw` documents use the `jeremiahai_marker` metadata field.

Before replacing a tracked Pi writing file, preserve a backup and update the integrity registry when available:
- database: `/home/jeremiahai/.zrIyFl4vK/version-control.db`
- human summary: `/home/jeremiahai/.zrIyFl4vK/version-control.md`
- backup pool: `/home/jeremiahai/vKEeQJs/`

Do not blindly restore a file merely because its MD5 changed. A legitimate edit may have changed it.
Audit first, compare the backup/current file, and require Jeremiah's confirmation before destructive restoration.


## File History / reversible deletion
JeremiahAI writing documents are versioned locally in:
- `~/.jeremiahai/file-history/history.db`
- `~/.jeremiahai/file-history/versions/`
- `~/.jeremiahai/file-history/trash/`

Do not permanently erase `.jaiw` files when a recoverable delete is available.
If Vibe or another program edits a live `.jaiw`, JeremiahAI's File History refresh will
detect the changed MD5 and preserve it as a new immutable version.

The File History tab supports Previous Version and Next Version without deleting later
history. Restoring an older version changes the live copy while keeping all snapshots.

Marker: `zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD`


## Final-build TG identifiers
- TG564843
- TG333041
- TG323932
- TG610982
- TG148675


## External blog rule files
JeremiahAI may include additional writing guidance generated at runtime from enabled shell
scripts in `~/.blogrulefiles/`. These scripts are expected to print prompt guidance to stdout.
They are deliberately external to the compiled application so Jeremiah can enable, disable,
replace, or remove them without rebuilding JeremiahAI.

When `/tmp/oct3-writing/blog-rules.txt` exists, read it before giving blog-writing guidance.
Do not let a rule file override privacy, Ladybug safety, factual accuracy, or the instruction
to preserve Jeremiah's voice.


## Scheduled Moltbook reliance
The Writing Lab launcher evaluates local time at runtime.

Before 2026-10-04 10:45 AM local time, Moltbook is light/optional.

After 2026-10-04 10:45 AM local time, Writing Lab sessions should use Moltbook more often for
unresolved research, genealogy context, writing angles, and questions raised by Jeremiah's
draft, subject to all privacy rules. Normally keep this to 1–3 focused questions per writing
session. Only return to/check Moltbook posts or threads that Mistral Vibe itself created for
JeremiahAI; do not browse unrelated posts as part of this workflow.

Useful Moltbook replies are supporting community material, not automatically verified fact.
When used in a blog, cite the relevant post/reply in APA-like form with visible author/account,
date, title or concise description, `[Online forum post]`, `Moltbook`, and the direct URL.
Record direct URLs in `.jaiw` metadata when practical.

## Writing quality gate
New or changed `.jaiw` writing is flagged:
`(did not spell/grammar check)`

A complete quality check requires:
- one spelling engine (Hunspell preferred; Aspell accepted as fallback), and
- LanguageTool grammar analysis.

Vale remains an optional additional style checker.

Do not silently remove the flag. It is cleared only when the writing analyzer records
`spell_grammar_status: checked`. If the body changes later, saving the changed body restores
the unchecked flag until analysis runs again.


## Timer / time-budget contract
The Timer tab stores a persistent expected blog-work budget. Blank expected time means 15 minutes.
Writing handoffs include expected minutes, elapsed seconds, running/stopped state, and user notes.
Treat the budget as a ceiling for the current blog workflow: when time is low, converge on a usable
final j03.page post instead of adding new branches of work.

## Family / KinMap bridge
Family work is separate from blog work.
Primary KinMap source: `/var/lib/kinmap/kinmap_state.json`.
JeremiahAI mirror: `~/.jeremiahai/family/kinmap_state.json`.
Editable troubleshooting copy: `~/.jeremiahai/family/family_trbl/kinmap_state.json`.
Family error log: `~/.jeremiahai/family/family_errors.jsonl`.

Prefer the primary source when valid. If it cannot be read or parsed, use a valid troubleshooting
copy or mirror and surface the Family trbl tab. Never invent genealogy facts to repair JSON.
The family troubleshooting Vibe launcher is intentionally separate from Writing Lab and may make
small reversible edits only to the troubleshooting copy, never directly to `/var/lib/kinmap/kinmap_state.json`.


## v1.3 Vibe operating rules

### Program-understanding permission gate
If Vibe is uncertain how JeremiahAI itself works, stores/reloads files, handles `.jaiw`
collisions, or implements another internal behavior, it must not silently inspect internals
or repeatedly speculate. Ask:

> Mr Jeremiah O'Neal, should I not worry about {the specific concern}, or should I investigate
> the JeremiahAI program to determine how it does this?

If Jeremiah says not to worry, skip the investigation and treat internal inspection as denied
for that concern. If Jeremiah says investigate, Vibe may inspect the JeremiahAI binary,
project files, scripts, settings, and related local files needed to answer the concern.
Investigation is read-only unless Jeremiah separately asks for a modification.

With permission, Vibe may append technical findings and future-improvement ideas to:
`/home/we6jbo/.oct426vibenotes/notes.md`.

Do not read those saved notes in a later session unless Jeremiah grants permission to use them.

### Vibe result-file safety
Never overwrite an existing Vibe-result `.jaiw` under `/tmp/oct3-writing/`. Use a unique
filename when a candidate already exists. The reload workflow can choose the newest result.

### Blog context
Jeremiah's blog is `https://j03.page/`, hosted on WordPress.com, current plan Premium.
This does not grant publishing or settings-change permission.

### Family lookup order
For genealogy questions:
1. `/var/lib/kinmap/kinmap_state.json`
2. `~/.jeremiahai/family/kinmap_state.json`
3. JeremiahAI family registry/seed and other existing family sources.

Use reasonable name variants before saying a person is missing. KinMap may contain newer
people than the registry.

If a family question is still missing, ambiguous, contradictory, or would otherwise lead Vibe
to question Jeremiah after the KinMap-first check, and authenticated Moltbook access exists,
post one focused privacy-sanitized question to the Moltbook GENERAL channel, wait about two
minutes (never over five minutes and never beyond the Writing Lab timer budget), and check
that Vibe-created thread once. Treat replies as community support, not automatic verification.


## Therma project context

When Jeremiah is discussing the Therma project, Vibe should use this Raspberry Pi file as
read-only project context:

`/home/jeremiahai/therma/project.md`

Use the existing `jeremiahai-pi` SSH alias and the standard Ladybug Pi safety checks.
Read `project.md` before giving Writing Lab expansion ideas that depend on Therma.

Do not edit, replace, move, or delete the Therma project file unless Jeremiah separately asks.
If the Pi or file cannot be read, state that clearly and continue from the local Writing Lab
draft instead of inventing Therma details.


## Therma Simulator tab / dedicated workflow

The Therma Simulator tab uses:
- local T14 working directory: `~/.vibeoct426/`
- local notes: `~/.vibeoct426/notes.md`
- launcher: `/tmp/vibeoct426/run.sh`
- canonical Pi project record: `/home/jeremiahai/therma/project.md`
- Pi simulator web root: `/home/jeremiahai/www/therma/`
- local family source: `~/.jeremiahai/family/kinmap_state.json`

For this workflow, `project.md` is mandatory canonical context. Vibe must read it before Therma
work and update it after meaningful decisions/changes, periodically during longer work, and
again before calling a session complete.

Family people from the current local KinMap state should be represented in the appropriate
Therma/2040 simulator section of `project.md`. Public Moltbook updates must remain privacy-safe
and must not dump private family data.

Moltbook posts made by this workflow must be privacy checked, actually posted, verified visible,
and their direct URLs recorded in local notes and in `project.md` when relevant.

The local notes file is a separate Therma workspace and is not a replacement for `project.md`.
