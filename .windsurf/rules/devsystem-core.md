---
trigger: always_on
---

# DevSystem Core

Core definitions and structure for the development system.

## Definitions

### Core Concepts

- **[WORKSPACE]**: The Windsurf/VSCode workspace root folder
- **[PROJECT]**: If Monorepo (workspace contains multiple projects), the project subfolder. No Monorepo: Workspace = Project
- **[SESSION]**: All context belonging to a work session - folder, files, conversations, commits, and tracking files (notes, problems, progress)

### Agent Folder

**[AGENT_FOLDER]** location depends on agent:
- Windsurf: `.windsurf/`
- Claude Code: `.claude/`

### Configuration

- **[RULES]**: The current set of agent rules in `[AGENT_FOLDER]/rules/`
- **[WORKFLOWS]**: The current set of agent workflows in `[AGENT_FOLDER]/workflows/`
- **[SKILLS]**: Agent Skills in `[AGENT_FOLDER]/skills/`

### Document Types

- **[INFO]** (IN): Information gathering from web research, option and code analysis, reading documents
  - Example: `AUTH-IN01`, `CRWL-IN02`
- **[SPEC]** (SP): A specification conforming to defined rules. When implemented, must be reverse-updated (synced) from verified code changes
  - Example: `CRWL-SP01`, `AUTH-SP01`
- **[IMPL]** (IP): An implementation plan. When implemented, must be reverse-updated (synced) from verified code changes
  - Example: `CRWL-IP01`, `AUTH-IP02`
- **[TEST]** (TP): Test plans suffixed to corresponding SPEC or IMPL
  - Example: `CRWL-TP01`, `AUTH-TP01`
- **[TASKS]** (TK): Partitioned task lists from IMPL/TEST plans
  - Example: `CRWL-TK01`, `AUTH-TK01`
  - Created via `/write-tasks-plan` or `/partition`

### Tracking Documents

Tracking documents exist at workspace, project, or session level. Only one of each type per scope.

- **[NOTES]**: Important information. Agent MUST read to avoid unintentional behavior
- **[PROGRESS]**: Progress tracking. Agent MUST read to avoid unintentional behavior
- **[PROBLEMS]**: Problem tracking. Each session tracks issues in its own `PROBLEMS.md`. On `/session-close`, sync to project [PROBLEMS]
- **[FAILS]**: Failure log - lessons learned from past mistakes. Agent MUST read during `/prime` to avoid repeating errors (except when using the `_` prefix). Never delete entries unconfirmed, only append or mark as resolved.

### Placeholders

- **[ACTOR]**: Decision-making entity (default: user, in /go-autonomous: agent)

### MNF (MUST-NOT-FORGET) Technique

Prevents critical oversights during task execution.

**Planning phase:**
1. Create `MUST-NOT-FORGET` list (5-15 items max). Name must not be changed to be greppable.
2. Collect items from: FAILS.md, learnings, rules, specs, user instructions
3. Include in plan or at top of working document

**Completion phase:**
1. Review each MNF item before marking task done
2. Verify compliance or document why item doesn't apply
3. Update FAILS.md if any MNF item was violated

### Complexity Levels

Maps to semantic versioning:

- **COMPLEXITY-LOW**: Single file, clear scope, no dependencies → patch version
- **COMPLEXITY-MEDIUM**: Multiple files, some dependencies, backward compatible → minor version
- **COMPLEXITY-HIGH**: Breaking changes, new patterns, external APIs, architecture → major version

### Operation Modes

Determines where implementation outputs are placed:

- **IMPL-CODEBASE** (default): Implement in existing codebase
  - For: SPEC, IMPL, TEST, [IMPLEMENT], HOTFIX, BUGFIX
  - Output: Project source folders (`src/`, etc.)
  - Affects existing code, configuration, runtime

