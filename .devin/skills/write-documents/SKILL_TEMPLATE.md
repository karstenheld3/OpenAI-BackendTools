# Skill Template

Template for writing skill documents.

## SKILL.md Structure

```markdown
---
name: [skill-name]
description: [When to apply this skill. One to three sentences covering trigger conditions and what the skill enables.]
compatibility: [Runtime requirements, e.g., "Requires Node.js 18+"]
---

# [Skill Title]

[One-liner: what this skill provides and how it relates to the underlying tool/concept.]

**References** (loaded on demand):
- [SKILLPREFIX_TOPIC.md](SKILLPREFIX_TOPIC.md) - [What it covers]

## MUST-NOT-FORGET

1. [Critical rule - most common mistake]
2. [Critical rule - data loss or security risk]
3. [Critical rule - API gotcha]

## Intent Lookup

**User wants to...**
- **[Goal A]** → [Procedure or section reference]
- **[Goal B]** → [Procedure or section reference]

## Core Procedures

### 1. [Procedure Name]

` ` `
1. [Step]
2. [Step]
` ` `

[Brief explanation of when/why to use this procedure.]

### 2. [Procedure Name]

` ` `
1. [Step]
2. [Step]
` ` `

## Gotchas

- **[Short label]** - [Explanation and fix]

## Quick Config

[Minimal copy-paste configuration to get started.]
```

## Optional Sections

Include based on skill complexity:

- **References** - Skill has supporting files
- **MUST-NOT-FORGET** - Always (even 2-3 items)
- **Intent Lookup** - Skill covers multiple use cases
- **Core Procedures** - Skill has step-by-step workflows
- **Gotchas** - Tool has non-obvious behavior
- **Quick Config** - Tool requires configuration

## Complexity Tiers

**Tier 1: Simple** (50-100 lines, 1-2 files)
- Frontmatter, title, MNF, procedures

**Tier 2: Standard** (100-200 lines, 3-5 files)
- Add Intent Lookup, Gotchas, Quick Config, supporting references

**Tier 3: Comprehensive** (200+ lines, 5-8 files)
- All sections, multiple reference files, config examples
