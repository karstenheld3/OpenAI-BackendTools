# Skill Document Rules

Rules for writing skill folders and SKILL.md files.

**Writing quality:** Apply `APAPALAN_RULES.md` to all skill content. Key rules for skills: AP-PR-07 (be specific), AP-BR-02 (sacrifice grammar for brevity), AP-NM-01 (one name per concept).

## Rule Index

Header (HD)
- SK-HD-01: YAML frontmatter with `name` and `description` required
- SK-HD-02: `description` must state when to apply (trigger conditions)
- SK-HD-03: Include `compatibility` field if tool has runtime requirements

Structure (ST)
- SK-ST-01: SKILL.md is the entry point - must be self-contained for common use cases
- SK-ST-02: Include MUST-NOT-FORGET section (3-10 items, ordered by impact)
- SK-ST-03: Include Intent Lookup when skill covers multiple use cases
- SK-ST-04: Procedures use numbered steps with tool invocations
- SK-ST-05: SETUP.md must include pre-installation verification section with checklist
- SK-ST-06: SETUP.md installation must be idempotent with backup-before-modify
- SK-ST-07: UNINSTALL.md must include pre-uninstall verification section

Files (FL)
- SK-FL-01: Flat layout - no subdirectories for fewer than 12 files
- SK-FL-02: Standard files keep standard names: `SETUP.md`, `UNINSTALL.md`
- SK-FL-03: Skill-specific files use skill prefix: `PLAYWRIGHT_TOOLS.md`, `GIT_HOOKS.md`
- SK-FL-04: Config example files use lowercase: `playwright_config_examples.json`
- SK-FL-05: All files referenced from SKILL.md References section
- SK-FL-06: 12+ files for a specific topic justifies a subfolder (e.g., `examples/`)

Content (CT)
- SK-CT-01: SKILL.md provides procedures and decision logic, not tool parameter docs
- SK-CT-02: Tool parameters come from MCP handshake or `--help` - do not duplicate
- SK-CT-03: Gotchas section for non-obvious behavior, deprecated APIs, common mistakes
- SK-CT-04: Quick Config section with minimal copy-paste examples
- SK-CT-05: No visual-only formatting in LLM-consumed reference files (no bold, no filler phrases)

## SK-HD-01: Frontmatter

**BAD:**
```yaml
---
name: playwright
---
```

**GOOD:**
```yaml
---
name: ms-playwright-mcp
description: Automates browser interactions via Microsoft Playwright MCP server. Use when navigating websites, filling forms, or testing web UI.
compatibility: Requires Node.js 18+ and @playwright/mcp package via npx
---
```

## SK-ST-01: Self-Contained SKILL.md

SKILL.md must answer the most common questions without loading reference files. Reference files are for deep dives.

**BAD:** SKILL.md says "See TOOLS.md for available tools" with no tool summary.

**GOOD:** SKILL.md has quick reference of core tools, links to TOOLS.md for full catalog.

## SK-FL-01: Flat Layout

**BAD:**
```
my-skill/
  SKILL.md
  references/
    AUTH.md
  assets/
    config.json
```

**GOOD:**
```
my-skill/
  SKILL.md
  MYSKILL_AUTH.md
  myskill_config.json
```

## SK-FL-02: Standard File Names

Files that exist across multiple skills keep unprefixed names for consistency.

**Standard names:** `SETUP.md`, `UNINSTALL.md`

**BAD:** `PLAYWRIGHT_SETUP.md`, `GIT_UNINSTALL.md`

**GOOD:** `SETUP.md`, `UNINSTALL.md`

## SK-FL-03: Skill-Specific Prefix

Files unique to a skill use an uppercase prefix derived from the skill's domain.

**BAD:** `TOOLS.md` (ambiguous across skills)

**GOOD:** `PLAYWRIGHT_TOOLS.md` (clearly scoped)

## SK-CT-01: Procedures Over Parameters

Skills teach *how* and *when*, not *what parameters exist*.

**BAD:** "`browser_click` accepts `ref` (string), `element` (string), `button` (enum: left, right, middle)"

**GOOD:** "After navigation or click, always re-snapshot before clicking - refs are ephemeral"
