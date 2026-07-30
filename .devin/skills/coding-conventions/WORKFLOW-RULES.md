# Workflow Rules

## Target Audience

Skill files are consumed by LLMs, not humans. Optimize for:
- Medium-reasoning models
- Low context windows - every saved token = more space for the actual task
- Instruction following over prose comprehension
- APAPALAN principle: As precise as possible, as little as necessary.

Design principles:
1. Maximum clarity - one interpretation per instruction, no ambiguity
2. Numbered steps - LLMs follow numbered sequences better than prose
3. MUST-NOT-FORGET technique - for complex skills with verification (SETUP.md, UNINSTALL.md)
4. No visual formatting in LLM-consumed files - `**bold**` adds tokens without improving comprehension
5. Headers as structure - `#` and `##` are parsing boundaries LLMs rely on
6. Compact format for lookups - one line per resource, no multi-line entries
7. Verbose format only when justified - multi-step reasoning, troubleshooting, code with explanation
8. JSON intermediate output - for multi-step workflows, require LLM to emit structured JSON between steps to enforce explicit reasoning and prevent drift

JSON intermediate output example:

```
## Step 3: Determine context
Emit before proceeding:
{"context": "INFO|SPEC|IMPL|Code|TEST|Session|Workflow|Skill", "reason": "..."}
```

This forces the LLM to commit to a decision before acting, reducing errors in medium-reasoning models.

## Formatting

1. Frontmatter: only `description` field. No `phase:` or other extras.
2. References:
   - Workflow refs as inline code: `/verify`, `/research`
   - Skill refs with @skills: prefix: `@skills:skill-name`
3. Steps: numbered, actionable verbs
4. No hardcoded paths. Use placeholders: `[WORKSPACE_FOLDER]`, `[SESSION_FOLDER]`
5. No `## Usage` sections that just show the workflow command. Only add if showing parameters.
6. No replication of rules defined elsewhere. Reference the source instead.

## Structure

Complex workflows: separate GLOBAL-RULES and CONTEXT-SPECIFIC sections.

```
# [Name] Workflow

## GLOBAL-RULES
- Rule 1

# CONTEXT-SPECIFIC

## Context A
- Rule for A
```

See `/verify` as canonical example.

## Token Optimization

Workflows and skills are consumed by LLMs, not humans.

Remove:
- `**Bold**` markup in LLM-consumed files (LLMs parse plain text equally well)
- Filler prose: "This section covers", "The following resources"
- Prose that restates the heading
- Blank lines between every list item when grouping is clear from headers

Keep:
- `#` and `## ` headers (LLMs use these as parsing boundaries)
- Parenthetical notes with critical context
- All technical detail, URLs, parameters
- Concrete examples (BAD/GOOD pairs)

Test: "Remove this token. Does the LLM lose information?" No? Remove it.

For complex workflows that require end-verification, use MUST-NOT-FORGET technique:

```
### MUST-NOT-FORGET (check after completion)
- [ ] Item 1
- [ ] Item 2

### Steps
1. Do thing
2. Do other thing
3. Walk MUST-NOT-FORGET list. All checked?
```

## Quality Checks

When verifying workflows:
- Ambiguities: unclear instructions with multiple interpretations?
- Term conflicts: same concept named differently?
- Underspecified behavior: missing edge cases?
- Outdated references: broken links to renamed/removed items?

Cross-reference checklist:
- [ ] All `/workflow` refs exist in workflows folder
- [ ] All `@skills:` refs exist in skills folder
- [ ] All `[STATE]` refs defined in ID-REGISTRY.md
- [ ] All document refs use correct naming conventions
