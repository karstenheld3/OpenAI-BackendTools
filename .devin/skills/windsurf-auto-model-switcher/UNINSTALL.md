# Uninstall: Windsurf Auto Model Switcher

Remove the custom keybindings for model switching.

## Automatic Uninstall (PowerShell)

Run this script to remove the keybindings:

```powershell
$keybindingsPath = "$env:APPDATA\Windsurf\User\keybindings.json"

if (-not (Test-Path $keybindingsPath)) {
    Write-Host "Keybindings file not found: $keybindingsPath"
    exit 0
}

# Read existing keybindings
$keybindings = Get-Content $keybindingsPath -Raw | ConvertFrom-Json

# Commands to remove
$commandsToRemove = @(
    "windsurf.cascade.toggleModelSelector",
    "windsurf.cascade.switchToNextModel"
)

# Filter out our keybindings
$originalCount = $keybindings.Count
$keybindings = $keybindings | Where-Object { $_.command -notin $commandsToRemove }
$removedCount = $originalCount - $keybindings.Count

if ($removedCount -gt 0) {
    # Save
    $keybindings | ConvertTo-Json -Depth 10 | Set-Content $keybindingsPath -Encoding UTF8
    Write-Host "Removed $removedCount keybinding(s)"
    Write-Host "Restart Windsurf to apply changes."
} else {
    Write-Host "No model switcher keybindings found to remove."
}
```

## Manual Uninstall

1. Open Windsurf
2. Press `Ctrl+Shift+P` -> "Preferences: Open Keyboard Shortcuts (JSON)"
3. Remove entries with these commands:
   - `windsurf.cascade.toggleModelSelector`
   - `windsurf.cascade.switchToNextModel`
4. Save and restart Windsurf

## Verify Uninstall

1. Open Windsurf
2. Press `Ctrl+Shift+F9`
3. Nothing should happen (or default behavior)

## What Gets Removed

| Shortcut | Command |
|----------|---------|
| Ctrl+Shift+F9 | `windsurf.cascade.toggleModelSelector` |
| Ctrl+Shift+F10 | `windsurf.cascade.switchToNextModel` |

Note: This only removes the custom keybindings. The default Windsurf keybindings (`Ctrl+/` and `Ctrl+Shift+/`) remain unaffected.
