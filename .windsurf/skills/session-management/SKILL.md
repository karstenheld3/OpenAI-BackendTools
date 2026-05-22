---
name: session-management
description: Apply when initializing, saving, resuming, or closing a work session
---

# Session Management Guide

## Phase Tracking

Sessions track EDIRD phases:
- NOTES.md: "Current Phase" section with phase, last verb, gate status
- PROGRESS.md: "Phase Plan" section with 5 phases and status

## MUST-NOT-FORGET

- Session folder location: `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`
- Default: `[DEFAULT_SESSIONS_FOLDER]` = `[WORKSPACE_FOLDER]` (override in `!NOTES.md`)
- Required files: NOTES.md, PROBLEMS.md, PROGRESS.md
- Lifecycle: Init → Work → Save → Resume → Finalize → Archive
- Sync session PROBLEMS.md to project on /session-finalize
- Phase tracking: NOTES.md has current phase, PROGRESS.md has full phase plan
- **Topic Folders**: `T##_TopicDescription_YYYY-MM-DD/` for independent work streams. Max 1 level. Run detection procedure on session entry.
- **STOP after session init**: After creating session files, STOP and wait for user review. Do NOT implement session goal until explicitly requested. User must review and refine goals before work begins.

## Session Lifecycle

1. **Init** (`/session-new`): Create session folder with tracking files
2. **Work**: Create specs, plans, implement, track progress
3. **Save** (`/session-save`): Document findings, commit changes
4. **Resume** (`/session-load`): Re-read session documents, continue work
5. **Finalize** (`/session-finalize`): Sync findings to project files, prepare for archive

## Step Folders

When a session performs multiple steps in sequence to produce an output, each step gets its own subfolder. Each subfolder yields a corresponding summary document at the session root.

### Step Folder Naming

**Pattern:** `S##_Description_YYYY-MM-DD[_gitignore]/`

- `S##` - 2-digit step sequence number with `S` prefix (S01, S02, ...)
- `Description` - CamelCase description; optionally prefixed with `TOPIC-` if step belongs to a research track (e.g., `S03_MYTPC-ExtractPatterns_2026-05-10/`)
- `YYYY-MM-DD` - date the step was executed
- `_gitignore` - optional suffix marking local-only content (large data, intermediate artifacts)

**Sub-steps:** Use letter suffix without renumbering: `S03a_`, `S03b_`

### Step Summary Documents

Each step folder gets a corresponding summary at the session root.

**Pattern:** `S##_Description_STEPLOG.md`

- Description matches the step folder name (without date and `_gitignore` suffix)
- No leading underscore (sorts alongside step folders in directory listing)
- All file references use relative markdown links: `[filename](S##_Folder/filename)`

### Step Summary Template

Use `STEPLOG_TEMPLATE.md` from this skill folder.

### Internal File Numbering

Each step folder has its own independent numbering namespace:

