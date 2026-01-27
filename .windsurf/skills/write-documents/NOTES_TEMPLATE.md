# NOTES Template

Template for workspace and session NOTES.md files.

## Workspace NOTES (!NOTES.md)

Workspace-level notes use `!` prefix for priority visibility.

### Required Sections

```markdown
[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\Archive

Current [DEVSYSTEM]: DevSystemV3.2
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

## Cascade Model Switching

**Tier Definitions:**
- **MODEL-HIGH** = Claude Opus 4.5 (Thinking) [5x] - Complex reasoning, specs, architecture
- **MODEL-MID** = Claude Sonnet 4.5 [2x] - Code verification, bug fixes, refactoring
- **MODEL-LOW** = Claude Haiku 4.5 [1x] - Scripts, git, file ops, monitoring

**Activity Mapping:**
- MODEL-HIGH: Writing docs, analyzing problems, architecture, gates
- MODEL-MID: Code verification, bug fixes, refactoring, implementation
- MODEL-LOW: Running scripts, git commit, file reads, session archive

**Default:** MODEL-HIGH (when uncertain)
```

### Optional Sections

- DevSystem Source/Sync Rules
- Workflow Design Rules
- Project-specific conventions

## Session NOTES (NOTES.md)

Session-level notes inside session folders.

### Header Block

```markdown
# Session Notes

**Doc ID**: [TOPIC]-NOTES
**Started**: YYYY-MM-DD
**Goal**: [Session objective]

## Current Phase

**Phase**: [PHASE-NAME] (status)
**Workflow**: /workflow-name
**Assessment**: [Brief status]
```

### Standard Sections

- **Current Phase** - Active phase and status
- **Session Info** - Objectives and context
- **Key Decisions** - Important choices made
- **Important Findings** - Discoveries and learnings
- **Document History** - Chronological updates

### Session Model Overrides

Sessions can override workspace model settings:

```markdown
## Model Switching (Session Override)

Override workspace defaults for this session:
- All tasks: Claude Sonnet 4.5
```

If present, session NOTES.md overrides workspace !NOTES.md for model selection.
