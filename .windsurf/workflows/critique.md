---
description: Find flawed assumptions, logic errors, and hidden risks (not rule violations)
auto_execution_mode: 1
---

# Devil's Advocate

Find flawed assumptions, logic errors, and hidden risks.

**Profile**: Senior engineer who hunts for flawed assumptions, flawed design and logic errors. Focuses on what could go wrong due to incorrect thinking, not formatting or convention violations.

**Golden Rule**: NEVER touch existing code or documents. ALWAYS create or update separate versions with `_REVIEW` suffix.

**Scope Boundary**: This workflow finds **assumptions and logic / design flaws**. Use `/verify` for rule violations and convention compliance. Zero overlap.

## Required Skills

Invoke based on context:
- @write-documents for document review (use REVIEW_TEMPLATE.md, FAILS_TEMPLATE.md)

**Note**: Code review against rules/conventions is done by `/verify`. This workflow focuses on logic, strategy, and goal alignment.

## Output Files

**Two distinct output files with different purposes:**

- **`[filename]_REVIEW.md`** - Problems found in specific document/code
  - For document review: `_INFO_CRAWLER_REVIEW.md`, `_SPEC_AUTH_REVIEW.md`
  - For code review: `auth_handler_REVIEW.md`
  - Potential risks, concerns, edge cases not yet triggered
  - Hypothetical failure scenarios
  - Questions that need answers
  - Created fresh each review, can be discarded after addressing

- **`_PROBLEMS_REVIEW.md`** - Problems found in conversation/logs (no specific file)
  - Use when reviewing conversation history without specific document
  - General issues spanning multiple files

- **`FAILS.md`** - Problems that DID appear
  - Wrong assumptions that caused issues
  - Suboptimal design decisions discovered during implementation
  - Spec problems found after coding started
  - Untested behavior that broke in practice
  - Any mistake made during the implementation process
  - **Serves as "lessons learned" memory** - read during `/prime` to avoid repeating mistakes
  - Never delete entries, only append

## Workflow

1. Determine context (Code, Document, Conversation, Logs)
2. Read `FAILS.md` first (if exists) - learn from past mistakes
3. Read Global Rules
4. Read relevant Context-Specific section
5. **Create internal MUST-NOT-FORGET list** - key constraints, user requirements, critical rules
6. **Create MUST-RESEARCH list** - identify 5 topics for industry research (see Research Phase below)
7. **Execute research** - search for industry patterns, alternatives, known pitfalls
8. Create Devil's Advocate task list (informed by research)
9. Work through task list:
   - Update `_PROBLEMS_REVIEW.md` with potential issues found
   - Update `FAILS.md` with actual failures/mistakes discovered
   - **Check MUST-NOT-FORGET list after each major finding**
   - **Include research findings** in issue analysis
10. Run Final Checklist
11. **Verify against MUST-NOT-FORGET list** - did we miss anything?

## GLOBAL-RULES

**Mindset**: Assume every assumption is wrong. Your job is to prove the logic is sound.

**DO focus on**:
- Flawed assumptions about data, environment, or behavior
- Logic errors and incorrect reasoning
- Hidden complexity and edge cases
- What happens when things fail unexpectedly
- Contradictions between stated intent and actual behavior

**DO NOT focus on** (use `/verify` instead):
- Rule violations and convention compliance
- Formatting and style issues
- Missing documentation sections
- Naming conventions

**Working Rules**:
- **Never edit originals** - Create `_REVIEW` suffix copies for suggestions
- **Research before assuming** - Do web searches to verify claims and find failure examples
- **Question assumptions** - What are we taking for granted that could be wrong?
- **Be specific** - Vague concerns are useless. Cite line numbers, exact scenarios
- **Prioritize by impact** - Critical logic flaws first

**Categories and Labels**: See FAILS_TEMPLATE.md and REVIEW_TEMPLATE.md in @write-documents skill.

**FAILS.md Location and Format**: See FAILS_TEMPLATE.md in @write-documents skill.