- **IMPL-ISOLATED**: Implement separately from existing codebase
  - For: [PROVE], POCs, prototypes, self-contained test scripts
  - Output: `[SESSION_FOLDER]/` or `[SESSION_FOLDER]/poc/`
  - Existing code/config/runtime MUST NOT be affected
  - NEVER create folders in workspace root
  - **REQUIRES SESSION**: If no session exists, run `/session-new` first

## Workspace Scenarios

Three dimensions define how the agent should behave:

### Dimension 1: Project Structure

- **SINGLE-PROJECT** - Workspace contains one project
- **MONOREPO** - Workspace contains multiple independent projects

### Dimension 2: Version Strategy

- **SINGLE-VERSION** - One active version, no migration
- **MULTI-VERSION** - Side-by-side versions (e.g., V1 and V2 coexisting)

### Dimension 3: Work Mode

- **SESSION-BASED** - Time-limited session with specific goals
- **PROJECT-WIDE** - Work spans entire project without session boundaries

## Folder Structure

### Single Project (No Monorepo)

```
[WORKSPACE_FOLDER]/
├── [AGENT_FOLDER]/
│   ├── rules/              # Agent rules (.md files)
│   ├── workflows/          # Agent workflows (.md files)
│   └── skills/             # Agent Skills (folders with SKILL.md)
├── _Archive/               # Archived sessions
├── _[SESSION_FOLDER]/       # Session folders start with underscore
│   ├── _IMPL_*.md          # Implementation plans
│   ├── _INFO_*.md          # Information documents
│   ├── _SPEC_*.md          # Specifications
│   ├── _TEST_*.md          # Test plans
│   ├── NOTES.md            # Session notes
│   ├── PROBLEMS.md         # Session problems
│   ├── PROGRESS.md         # Session progress
│   └── FAILS.md            # Lessons learned
├── src/                    # Source code
├── !NOTES.md               # Workspace notes (priority file)
├── !PROBLEMS.md            # Known problems
├── !PROGRESS.md            # Overall progress
└── FAILS.md                # Lessons learned (workspace-level)
```

### Monorepo (Multiple Projects)

```
[WORKSPACE_FOLDER]/
├── [AGENT_FOLDER]/
│   ├── rules/              # Workspace-level rules
│   ├── workflows/          # Workspace-level workflows
│   └── skills/             # Workspace-level skills
├── _Archive/               # Archived sessions (all projects)
├── [PROJECT_A]/
│   ├── _Archive/           # Project A archived sessions
│   ├── _[SESSION_FOLDER]/   # Project A sessions
│   ├── src/                # Project A source code
│   ├── NOTES.md            # Project A notes
│   ├── PROBLEMS.md         # Project A problems
│   ├── PROGRESS.md         # Project A progress
│   └── FAILS.md            # Project A lessons learned
├── [PROJECT_B]/
│   └── ...                 # Same structure
├── !NOTES.md               # Workspace-level notes
├── !PROBLEMS.md            # Workspace-level problems
├── !PROGRESS.md            # Workspace-level progress
└── FAILS.md                # Lessons learned (workspace-level)
```

## File Naming Conventions

### Priority Files (! prefix)

Files starting with `!` indicate high relevance. Must be treated with extra attention during `/prime`.

### Ignored Files (_ prefix)

Files starting with `_` are skipped by automatic priming workflows. Use for session-specific, WIP, or archived content.

### Hidden Files (. prefix)

Files starting with `.` follow Unix convention - hidden from directory listings.

### Temporary Files (.tmp prefix)

Files starting with `.tmp` are temporary helper scripts created during operations. They should be deleted after use. Example: `.tmp_fix_quotes.ps1`

## Placeholders

- **[WORKSPACE_FOLDER]**: Absolute path of root folder where Windsurf operates
- **[PROJECT_FOLDER]**: Absolute path of project folder (same as workspace if no monorepo)
- **[SRC_FOLDER]**: Absolute path of source folder
- **[DEFAULT_SESSIONS_FOLDER]**: Base folder for sessions (default: `[WORKSPACE_FOLDER]`, override in `!NOTES.md`)
- **[SESSION_ARCHIVE_FOLDER]**: Archive folder for closed sessions (default: `[SESSION_FOLDER]/../_Archive`)
- **[SESSION_FOLDER]**: Absolute path of currently active session folder

