---
description: Switch Cascade AI model tier (HIGH, MID, LOW)
---

# Switch Model Workflow

Switch to a different AI model tier. Direct execution - no file reads.

## Configuration

```
MODEL-HIGH = "Claude Opus 4.5 (Thinking)"
MODEL-HIGH-QUERY = "opus 4.5 thinking"

MODEL-MID = "Claude Sonnet 4.5"
MODEL-MID-QUERY = "sonnet 4.5"

MODEL-LOW = "Gemini 3 Flash Medium"
MODEL-LOW-QUERY = "gemini 3 flash medium"
```

## Required Skills

- `@windsurf-auto-model-switcher` for model switching

## Usage

```
/switch-model MODEL-HIGH (or 'high' or 'h' )
/switch-model MODEL-MID (or 'mid' or 'm' )
/switch-model MODEL-LOW (or 'low' or 'l' )
```

## Execute

Based on tier argument, run from `.windsurf/skills/windsurf-auto-model-switcher/`:

**MODEL-HIGH:**
```powershell
.\select-windsurf-model-in-ide.ps1 -Query "[MODEL-HIGH-QUERY]"
```

**MODEL-MID:**
```powershell
.\select-windsurf-model-in-ide.ps1 -Query "[MODEL-MID-QUERY]"
```

**MODEL-LOW:**
```powershell
.\select-windsurf-model-in-ide.ps1 -Query "[MODEL-LOW-QUERY]"
```

See `@windsurf-auto-model-switcher` skill for script details.

## Confirm

Report: "Switched to [MODEL-*]. Takes effect on next message."

Where [MODEL-*] is the configured model name (MODEL-HIGH, MODEL-MID, or MODEL-LOW from Configuration section)

## Notes

- Model switch takes effect on user's NEXT message
- To change tier → model mapping, edit this workflow
- Safety checks only apply for autonomous agent switching (see `cascade-model-switching.md`)