- `_INFO_TOPIC_01-SUMMARY.md`, `_INFO_TOPIC_02-SOURCES.md`, etc.
- Numbering starts at 01 per folder, independent of step number
- This avoids collision between step sequence (S##) and document sequence (NN)

### Example

See "Structure" example under Topic Folders section for a complete session layout including Step Folders, Topic Folders, and Bug Folders.

### When to Use Step Folders

- Session involves a multi-step pipeline (download → process → analyze → synthesize)
- Each step produces artifacts that feed the next step
- Steps may be executed on different dates or by different agents

**Not needed** for single-step sessions or sessions where all work fits in the session root with a few INFO files.

## Topic Folders

When a session contains multiple independent work streams, each stream gets its own `[TOPIC_FOLDER]` with independent tracking files. Max 1 level of nesting (session root → topic folder, never deeper).

### Naming

**Pattern:** `T##_TopicDescription_YYYY-MM-DD/`

- `T##` - 2-digit sequence number with `T` prefix (T01, T02, ...). Sequence = creation order, not dependency
- `TopicDescription` - CamelCase description; optionally prefixed with `TOPIC-` if topic belongs to a research track (e.g., `T01_XLREF-TranslationReflection_2026-05-22/`)
- `YYYY-MM-DD` - date the topic folder was created

### Structure

```
_YYYY-MM-DD_SessionName/
├── NOTES.md                        (Topic Registry, Topic/Step Folders, Bug List)
├── PROBLEMS.md
├── PROGRESS.md                     (Topic/Step Folders progress)
│
│   Topic Folders (independent work streams)
├── T01_DatabaseOptions_2026-01-15/
│   ├── NOTES.md
│   ├── PROBLEMS.md
│   ├── PROGRESS.md
│   └── _INFO_DBOPT_01.md
├── T02_APID-APIDesign_2026-01-15/
│   ├── NOTES.md
│   ├── PROBLEMS.md
│   ├── PROGRESS.md
│   └── _SPEC_APID_01.md
│
│   Step Folders (sequential pipeline)
├── S01_CollectData_2026-01-15_gitignore/
│   └── (large source files, local only)
├── S01_CollectData_STEPLOG.md
├── S02_MYTPC-AnalyzeResults_2026-01-16/
│   ├── _INFO_MYTPC_01-SUMMARY.md
│   └── _INFO_MYTPC_02-SOURCES.md
├── S02_MYTPC-AnalyzeResults_STEPLOG.md
│
│   Bug Folders (AUTH = session TOPIC ID, see /bugfix workflow)
└── AUTH-BG-0001_TokenRaceCondition/
    ├── PROBLEMS.md
    └── _INFO_*.md
```

### When to Use Topic Folders

- Session has multiple independent research tracks or work streams
- Each track has its own problems, progress, and findings
- Tracks do NOT depend on each other sequentially (use Step Folders for sequential)

**Not needed** for sessions with a single focus or where all work feeds into one outcome.

### Topic Folder Detection

Execute when entering any session workflow. Detect from the current working path:

1. Check if current folder name matches `T##_*` pattern
2. If yes: current folder is the `[TOPIC_FOLDER]`, its parent is the `[SESSION_FOLDER]`
3. Load parent tracking files (NOTES.md, PROBLEMS.md, PROGRESS.md) for context
4. Then load topic folder tracking files
5. If no: standard behavior, current folder is the `[SESSION_FOLDER]`

**Workspace-level files** (e.g., `!NOTES.md`) are loaded by `/prime`, not as parent session context.

### Topic Folder Save Sync

Execute at end of `/session-save` when working in a `T##_*` folder:

1. Save to topic folder tracking files (NOTES.md, PROBLEMS.md, PROGRESS.md)
2. Update parent PROGRESS.md `## Topic Folders` section (create section if not present):
   - Format: `- [ ] T##_Description_YYYY-MM-DD: [one-line status summary]`
   - Mark `[x]` when topic folder work is complete
3. If new cross-cutting problems found: add to parent PROBLEMS.md with cross-reference to topic folder

### Topic Folder Finalize

Execute when `/session-finalize` is invoked:

**If finalizing from a `T##_*` folder:**
- Sync findings to parent tracking files only (not project)
- Update parent PROGRESS.md topic entry to `[x]`
- Move relevant problems to parent PROBLEMS.md Resolved section
- Sync FAILS.md and LEARNINGS.md to parent if present

**If finalizing from session root with `T##_*` subfolders:**
- Aggregate all topic folder findings into parent tracking files
- Then sync to project as normal (existing `/session-finalize` behavior)

### Topic Folder Creation

When creating a new topic folder inside an existing session:

1. Determine next `T##` number (find highest existing `T##` number + 1)
2. Create `T##_TopicDescription_YYYY-MM-DD/` inside the session folder
3. Create tracking files from templates (NOTES.md, PROBLEMS.md, PROGRESS.md)
4. Register in parent NOTES.md `## Topic Folders` section
5. Add entry to parent PROGRESS.md `## Topic Folders` section

## Session Folder Location

**Base:** `[DEFAULT_SESSIONS_FOLDER]` (default: `[WORKSPACE_FOLDER]`, can be overridden in `!NOTES.md`)

**Format:** `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`

**Example:** `_PrivateSessions/_2026-01-12_FixAuthenticationBug/`

## Required Session Files

Use templates from this skill folder:

- **NOTES.md** (`NOTES_TEMPLATE.md`): Key information, agent instructions, working patterns, large initial prompts (>120 tokens)
- **PROBLEMS.md** (`PROBLEMS_TEMPLATE.md`): All problems to be addressed - initial prompts, questions, feature requests, bugs, strange behavior, investigation topics. Each problem gets a unique ID and tracks status (Open/Resolved/Deferred)
- **PROGRESS.md** (`PROGRESS_TEMPLATE.md`): Task execution tracking - to-do list, done items, tried-but-not-used approaches

**Key distinction:**
- **NOTES.md** = Context and reference information (static knowledge)
- **PROBLEMS.md** = All topics requiring attention (dynamic problem list with IDs)
- **PROGRESS.md** = Task execution status (what's being worked on)

## Assumed Workflow

```
1. INIT: User initializes session (`/session-new`)
   └── Session folder, NOTES.md, PROBLEMS.md, PROGRESS.md created

2. PREPARE (one of):
   A) User prepares work manually
      └── Creates INFO / SPEC / IMPL documents, tracks progress
   B) User explains problem, agent assists
      └── Updates Problems, Progress, Notes → researches → creates documents

3. WORK: User or agent implements
   └── Makes decisions, creates tests, implements, verifies
   └── Progress and findings tracked continuously

4. SAVE: User saves session for later (`/session-save`)
   └── Everything updated and committed

5. RESUME: User resumes session (`/session-load`)
   └── Agent primes from session files, executes workflows in Notes
   └── Continue with steps 2-3

6. FINALIZE: User finalizes session (`/session-finalize`)
   └── Everything updated, committed, synced to project/workspace

7. ARCHIVE: User archives session
   └── Session folder moved to _Archive/
```

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` rule (always-on) for complete ID system.

**Quick Reference:**
- Document: `[TOPIC]-[DOC][NN]` (IN, SP, IP, TP)
  - Example: `CRWL-SP01`, `AUTH-IP01`
- Tracking: `[TOPIC]-[TYPE]-[NNNN]` (BG = Bug, FT = Feature, PR = Problem, FX = Fix, TK = Task)
  - Example: `SAP-BG-0001`, `UI-PR-0003`, `GLOB-TK-0015`
- Topic Registry: Session-level in session NOTES.md, project-level in ID-REGISTRY.md

## Session Init Templates

Use the full templates from this skill folder (not the minimal snippets below):

- `NOTES_TEMPLATE.md` - Includes Topic Registry, Topic/Step Folders, Bug List, Significant Prompts Log
- `PROBLEMS_TEMPLATE.md` - Open/Resolved/Deferred sections with ID format
- `PROGRESS_TEMPLATE.md` - To Do/In Progress/Done, Topic/Step Folders progress