## Workflow Reference

- `/build` - BUILD workflow entry point (code output)
- `/commit` - Create conventional commits
- `/continue` - Execute next items on plan
- `/critique` - Devil's Advocate review
- `/fail` - Record failures to FAILS.md
- `/go` - Autonomous loop (recap + continue until done)
- `/implement` - Execute implementation from plan
- `/learn` - Extract learnings from resolved problems
- `/partition` - Split plans into discrete tasks
- `/prime` - Load workspace context
- `/recap` - Analyze context, identify current status
- `/reconcile` - Pragmatic review of critique findings
- `/rename` - Global/local refactoring with verification
- `/research` - Structured research with verification
- `/session-archive` - Move session folder to archive
- `/session-close` - Close session, sync findings, archive
- `/session-new` - Initialize new session
- `/session-resume` - Resume existing session
- `/session-save` - Save session progress
- `/solve` - SOLVE workflow entry point (knowledge output)
- `/sync` - Document synchronization
- `/test` - Run tests based on scope
- `/transcribe` - PDF/web to markdown transcription
- `/verify` - Verify work against specs and rules
- `/write-impl-plan` - Create implementation plan from spec
- `/write-spec` - Create specification from requirements
- `/write-strut` - Create STRUT plans with proper format
- `/write-tasks-plan` - Create tasks plan from IMPL/TEST
- `/write-test-plan` - Create test plan from spec

## STRUT Execution

STRUT plans use structured notation for progress tracking.

**Creating STRUTs**: Use `/write-strut` workflow or invoke `@write-documents` skill with `STRUT_TEMPLATE.md`.

Execution follows these rules:

### Execution Algorithm

1. **Locate current position**: Find first unchecked step `[ ] Px-Sy`
2. **Execute step**: Perform the verb action with given parameters
3. **Update checkbox**: Mark `[x]` on success, increment `[N]` on retry
4. **Check deliverables**: After step completion, verify if any `Px-Dy` can be checked
5. **At phase boundary**: Run `/verify` to evaluate transition conditions
6. **Follow transition**: Go to next phase, `[CONSULT]`, or `[END]`

### Verification Gates

- **Planning time**: Run `/verify` after creating STRUT plans to validate structure
- **Phase transitions**: Run `/verify` before transitioning between phases
- **Mandate**: Only `/verify` workflow has authority to approve autonomous phase transitions

### Resuming Interrupted Plans

1. Read PROGRESS.md or document containing STRUT plan
2. Find first unchecked deliverable `[ ] Px-Dy`
3. Identify which steps feed that deliverable
4. Continue from first unchecked step

### Checkbox States

- `[ ]` - Pending (not started)
- `[x]` - Done (completed once)
- `[N]` - Done N times (e.g., `[2]` = retried twice)

### Transition Targets

- `[PHASE-NAME]` - Next phase (e.g., `[DESIGN]`, `[IMPLEMENT]`)
- `[CONSULT]` - Escalate to [ACTOR]
- `[END]` - Plan complete

## Agent Instructions

### Before Starting Work

1. Run `/prime` to load context
2. Read all `!*.md` files (priority documentation)
3. Read session tracking files if in a session
4. Check for existing specs and plans
5. Determine current phase from NOTES.md

### During Work (EDIRD Flow)

1. Start with [ASSESS] in EXPLORE to determine workflow type and complexity
2. Execute verbs in phase order, check gates before transitions
3. Use small cycles: [IMPLEMENT]→[TEST]→[FIX]→green→next
4. Track progress in PROGRESS.md, problems in PROBLEMS.md
5. Update NOTES.md with current phase on transitions
6. Run `/verify` after significant changes

### Before Ending Session

1. Run `/session-save` to document findings
2. Ensure all changes are committed
3. Update tracking files with current phase state