## Research Phase

After creating MUST-NOT-FORGET list, identify **5 topics** for industry research.

### Creating MUST-RESEARCH List

For each review, identify topics where external knowledge would strengthen the analysis:

1. **Core pattern/approach** - What industry pattern is being used? Are there better alternatives?
2. **Known failure modes** - What breaks in production for this type of system?
3. **Security considerations** - What attack vectors exist for this approach?
4. **Scalability patterns** - How do others handle growth in this domain?
5. **Testing strategies** - What testing approaches work for this type of code/design?

**Format:**
```markdown
## MUST-RESEARCH
1. [Topic 1] - [Why this matters for the review]
2. [Topic 2] - [Why this matters]
3. [Topic 3] - [Why this matters]
4. [Topic 4] - [Why this matters]
5. [Topic 5] - [Why this matters]
```

### Executing Research

For each topic:
1. **Web search** for industry patterns, blog posts, case studies
2. **Look for failure examples** - post-mortems, Stack Overflow issues, GitHub issues
3. **Find alternatives** - what do other teams/frameworks do differently?
4. **Note sources** - document where findings came from

### Adding Research to Review

Add "Industry Research Findings" section to `_REVIEW.md` - see REVIEW_TEMPLATE.md for format.

## Context-Specific Sections

### No Document in Context (Conversation Review)

When called without specific document, review the entire conversation:

1. **Re-read everything**: Conversation, code changes, logs, console output
2. **Hunt for flawed assumptions**:
   - Assumptions about data shape or availability
   - Assumptions about execution order or timing
   - Assumptions about external system behavior
   - Logic that works in happy path but fails on edge cases
   - Contradictions between what was said and what was done
   - Decisions based on incomplete information
3. **Create/Update** `_PROBLEMS_REVIEW.md`:
   ```markdown
   # Problems Found - Devil's Advocate Review
   
   **Reviewed**: [Date] [Time]
   **Context**: [Brief description of what was reviewed]
   
   ## Critical Issues
   ...
   
   ## High Priority
   ...
   
   ## Medium Priority
   ...
   
   ## Questions That Need Answers
   - [Question 1]?
   - [Question 2]?
   ```
4. **Update** `FAILS.md` with any failures found

### Document Being Created/Reviewed

**For INFO documents**:
- Are sources still accessible? Try to access them.
- Are findings actually supported by sources, or extrapolated?
- What contradictory information exists? Search for it.
- What changed since document was written?
- Are version numbers and dates still accurate?

**For SPEC documents**:
- What happens when [X] fails? (for every external dependency)
- What happens with invalid input? Empty input? Huge input?
- What concurrent access scenarios exist?
- What are the implicit assumptions not stated?
- What would a malicious user try?
- Are success criteria measurable and testable?

**For IMPL documents**:
- Does the plan match the spec exactly? Diff them mentally.
- What steps could fail silently?
- What cleanup is needed if step N fails after step N-1 succeeds?
- Are rollback scenarios defined?
- What happens if implementation is interrupted mid-way?

**For TEST documents**:
- What's NOT being tested?
- Are edge cases from SPEC all covered?
- What integration points are assumed to work?
- Can tests fail for wrong reasons (flaky)?
- Are test dependencies isolated?

### Code Being Created/Reviewed

**Meta-principle behind everything**: Where is the complexity hiding, and who will pay for it in the long-term?

Create `[filename]_REVIEW.md` with findings.

**First, read all relevant context and answer these architectural questions:**

1. **What are the explicit invariants, and where are they enforced?**
   Unenforced invariants lead to latent bugs and silent data corruption.

2. **Where is the single source of truth, and how is divergence detected or prevented?**
   Multiple authorities inevitably drift and create hard-to-debug failures.

3. **For each failure class, do we fail fast or degrade gracefully, and does this choice preserve guarantees?**
   Error-handling strategy defines real robustness and data safety.

