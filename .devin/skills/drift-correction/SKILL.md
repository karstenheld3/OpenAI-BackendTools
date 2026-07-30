# Drift Correction Skill

**Goal**: Drift detection knowledge, correction guidance, and process discipline audit criteria for `/drift-detect` and `/drift-correct`

## Overview

Drift Correction ensures agents follow instructions completely. This skill provides drift detection knowledge, correction guidance, and CHECKS files used by `/drift-detect` and `/drift-correct` after task completion.

## GRUC File Placement

GRUC (Guides, Rules, Checks) files are distributed by consumer alignment:

- **GUIDE** files - in each skill folder (consumed by working agent BEFORE execution)
- **RULES** files - in each skill folder (consumed by `/verify`, `/improve` AFTER execution)
- **CHECKS** files for skills - in each skill folder (alongside GUIDE and RULES)
- **CHECKS** files for workflows - in this skill folder (consumed by `/drift-detect` AFTER execution)

**Why workflow CHECKS are centralized here**: `/drift-detect` is the sole consumer of CHECKS files. Placing workflow CHECKS in the consumer's skill prevents working agents from seeing audit criteria during execution, which would cause superficial compliance (gaming).

**Exception**: `write-documents` keeps all three GRUC types in its own folder per design constraint.

## File Structure

```
drift-correction/
├── SKILL.md                       # This file
├── DRIFT_DETECTION.md             # Detection knowledge (drift lenses, DoD extraction)
├── DRIFT_CORRECTION.md            # Correction knowledge (gap closure strategies)
├── DRIFT_TEMPLATE.md              # Template for __DRIFT_[TOPIC].md files
├── DRIFTS_TEMPLATE.md             # Template for DRIFTS.md log entries
├── [WORKFLOW]_CHECKS.md            # One file per auditable workflow (created on demand)
└── ...
```

Skill CHECKS reside in their own skill folder:
```
deep-research/
├── SKILL.md
├── RESEARCH_RULES.md
└── RESEARCH_CHECKS.md             # Process checks for research skill
```

## CHECKS File Convention

Each CHECKS file follows the pattern from `_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` section 9.3:

- **Action-oriented** - describes what the agent MUST HAVE DONE
- **Evidence-based** - specifies what proves compliance
- **Failure indicators** - describes what non-compliance looks like
- **Severity levels** - CRITICAL, HIGH, MEDIUM
- **Invisible to executor** - never referenced in workflows, SKILL.md intent lookups, or MNF sections

### CHECKS File Template

```markdown
# [Domain] Checks

[One-line: what process discipline this audits]

**Evidence sources:** conversation logs, git history, file timestamps, terminal output

## Check Index

Process ([2-letter prefix])
- [PREFIX]-[CAT]-[NN]: [Action that must have happened]

## [Check ID]: [Check Name]

**Evidence**: [What proves the action occurred]
**Failure indicator**: [What absence or contradiction indicates non-compliance]
**Severity**: CRITICAL | HIGH | MEDIUM
```

## Consumer

Only `/drift-detect` reads CHECKS files from this skill. The working agent NEVER sees CHECKS during execution.

## Related Documentation

- `_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` - GRUC theory and writing patterns
- `_INFO_AGENT_DRIFT_PREVENTION_APPROACH.md [ADP-IN01]` - Drift correction methodology and scope model
