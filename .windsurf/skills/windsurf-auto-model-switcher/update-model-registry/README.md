# Screenshot Scripts

## For General Screenshots

Use `windows-desktop-control` skill:
```powershell
# From DevSystemV3.2/skills/windows-desktop-control/
.\simple-screenshot.ps1
```

## capture-model-selector.ps1

**Purpose:** Model registry update workflow

**Behavior:** OPENS model selector popup, sends keystrokes, navigates list, takes screenshots

**Use when:**
- Updating windsurf-model-registry.json
- Extracting model names and costs from UI
- Following UPDATE_WINDSURF_MODEL_REGISTRY.md workflow

**WARNING:** This script actively manipulates the UI. Do NOT use for general screenshots.

**Usage:**
```powershell
# Full screen capture with popup navigation
.\capture-with-crop.ps1 -CropX 0 -CropY 0 -CropWidth 2048 -CropHeight 1280 -MaxSections 10
```

## Quick Reference

| Need | Script |
|------|--------|
| Test model switcher | `simple-screenshot.ps1` |
| Verify popup state | `simple-screenshot.ps1` |
| Update model registry | `capture-with-crop.ps1` |
| General screenshots | `simple-screenshot.ps1` |
