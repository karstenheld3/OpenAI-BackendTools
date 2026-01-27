# Update Model Registry Workflow

Update `windsurf-model-registry.json` with current models and costs.

## Data Sources (Priority Order)

1. **Windsurf Docs** (preferred) - https://docs.windsurf.com/windsurf/models
2. **UI Screenshot Capture** (fallback) - when docs are outdated or unavailable

## Method A: Windsurf Docs (Recommended)

### Step 1: Fetch Model Data

Use web search or read URL:
```
https://docs.windsurf.com/windsurf/models
```

### Step 2: Extract Models and Costs

Parse the page for model names and credit costs.

### Step 3: Update Registry

Update `windsurf-model-registry.json` with extracted data.

## Method B: UI Screenshot Capture (Fallback)

Use when docs are outdated or don't match UI.

**IMPORTANT:** Use `capture-model-selector.ps1` for model registry updates ONLY. For general screenshots, use `windows-desktop-control/simple-screenshot.ps1` instead.

### Step 1: Capture All Sections

```powershell
.\capture-model-selector.ps1 -MaxSections 10
```

**Note:** This script opens the model selector popup and sends keystrokes to scroll through the list. Uses DPI-aware fullscreen capture.

### Step 2: Cascade Reads Screenshots

Cascade reads each fullscreen screenshot from `.tools/_screenshots/`.
Extracts model names and costs from the popup visible in each image.

### Step 3: Stop When List Wraps

When Cascade sees duplicate models (list wrapped around), extraction is complete.

### Step 4: Update Registry

Update `windsurf-model-registry.json` with discovered models and costs.

### Step 5: Cleanup (Only After Success)

**IMPORTANT:** Only delete screenshots after successfully updating `windsurf-model-registry.json`.

```powershell
Remove-Item -Path "[WORKSPACE]/.tools/_screenshots/*.jpg" -Force
```

If extraction failed, keep screenshots for debugging.

## Method C: Playwright (Last Resort)

If docs blocked or UI capture fails, use Playwright MCP to navigate:
1. Open https://docs.windsurf.com/windsurf/models
2. Extract model table data
3. Update registry

## Output Format

```json
{
  "_version": "1.4",
  "_updated": "2026-01-26",
  "_source": "docs.windsurf.com/windsurf/models",
  "models": [
    { "name": "Claude 3.5 Sonnet", "cost": "2x" }
  ]
}
```
