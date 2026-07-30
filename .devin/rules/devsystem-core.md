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
- Devin: `.devin/`
- Claude Code: `.claude/`

### Configuration

- **[RULES]**: The current set of agent rules in `[AGENT_FOLDER]/rules/`
- **[WORKFLOWS]**: The current set of agent workflows in `[AGENT_FOLDER]/workflows/`
- **[SKILLS]**: Agent Skills in `[AGENT_FOLDER]/skills/`
- **[GRUC]**: Guides, Rules, Checks - pre-calculated compliance criteria. GUIDE + RULES in each skill folder; CHECKS in each skill folder (for skills) or `drift-correction/` (for workflows). Exception: `write-documents` keeps all GRUC types in its own folder.

### Document Types

- **[INFO]** (IN): Information gathering from web research, option and code analysis, reading documents
  - Example: `AUTHSYST-IN01`, `CRAWLENG-IN02`
- **[SPEC]** (SP): A specification conforming to defined rules. When implemented, must be reverse-updated (synced) from verified code changes
  - Example: `CRAWLENG-SP01`, `AUTHSYST-SP01`
- **[IMPL]** (IP): An implementation plan. When implemented, must be reverse-updated (synced) from verified code changes
  - Example: `CRAWLENG-IP01`, `AUTHSYST-IP02`
- **[TEST]** (TP): Test plans suffixed to corresponding SPEC or IMPL
  - Example: `CRAWLENG-TP01`, `AUTHSYST-TP01`
- **[TASKS]** (TK): Partitioned task lists from IMPL/TEST plans
  - Example: `CRAWLENG-TK01`, `AUTHSYST-TK01`
  - Created via `/write-tasks-plan` or `/partition`

### Tracking Documents

Tracking documents exist at workspace, project, or session level. Only one of each type per scope.

- **[NOTES]**: Important information. Agent MUST read to avoid unintentional behavior
- **[PROGRESS]**: Progress tracking. Agent MUST read to avoid unintentional behavior
- **[PROBLEMS]**: Problem tracking. Each session tracks issues in its own `PROBLEMS.md`. On `/session-finalize`, sync to project [PROBLEMS]
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

- **SESSION-MODE** - Time-limited session with specific goals
- **PROJECT-MODE** - Work spans entire project without session boundaries

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

Files starting with `_` are skipped by automatic priming workflows. Use for session-specific, WIP, or archived content. Single `_` prefix files are deliverables (INFO, SPEC, IMPL, TEST, TASKS).

### Scaffolding Files (__ prefix)

Files starting with `__` (double underscore) are workflow/skill-generated process artifacts. Distinction:

- **User-explicit = deliverable** (no `__`): Documents the user explicitly creates via `/write-tasks-plan`, `/write-strut`, `/write-spec`, etc.
- **Workflow/skill-implicit = scaffolding** (`__`): Documents that workflows auto-create during execution (STRUTs, TASKS, templates for self-tracking)

Scaffolding has no value after the goal is reached. Deleted by `/cleanup` category 6.

**Lifecycle tiers:**
- `.tmp_` = single-run temp (scripts, metadata). Deleted within same workflow or by `/cleanup` category 1
- `__` = multi-run scaffolding (execution plans, task tracking, templates). Persists during active work, deleted by `/cleanup` after goal reached
- `_` = deliverable (findings, specs, plans). Never auto-deleted

### Hidden Files (. prefix)

Files starting with `.` follow Unix convention - hidden from directory listings.

### Git Exclusion Suffix (_gitignore)

Append `_gitignore` before the extension to exclude any file or folder from git without editing `.gitignore`:
- `data_gitignore.json` - excluded file
- `scratch_gitignore/` - excluded folder

Patterns in `.gitignore`: `*_gitignore.*` and `*_gitignore/`

## Placeholders

- **[WORKSPACE_FOLDER]**: Absolute path of root folder where Windsurf operates
- **[PROJECT_FOLDER]**: Absolute path of project folder (same as workspace if no monorepo)
- **[SRC_FOLDER]**: Absolute path of source folder
- **[DEFAULT_SESSIONS_FOLDER]**: Base folder for sessions (default: `[WORKSPACE_FOLDER]`, override in `!NOTES.md`)
- **[SESSION_ARCHIVE_FOLDER]**: Archive folder for closed sessions (default: `[SESSION_FOLDER]/../_Archive`)
- **[SESSION_FOLDER]**: Absolute path of currently active session folder

## Workflow Reference

- `/bugfix` - Record and fix bugs (SESSION-MODE or PROJECT-MODE)
- `/build` - BUILD workflow entry point (code output)
- `/cleanup` - Delete temporary files and artifacts left by workflows
- `/commit` - Create conventional commits
- `/conversation-start` - Create new conversation tracking file
- `/conversation-update` - Update existing conversation tracking file
- `/critique` - Devil's Advocate review
- `/deep-research` - Deep research (MEPI or MCPI) with domain-specific patterns
- `/drift-correct` - Close gaps identified by /drift-detect
- `/drift-detect` - Post-execution drift detection, persist gaps to __DRIFT_ file
- `/fail` - Record failures to FAILS.md
- `/fix` - Fix any problem by reading relevant DevSystem knowledge
- `/go` - Autonomous loop until goal reached
- `/implement` - Execute implementation from plan
- `/improve` - Depth-first improvement (one proven change per run)
- `/learn` - Extract learnings from resolved problems
- `/partition` - Split plans into discrete tasks
- `/prime` - Load workspace context
- `/project-release` - Create a dated release with comprehensive release notes
- `/propose-minto` - Generate AMINTON argument candidates from research material
- `/reconcile` - Pragmatic review of critique findings
- `/remove` - Remove session content, conversation content, or specific files with preview and confirmation
- `/rename` - Global/local refactoring with verification
- `/research` - Structured research with verification
- `/session-archive` - Move session folder to archive
- `/session-finalize` - Finalize session, sync findings, prepare for archive
- `/session-load` - Resume existing session
- `/session-new` - Initialize new session
- `/session-save` - Save session progress
- `/solve` - SOLVE workflow entry point (knowledge output)
- `/switch-model` - Switch Cascade AI model tier (HIGH, MID, LOW)
- `/sync` - Document synchronization
- `/test` - Run tests based on scope
- `/transcribe` - PDF/web to markdown transcription
- `/translate` - Translate markdown or PDF files to target languages
- `/verify` - Verify work against specs and rules
- `/write-impl-plan` - Create implementation plan from spec
- `/write-info` - Create INFO document from research
- `/write-minto` - Develop full Minto Pyramid article from draft
- `/write-spec` - Create specification from requirements
- `/write-strut` - Create STRUT plans with proper format
- `/write-tasks-plan` - Create tasks plan from IMPL/TEST
- `/write-test-plan` - Create test plan from spec

## STRUT Execution

STRUT plans use structured notation for progress tracking.

**Creating STRUTs**: Use `/write-strut` workflow or invoke `@skills:write-documents` with `STRUT_TEMPLATE.md`.

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

