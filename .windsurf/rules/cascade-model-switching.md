# Cascade Model Switching

## Required Skills

- `@windsurf-auto-model-switcher` for model switching script
- `@windows-desktop-control` for screenshot-based safety checks

## Overview

Automatically switch AI models based on task type and STRUT or TASKS hints.

## Model Hints

STRUT Strategy sections may include model hints:
```
├─ Strategy: Analyze requirements, design solution
│   - Opus for analysis, Sonnet for implementation
```

Hints are recommendations - agent decides based on actual task.

## Default Model Selection

When no STRUT hint exists, use task-based selection:
- **MODEL-HIGH** (Planning/Analysis): Claude Opus 4.5 (Thinking)
- **MODEL-MID** (Implementation/Bugfix): Claude Sonnet 4.5
- **MODEL-LOW** (git, files, scripts): Claude Haiku 4.5

## Safety Conditions (ALL required)

Auto-switching ONLY happens if NO user activity detected:

1. **OUR Windsurf instance in foreground** - Not another app, not another Windsurf window
2. **OUR conversation open in Cascade** - The conversation we are in, not a different one
3. **User NOT doing anything else** - Not typing in editor, not selecting text, not scrolling
4. **Cascade chat input is empty** - Only queued commands allowed, no partial user input

**If ANY condition fails: Skip switch silently.**

## Switching Procedure

1. Take screenshot using `@windows-desktop-control` skill
2. Analyze screenshot for ALL safety conditions:
   - Is Windsurf the foreground window?
   - Is Cascade panel visible?
   - Is our conversation showing (check conversation title/context)?
   - Is the code editor idle (no cursor activity, no selection)?
   - Is the Cascade chat input field empty?
3. If ALL conditions met: Run `select-windsurf-model-in-ide.ps1 -Query "<model>"`
4. If ANY condition fails: Do not switch, do not log, do not notify
5. **After task completion: Switch back to original model**

## Switch-Back Pattern

After completing a task with a different model, ALWAYS switch back to the original model:

```
1. Complete the task (implementation, bugfix, chores)
2. Run safety check (screenshot + analysis)
3. If safe: Switch back to original model
4. Continue with next task
```

**Example:**
- Start: Opus (planning)
- Switch to: Sonnet (implementation)
- Complete: Implementation done
- Switch back: Opus (for next planning task)

**Why:** Prevents model drift - ensures user returns to expected model for next interaction.
