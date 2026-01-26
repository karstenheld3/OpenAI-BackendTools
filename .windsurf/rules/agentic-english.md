# Agentic English

Controlled vocabulary for agent-human communication. Provides consistency, composability, and traceability.

## Syntax

Two token types with distinct syntax:

### Instructions `[BRACKETS]`

Use brackets for tokens in **instructions** - things the agent reads and DOES:

- `[VERB]` - Action to execute (e.g., `[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`)
- `[PLACEHOLDER]` - Value to substitute (e.g., `[ACTOR]`, `[WORKSPACE_FOLDER]`)
- `[LABEL]` - Classification to apply (e.g., `[UNVERIFIED]`, `[CRITICAL]`)

**Verb modifiers:**
- `[VERB]-OK` - Successful outcome, proceed to next step
- `[VERB]-FAIL` - Failed outcome, re-iterate or escalate
- `[VERB]-SKIP` - Intentionally skipped (complexity doesn't require it)

### States `NO-BRACKETS`

No brackets for tokens in **conditions** - things the agent checks for branching:

- `PREFIX-VALUE` format (e.g., `SINGLE-PROJECT`, `COMPLEXITY-HIGH`, `HOTFIX`)
- Used in conditional headers: `## For COMPLEXITY-HIGH`
- Never substituted or executed - only checked

## Placeholders

### Decision Context

- **[ACTOR]** - Decision-making entity (default: user, in /go-autonomous: agent)

### Folder Paths

- **[WORKSPACE_FOLDER]** - Absolute path of root folder where agent operates
- **[PROJECT_FOLDER]** - Absolute path of project folder (same as workspace if no monorepo)
- **[SESSION_FOLDER]** - Absolute path of currently active session folder
- **[SRC_FOLDER]** - Absolute path of source folder
- **[AGENT_FOLDER]** - Agent config folder (`.windsurf/` or `.claude/`)

### Configuration

- **[DEVSYSTEM]** - Current DevSystem version
- **[DEVSYSTEM_FOLDER]** - Path to DevSystem folder

## Verbs

### Information Gathering

- **[RESEARCH]** - Web search, read docs, explore options
- **[ANALYZE]** - Study code, data, or documents
- **[EXPLORE]** - Open-ended investigation without specific target
- **[INVESTIGATE]** - Focused inquiry into specific issue
- **[GATHER]** - Collect information, logs, context, requirements
- **[PRIME]** - Load most relevant information into context
- **[READ]** - Careful, thorough reading of provided content with attention to detail

### Thinking and Planning

- **[SCOPE]** - Define boundaries and constraints
- **[FRAME]** - Structure the problem or approach
- **[PLAN]** - Create structured approach with steps
- **[PARTITION]** - Break large plan into small testable steps (TASKS document)
- **[DECIDE]** - Make a choice between options
- **[ASSESS]** - Assess effort, time, risk, or complexity
- **[PRIORITIZE]** - Order by importance or urgency
- **[EVALUATE]** - Compare options against criteria, score, rank
- **[SYNTHESIZE]** - Combine findings into coherent understanding
- **[CONCLUDE]** - Draw conclusions from analysis
- **[DEFINE]** - Establish clear definitions or criteria
- **[RECAP]** - Analyze context, revisit plan, identify current status
- **[CONTINUE]** - Forward-looking assessment, execute next items on plan
- **[GO]** - Sequence of [RECAP] + [CONTINUE] until goal reached

### Validation and Proof

- **[PROVE]** - POC, spike, minimal test to validate idea
- **[PROTOTYPE]** - Build working draft to test approach
- **[VERIFY]** - Check against formal rules, specs, and conventions (compliance)
- **[TEST]** - Run automated tests
- **[REVIEW]** - Inspect work (open-minded)
- **[CRITIQUE]** - Find flaws in logic, strategy, and goal alignment (disregards formal rules)
- **[RECONCILE]** - Bridge gap between ideal and feasible, balance trade-offs (disregards formal rules)

### Documentation

- **[WRITE]** - Generic write action
- **[WRITE-INFO]** - Write INFO document (research findings)
- **[WRITE-SPEC]** - Write SPEC document (specification)
- **[WRITE-IMPL-PLAN]** - Write IMPL document (implementation plan)
- **[WRITE-TEST-PLAN]** - Write TEST document (test plan)
- **[OUTLINE]** - Create high-level structure
- **[SUMMARIZE]** - Create concise summary
- **[DRAFT]** - Create initial version for review

### Implementation

- **[IMPLEMENT]** - Write code or implement proposed changes
- **[CONFIGURE]** - Set up or update environment/settings
- **[INTEGRATE]** - Connect components
- **[REFACTOR]** - Restructure code per stated goal
- **[FIX]** - Correct issues
- **[IMPROVE]** - General quality improvements
- **[OPTIMIZE]** - Performance, memory, or efficiency improvements only

### Communication

- **[CONSULT]** - Request input, clarification, decisions from [ACTOR]
- **[CLARIFY]** - Make something clearer or resolve ambiguity
- **[QUESTION]** - Ask specific questions to gather information
- **[STATUS]** - Write status report
- **[PROPOSE]** - Present multiple options for [ACTOR] to choose from
- **[RECOMMEND]** - Suggest single option with rationale
- **[CONFIRMS]** - Confirm approach or result with [ACTOR]
- **[PRESENT]** - Share findings or results with [ACTOR]

### Completion

- **[HANDOFF]** - Transfer to next phase/person
- **[COMMIT]** - Git commit
- **[MERGE]** - Combine branches
- **[DEPLOY]** - Push to environment
- **[FINALIZE]** - Perform all activities to allow for task closure
- **[CLOSE]** - Mark as done and sync data to container
- **[ARCHIVE]** - Archive closed

## Labels

### Assumption Labels

- **[UNVERIFIED]** - Assumption made without evidence
- **[CONTRADICTS]** - Logic conflicts with other statement/code
- **[OUTDATED]** - Assumption may no longer be valid
- **[INCOMPLETE]** - Reasoning missing critical considerations

### Status Labels

- **[RESOLVED]** - Issue fixed, documented for reference
- **[WONT-FIX]** - Acknowledged risk, accepted trade-off
- **[NEEDS-DISCUSSION]** - Requires [CONSULT] with [ACTOR]

## States

### Workspace Context

- **SINGLE-PROJECT** - Workspace contains one project
- **MONOREPO** - Workspace contains multiple independent projects
- **SESSION-BASED** - Time-limited session with specific goals
- **PROJECT-WIDE** - Work spans entire project without session boundaries

### Complexity Assessment

Maps to semantic versioning:

- **COMPLEXITY-LOW** - Single file, clear scope, no dependencies (patch)
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies (minor)
- **COMPLEXITY-HIGH** - Breaking changes, new patterns, external APIs (major)

### Problem Type (SOLVE workflow)

- **RESEARCH** - Explore topic, gather information
- **ANALYSIS** - Deep dive into data or situation
- **EVALUATION** - Compare options, make recommendations
- **WRITING** - Create documents, books, reports
- **DECISION** - Choose between alternatives
- **HOTFIX** - Production down
- **BUGFIX** - Defect investigation
