---
description: DELIVER phase - complete and hand off
phase: DELIVER
---

# Deliver Workflow

## Required Skills

- @git-conventions for commit/merge
- @edird-phase-model for gate details

## Phase: DELIVER

**Entry gate:** REFINE→DELIVER passed

### Verb Sequence

1. [VALIDATE] with [ACTOR] (final approval)
2. [MERGE] branches (if applicable)
3. [DEPLOY] to environment (if applicable)
4. [FINALIZE] documentation
5. [HANDOFF] communicate completion
6. [CLOSE] mark as done
7. [ARCHIVE] session (if session-based)

### For BUILD

- [MERGE] and [DEPLOY] typically required
- [VALIDATE] ensures [ACTOR] approves before merge

### For SOLVE

- [CONCLUDE] draw final conclusions
- [RECOMMEND] with rationale (or [PROPOSE] if multiple options)
- [PRESENT] findings to [ACTOR]

### Gate Check: DELIVER→DONE

- [ ] Work validated with [ACTOR]
- [ ] For BUILD: Merged and deployed (if applicable)
- [ ] For SOLVE: Conclusions documented
- [ ] Session closed (if session-based)

**Pass**: Workflow complete | **Fail**: Continue [DELIVER]

## Output

Update NOTES.md with:
```markdown
## Current Phase

**Phase**: DELIVER
**Status**: Complete
```

Run `/session-close` if session-based workflow.