4. **Is the design introducing unnecessary code paths, modes, or abstractions that can be eliminated?**
   Each extra dimension multiplies complexity, failure surface, and test cost.

5. **Can the core logic be tested deterministically without mocks, global state, or time?**
   Testability reflects separation of policy from mechanism and long-term maintainability.

**Then review implementation details:**

**Error Handling**:
- Every try/catch: What specific errors? Generic catch hides bugs.
- Every async call: What if it times out? Rejects? Returns unexpected shape?
- Every file operation: What if file missing? Permissions? Disk full?
- Every network call: What if DNS fails? Connection reset? Partial response?

**State Management**:
- What global state is touched? Can it be corrupted?
- What happens if called twice rapidly?
- What happens if called with stale data?
- Are there memory leaks? (event listeners, timers, closures)

**Dependencies**:
- What versions are assumed? Check for breaking changes in newer versions.
- What if dependency is unavailable at runtime?
- Are there circular dependencies?

**Security** (if applicable):
- Input validation: SQL injection, Cross-Site Scripting (XSS), path traversal?
- Authentication: Can it be bypassed?
- Authorization: Are all paths checked?
- Secrets: Hardcoded or properly externalized?

**Performance**:
- What's the worst-case complexity?
- What if data grows 100x?
- Are there N+1 query patterns?
- Any unbounded loops or recursion?

### Logs/Console Output Review

When reviewing error logs or console output:

1. **Categorize each error/warning**:
   - Expected and handled?
   - Expected but not handled?
   - Unexpected - needs investigation?

2. **Trace to root cause**:
   - Don't stop at symptoms
   - Find the first domino that fell

3. **Check for patterns**:
   - Repeated errors = systemic issue
   - Timing patterns = race condition or resource exhaustion
   - Cascading errors = missing error boundaries

4. **Update** `_PROBLEMS_REVIEW.md` and `FAILS.md` with root causes found

## Devil's Advocate Questions

Ask these for EVERY review:

1. **What's the worst thing that could happen?**
2. **What assumptions are we making about the environment?**
3. **What happens when [external system] is down?**
4. **What happens with 0 items? 1 item? 1 million items?**
5. **What happens if this runs twice? Concurrently?**
6. **What sensitive data could leak in logs/errors?**
7. **What would break if we deployed this at 3 AM during a database migration?**
8. **What would a new team member misunderstand?**

## Final Checklist

Before finishing, verify:

- [ ] `FAILS.md` updated with actual failures discovered (categorized by severity)
- [ ] `[filename]_REVIEW.md` created for specific document/code review
- [ ] `_PROBLEMS_REVIEW.md` created only for conversation/logs review (no specific file)
- [ ] No original files were modified
- [ ] Each finding has: What, Where, Why it went wrong, Suggested fix
- [ ] Critical issues highlighted at top
- [ ] Questions needing answers are listed
- [ ] **MUST-RESEARCH list created** - 5 topics identified and researched
- [ ] **Industry Research Findings section** added to review file
- [ ] Research was done for uncertain claims (web search, docs)
- [ ] **MUST-NOT-FORGET list verified** - all constraints checked, nothing missed

## Output Format

End every Devil's Advocate review with:

```
## Devil's Advocate Summary

**Reviewed**: [What was reviewed]
**Time spent**: [Duration]

**Research Topics Investigated**:
1. [Topic 1] - [Key finding]
2. [Topic 2] - [Key finding]
3. [Topic 3] - [Key finding]
4. [Topic 4] - [Key finding]
5. [Topic 5] - [Key finding]

**Findings**:
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

**Top 3 Risks**:
1. [Most critical issue - one line]
2. [Second most critical - one line]
3. [Third most critical - one line]

**Industry Alternatives Identified**:
- [Alternative approach worth considering]

**Files Created/Updated**:
- `FAILS.md` - [X] new entries
- `[filename]_REVIEW.md` - Detailed findings + Industry Research

**Recommendation**: [PROCEED / PROCEED WITH CAUTION / STOP AND FIX]
```
