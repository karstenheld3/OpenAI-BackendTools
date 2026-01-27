# Setup: Windsurf Auto Model Switcher

Install the required keybindings for model switching.

## Automatic Setup (PowerShell)

Run this script to add the keybindings:

```powershell
$keybindingsPath = "$env:APPDATA\Windsurf\User\keybindings.json"

# Read existing keybindings or create empty array
if (Test-Path $keybindingsPath) {
    $keybindings = Get-Content $keybindingsPath -Raw | ConvertFrom-Json
} else {
    $keybindings = @()
}

# Convert to ArrayList for manipulation
$keybindings = [System.Collections.ArrayList]@($keybindings)

# New keybindings to add
$newBindings = @(
    @{
        key = "ctrl+shift+f9"
        command = "windsurf.cascade.toggleModelSelector"
        when = "!terminalFocus"
    },
    @{
        key = "ctrl+shift+f10"
        command = "windsurf.cascade.switchToNextModel"
        when = "!terminalFocus"
    }
)

# Add new bindings (skip if already exists)
foreach ($binding in $newBindings) {
    $exists = $keybindings | Where-Object { $_.key -eq $binding.key -and $_.command -eq $binding.command }
    if (-not $exists) {
        $keybindings.Add([PSCustomObject]$binding) | Out-Null
        Write-Host "Added: $($binding.key) -> $($binding.command)"
    } else {
        Write-Host "Already exists: $($binding.key)"
    }
}

# Save
$keybindings | ConvertTo-Json -Depth 10 | Set-Content $keybindingsPath -Encoding UTF8
Write-Host "`nKeybindings saved to: $keybindingsPath"
Write-Host "Restart Windsurf to apply changes."
```

## Manual Setup

1. Open Windsurf
2. Press `Ctrl+Shift+P` -> "Preferences: Open Keyboard Shortcuts (JSON)"
3. Add the following entries to the JSON array:

```json
{
  "key": "ctrl+shift+f9",
  "command": "windsurf.cascade.toggleModelSelector",
  "when": "!terminalFocus"
},
{
  "key": "ctrl+shift+f10",
  "command": "windsurf.cascade.switchToNextModel",
  "when": "!terminalFocus"
}
```

4. Save and restart Windsurf

## Verify Installation

1. Open Windsurf
2. Press `Ctrl+Shift+F9`
3. The model selector popup should appear

If it doesn't work:
- Ensure Windsurf was restarted after adding keybindings
- Check that the JSON syntax is valid
- Verify the keybindings file path: `%APPDATA%\Windsurf\User\keybindings.json`
