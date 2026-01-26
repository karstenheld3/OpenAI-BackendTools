---
description: Create INFO document from research
auto_execution_mode: 1
---

# Write INFO Workflow

Create research and analysis documents following INFO_TEMPLATE.md structure.

## Required Skills

Invoke these skills before proceeding:
- @write-documents for INFO document structure and formatting rules

## Prerequisites

- User has described a research topic, question, or analysis goal
- Clarify scope before starting if ambiguous
- Read @write-documents skill and INFO_TEMPLATE.md

## Steps

1. **Create INFO File**
   - Create `_INFO_[TOPIC].md` in session folder
   - Header block: Doc ID (`[TOPIC]-IN[NN]`), Goal, Timeline
   - Add empty Summary section (fill last)

2. **Make Research Plan**
   - Identify 3-5 key questions to answer
   - List potential sources (docs, code, web, APIs)
   - Estimate scope: narrow (single source) vs broad (multi-source comparison)

3. **Research Step-by-Step**
   - Add sections incrementally as findings emerge
   - After each section, ask:
     - Do I need to verify these findings with further research?
     - Can I remove duplicates?
     - Can I remove unverified or contradicting findings?
     - Is this information really helpful? If yes, why?
   - Review new sections in context of existing ones
   - Remove cognitive overload, redundancies, ambiguities

4. **Think Outside the Box**
   - If no verified solution exists, reconsider the problem
   - Are we missing important points or perspectives?
   - Are there clever alternatives we overlooked?
   - Avoid polluting document with non-working solutions

5. **Document Sources**
   - Use source IDs: `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`
   - List URL and primary finding for each source
   - Mark verified sources with `[VERIFIED]`

6. **Write Summary**
   - Copy/paste ready list at document top
   - Label findings: `[ASSUMED]`, `[VERIFIED]`, `[TESTED]`, `[PROVEN]`
   - Most important findings first

7. **Add Next Steps**
   - Actionable items based on findings
   - Link to follow-up work (SPEC, IMPL, decision needed)

8. **Verify**
   - Run `/verify` workflow
   - Check: All questions answered? Sources documented? Summary accurate?

## Document Structure

See `INFO_TEMPLATE.md` in @write-documents skill for complete template.

```markdown
# INFO: [Topic]

**Doc ID**: [TOPIC]-IN[NN]
**Goal**: [Single sentence]
**Timeline**: Created YYYY-MM-DD

## Summary
- [Key finding 1] [VERIFIED]
- [Key finding 2] [ASSUMED]

## Table of Contents
...

## 1. [Section]
...

## Sources
- `TOPIC-IN01-SC-SITE-PAGE`: [URL] - [Finding]

## Next Steps
1. [Action]

## Document History
**[YYYY-MM-DD HH:MM]**
- Initial research document created
```
