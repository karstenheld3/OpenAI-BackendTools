# Skill Writing Guide

Step-by-step guide for creating well-structured agent skills.

## 1. Research First

Before writing any skill:

1. Understand the technology - how does it actually work?
2. Verify compatibility - does it work with the target agent (Windsurf/Cascade)?
3. Identify dependencies - what must be installed? What versions?
4. Find known issues - check GitHub issues, forums, community reports
5. Test manually first - run commands yourself before documenting them

Document research in an INFO document or directly in SKILL.md.

## 2. Determine Skill Type

Classify before writing:

- **Instructional** - Multi-step procedures, decision logic, gotchas (e.g., `ms-playwright-mcp`)
- **Resource/lookup** - URL collections, reference lists (e.g., `travel-info`)
- **Setup-heavy** - Tool installation with system modifications (e.g., `computer-use-mcp`)

This determines format density:
- Instructional → standard format per `SKILL_TEMPLATE.md`
- Resource/lookup → compact format (one line per resource, no bullets)
- Setup-heavy → verbose SETUP.md/UNINSTALL.md with verification steps

## 3. Write SKILL.md

Follow `SKILL_TEMPLATE.md` structure. Key decisions:

**Frontmatter**: `name`, `description` (trigger conditions), `compatibility` (runtime needs)

**MUST-NOT-FORGET**: 3-10 items. Order by impact. Include:
- Most common mistake users make
- Data loss or security risks
- API gotchas (deprecated names, breaking changes)

**Intent Lookup**: Map user goals to procedures. Think "user wants to..." then arrow to action.

**Core Procedures**: Numbered steps with tool invocations. One procedure per common task.

**Gotchas**: Non-obvious behavior. Format: `**Short label** - explanation and fix`

## 4. Token Optimization

Skill files are consumed by LLMs. Every token costs context window space.

**Remove** (visual-only, no LLM benefit):
- `**Bold**` markup in LLM-consumed reference files
- Verbose prefixes (`- **URL:** `, `- **Best for:** `) where compact format works
- Redundant prose restating headings
- Filler phrases: "This section covers", "The following resources"

**Keep** (improves LLM comprehension):
- `#` and `##` headers (structural parsing boundaries)
- Keywords/trigger lines (how the LLM finds the right file)
- Parenthetical notes with critical context
- All URLs, parameters, and technical detail
- Concrete examples

**Review metric**: "If I remove this token, does the LLM lose information?" If no, remove it.

Exception: SETUP.md and UNINSTALL.md may use richer formatting because they guide human users through system changes.

## 5. Write SETUP.md (If Needed)

Only if skill requires installation or system modification.

### 5.1 Pre-Installation Verification

Test WITHOUT modifying the system first:

```markdown
## Pre-Installation Verification

Complete ALL steps before modifying your system.

## 1. Verify [Prerequisite]
[commands]
Expected: [what user should see]

## 2. Test [Core Functionality]
[commands that test WITHOUT modifying system]
Expected: [what success looks like]

## Pre-Installation Checklist
- [ ] Prerequisite 1 verified
- [ ] Core functionality tested
- [ ] System state checked

**If all checks pass, proceed to installation.**
```

### 5.2 Installation

1. Backup existing configuration
2. Make minimal changes
3. Provide rollback instructions inline
4. Show expected results after each step

### 5.3 MCP Config Modification Pattern (Windsurf)

For skills modifying `~/.codeium/windsurf/mcp_config.json`:

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

$targetServer = @{
    command = "npx"
    args = @("package-name")
}

# Read existing config
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
} else {
    $config = @{ mcpServers = @{} }
}

# Convert PSCustomObject to Hashtable if needed
if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Idempotent check
if ($config.mcpServers.ContainsKey("server-name")) {
    $currentJson = $config.mcpServers["server-name"] | ConvertTo-Json -Compress
    $targetJson = $targetServer | ConvertTo-Json -Compress
    if ($currentJson -eq $targetJson) {
        Write-Host "Already configured" -ForegroundColor Green
        return
    }
}

# Backup before modifying
$backupPath = "$configPath._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configPath $backupPath -ErrorAction SilentlyContinue

# Add/update server
$config.mcpServers["server-name"] = $targetServer
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
```

Requirements: idempotent, backup first, handle PSCustomObject, compare before write.

### 5.4 Post-Installation Verification

1. Verify installation succeeded
2. Test actual functionality
3. Document expected behavior
4. Provide troubleshooting for common failures

## 6. Write UNINSTALL.md (Required If SETUP.md Exists)

### 6.1 Pre-Uninstall Verification

```markdown
## Pre-Uninstall Verification

## 1. Check Current Installation
[commands to show what's installed]
Expected: [what indicates it's installed]

## 2. Check Dependencies
[commands to identify what depends on this]
If dependencies found: [what to do]

## Pre-Uninstall Checklist
- [ ] Current installation verified
- [ ] Dependencies checked
- [ ] Backup created (if needed)

**If all checks pass, proceed to uninstall.**
```

### 6.2 Uninstall

1. Remove in reverse order of installation
2. Show what each step removes
3. Verify removal after each step

### 6.3 Post-Uninstall Verification

1. Confirm all components removed
2. Verify system returned to clean state
3. Note any manual cleanup needed

## 7. File Layout

Apply `SKILL_RULES.md` SK-FL-* rules:

```
my-skill/
  SKILL.md                    # Required entry point
  SETUP.md                    # Standard name (unprefixed)
  UNINSTALL.md                # Standard name (unprefixed)
  MYSKILL_REFERENCE.md        # Skill-specific (prefixed)
  myskill_config_examples.json # Data files (lowercase)
```

## 8. Review Checklist

Before publishing:

- [ ] Research documented (INFO or in SKILL.md)
- [ ] SKILL.md has MUST-NOT-FORGET section
- [ ] SKILL.md self-contained for common use cases
- [ ] File layout follows SK-FL-* rules
- [ ] If SETUP.md exists: pre-installation verification present
- [ ] If SETUP.md exists: UNINSTALL.md also exists
- [ ] All code snippets tested manually
- [ ] Expected output documented for each step
- [ ] Token optimization applied (no visual-only formatting in LLM-consumed files)
- [ ] References link to primary sources
